from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

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

    try:
        square_feet = float(request.form.get('square_feet', 0))
    except ValueError:
        return jsonify({'error': 'Invalid square footage'}), 400

    room_type = request.form.get('room_type', '').lower()

    if not square_feet or square_feet <= 0:
        return jsonify({'error': 'Missing or invalid square footage'}), 400

    suggestions = {
        'kitchen': {
            'suggestion': 'Modern Montreal kitchen: white cabinets, subway tiles, and butcher block counters.',
            'materials': {
                'paint_gallons': round(square_feet / 400, 1),
                'tiles_sqft': round(square_feet * 0.3, 1),
            },
            'estimated_cost': round(square_feet * 40, 2)
        },
        'bathroom': {
            'suggestion': 'Bright and clean look: ceramic tiles, waterproof paint, modern vanity.',
            'materials': {
                'paint_gallons': round(square_feet / 300, 1),
                'tiles_sqft': round(square_feet * 0.8, 1),
            },
            'estimated_cost': round(square_feet * 55, 2)
        },
        'living room': {
            'suggestion': 'Scandinavian cozy: white oak flooring, neutral tones, matte black accents.',
            'materials': {
                'paint_gallons': round(square_feet / 350, 1),
                'flooring_boxes': round(square_feet / 20, 1),
            },
            'estimated_cost': round(square_feet * 35, 2)
        },
        'bedroom': {
            'suggestion': 'Warm Montreal bedroom: off-white walls, light wood floor, blackout curtains.',
            'materials': {
                'paint_gallons': round(square_feet / 350, 1),
                'flooring_boxes': round(square_feet / 22, 1),
            },
            'estimated_cost': round(square_feet * 30, 2)
        }
    }

    if room_type not in suggestions:
        return jsonify({'error': f'Room type "{room_type}" not recognized. Try kitchen, bathroom, living room, or bedroom.'}), 400

    result = suggestions[room_type]

    return jsonify({
        'message': 'Image received',
        'filename': filename,
        'square_feet': square_feet,
        'room_type': room_type,
        'suggestion': result['suggestion'],
        'materials_needed': result['materials'],
        'estimated_cost': f"${result['estimated_cost']}"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
