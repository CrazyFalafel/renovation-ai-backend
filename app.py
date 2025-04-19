from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ROOM_DATA = {
    "living_room": {
        "suggestion": "Scandinavian cozy: white oak flooring, neutral tones, matte black accents.",
        "paint_per_sqft": 0.0028,
        "flooring_per_sqft": 0.05,
        "paint_cost": 60,
        "flooring_cost": 3.5
    },
    "kitchen": {
        "suggestion": "Modern clean: ceramic backsplash, quartz countertops, light grey tones.",
        "paint_per_sqft": 0.0025,
        "flooring_per_sqft": 0.04,
        "paint_cost": 65,
        "flooring_cost": 4.5
    },
    "bathroom": {
        "suggestion": "Spa style: large tiles, floating vanity, LED mirror.",
        "paint_per_sqft": 0.0015,
        "flooring_per_sqft": 0.03,
        "paint_cost": 70,
        "flooring_cost": 5.5
    },
    "bedroom": {
        "suggestion": "Soft minimal: warm tones, wide plank laminate, soft lighting.",
        "paint_per_sqft": 0.0025,
        "flooring_per_sqft": 0.045,
        "paint_cost": 60,
        "flooring_cost": 3.2
    },
    "basement": {
        "suggestion": "Cozy + practical: vinyl plank flooring, recessed lighting, drycore subfloor.",
        "paint_per_sqft": 0.0028,
        "flooring_per_sqft": 0.06,
        "paint_cost": 55,
        "flooring_cost": 2.8
    },
    "hallway": {
        "suggestion": "Bright + functional: runner flooring, entry accent wall, large mirror.",
        "paint_per_sqft": 0.0018,
        "flooring_per_sqft": 0.04,
        "paint_cost": 60,
        "flooring_cost": 3.0
    },
    "dining_room": {
        "suggestion": "Elegant: bold wall color, modern chandelier, herringbone floors.",
        "paint_per_sqft": 0.003,
        "flooring_per_sqft": 0.06,
        "paint_cost": 70,
        "flooring_cost": 4.0
    },
    "garage": {
        "suggestion": "Clean utility: epoxy flooring, heavy-duty shelves, white walls.",
        "paint_per_sqft": 0.002,
        "flooring_per_sqft": 0.07,
        "paint_cost": 50,
        "flooring_cost": 5.0
    },
    "garden": {
        "suggestion": "Natural: patio pavers, grass, garden border lights.",
        "paint_per_sqft": 0,
        "flooring_per_sqft": 0.09,
        "paint_cost": 0,
        "flooring_cost": 6.5
    },
    "exterior": {
        "suggestion": "Modern curb appeal: deep tones, black trim, updated porch lights.",
        "paint_per_sqft": 0.0018,
        "flooring_per_sqft": 0,
        "paint_cost": 80,
        "flooring_cost": 0
    },
}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'room_type' not in request.form:
        return jsonify({'error': 'Missing file or room_type'}), 400

    file = request.files['file']
    square_feet = request.form.get('square_feet')
    room_type = request.form.get('room_type').lower()

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not square_feet or not room_type:
        return jsonify({'error': 'Missing square footage or room type'}), 400
    if room_type not in ROOM_DATA:
        return jsonify({'error': f'Room type \"{room_type}\" not recognized. Try kitchen, bathroom, living room, or bedroom.'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    sqft = float(square_feet)
    data = ROOM_DATA[room_type]

    paint_gal = round(sqft * data['paint_per_sqft'], 1)
    flooring_boxes = round(sqft * data['flooring_per_sqft'], 1)

    budget = round(paint_gal * data['paint_cost'] + flooring_boxes * data['flooring_cost'])

    return jsonify({
        'filename': filename,
        'room_type': room_type,
        'square_feet': sqft,
        'suggestion': data['suggestion'],
        'materials_needed': {
            'paint_gallons': paint_gal,
            'flooring_boxes': flooring_boxes
        },
        'budget': budget
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
