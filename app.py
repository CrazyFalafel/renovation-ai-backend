from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'room_type' not in request.form:
        return jsonify({'error': 'Missing file or room type'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    square_feet = request.form.get('square_feet')
    room_type = request.form.get('room_type')

    if not square_feet or not room_type:
        return jsonify({'error': 'Missing square footage or room type'}), 400

    try:
        sqft = float(square_feet)
    except ValueError:
        return jsonify({'error': 'Invalid square footage'}), 400

    # Suggestions and materials by room
    suggestions = {
        'kitchen': {
            'suggestion': 'Modern clean kitchen with white cabinets, quartz countertops, and soft-close drawers.',
            'paint': 0.5,
            'floor': 0.7,
            'cost_per_sqft': 80
        },
        'bathroom': {
            'suggestion': 'Elegant bathroom with matte tiles, light grey paint, and a black faucet accent.',
            'paint': 0.3,
            'floor': 0.6,
            'cost_per_sqft': 120
        },
        'living_room': {
            'suggestion': 'Scandinavian cozy: white oak flooring, neutral tones, matte black accents.',
            'paint': 0.7,
            'floor': 0.5,
            'cost_per_sqft': 60
        },
        'bedroom': {
            'suggestion': 'Warm and relaxing bedroom with soft lighting, oak floors, and calm paint tones.',
            'paint': 0.6,
            'floor': 0.4,
            'cost_per_sqft': 50
        }
    }

    room_data = suggestions.get(room_type.lower())
    if not room_data:
        return jsonify({'error': f'Room type "{room_type}" not recognized. Try kitchen, bathroom, living room, or bedroom.'}), 400

    return jsonify({
        'filename': filename,
        'room_type': room_type,
        'square_feet': sqft,
        'suggestion': room_data['suggestion'],
        'materials_needed': {
            'paint_gallons': round(sqft * room_data['paint'], 1),
            'flooring_boxes': round(sqft * room_data['floor'], 1)
        },
        'estimated_budget': round(sqft * room_data['cost_per_sqft'])
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
