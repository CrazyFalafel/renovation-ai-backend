from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def estimate_budget(square_feet, room_type):
    paint_price_per_gallon = 40
    flooring_price_per_box = 60

    paint_gallons = round(float(square_feet) / 350, 1)
    flooring_boxes = round(float(square_feet) / 20, 1)

    if room_type == 'kitchen':
        extra = 500  # cabinets, tile
    elif room_type == 'bathroom':
        extra = 700  # vanity, tiles, toilet
    elif room_type == 'bedroom':
        extra = 300
    elif room_type == 'living_room':
        extra = 400
    elif room_type == 'basement':
        extra = 1500
    elif room_type == 'hallway':
        extra = 150
    elif room_type == 'dining_room':
        extra = 400
    elif room_type == 'garage':
        extra = 1000
    elif room_type == 'garden':
        extra = 1200
    elif room_type == 'exterior':
        extra = 1800
    else:
        extra = 500

    total = round(paint_gallons * paint_price_per_gallon + flooring_boxes * flooring_price_per_box + extra)
    return paint_gallons, flooring_boxes, total

def generate_suggestion(room_type):
    suggestions = {
        'kitchen': 'Modern kitchen with white cabinets, subway tile backsplash, and quartz countertops.',
        'bathroom': 'Spa-inspired bathroom with large tiles, soft lighting, and floating vanity.',
        'bedroom': 'Cozy bedroom with soft neutrals, accent wall, and warm wood flooring.',
        'living_room': 'Scandinavian cozy: white oak flooring, neutral tones, matte black accents.',
        'basement': 'Functional basement with laminate flooring, pot lights, and neutral paint.',
        'hallway': 'Bright hallway with light paint and decorative wall panels.',
        'dining_room': 'Elegant dining room with pendant lighting and textured wallpaper.',
        'garage': 'Clean garage with epoxy floor and wall-mounted shelving.',
        'garden': 'Backyard with composite decking, stone path, and greenery.',
        'exterior': 'Modern curb appeal with updated siding, black trim, and new lighting.'
    }
    return suggestions.get(room_type, 'Simple modern design with light colors and durable materials.')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files or 'room_type' not in request.form:
        return jsonify({'error': 'Missing file or room type'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    square_feet = request.form.get('square_feet')
    room_type = request.form.get('room_type')

    if not square_feet or not room_type:
        return jsonify({'error': 'Missing square footage or room type'}), 400

    room_type = room_type.lower().replace(" ", "_")

    allowed_rooms = [
        'kitchen', 'bathroom', 'bedroom', 'living_room',
        'basement', 'hallway', 'dining_room', 'garage',
        'garden', 'exterior'
    ]

    if room_type not in allowed_rooms:
        return jsonify({'error': f'Room type "{room_type}" not recognized. Try {", ".join(allowed_rooms)}.'}), 400

    paint_gallons, flooring_boxes, estimated_budget = estimate_budget(square_feet, room_type)

    return jsonify({
        'message': 'Image received',
        'filename': filename,
        'square_feet': square_feet,
        'room_type': room_type,
        'suggestion': generate_suggestion(room_type),
        'materials_needed': {
            'paint_gallons': paint_gallons,
            'flooring_boxes': flooring_boxes
        },
        'estimated_budget': estimated_budget
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
