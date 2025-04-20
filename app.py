from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

room_suggestions = {
    "kitchen": "Modern white cabinets with quartz countertops and stainless steel appliances.",
    "bathroom": "Spa-like with neutral tiles, walk-in shower, and light wood accents.",
    "bedroom": "Warm tones, cozy lighting, and wood accents for a restful atmosphere.",
    "living_room": "Scandinavian cozy: white oak flooring, neutral tones, matte black accents.",
    "dining_room": "Contemporary space with pendant lighting, bold accent wall, hardwood floors.",
    "basement": "Industrial loft style with exposed ceiling beams and vinyl plank flooring.",
    "hallway": "Bright and minimal with mirror panels and LED base lighting.",
    "garage": "Epoxy floor coating, tool storage, and wall-mounted bike racks.",
    "garden": "Natural wood decking, stone pathway, and integrated lighting.",
    "exterior": "Modern facade with fiber cement siding, matte black fixtures, and wood soffits.",
    "auto": "Room type will be auto-detected soon — stay tuned!"
}

pricing = {
    "paint_per_gallon": 65,
    "flooring_per_box": 85,
    "fixture_cost_estimate": {
        "kitchen": 2500,
        "bathroom": 1800,
        "bedroom": 800,
        "living_room": 1000,
        "dining_room": 1200,
        "basement": 1500,
        "hallway": 500,
        "garage": 1000,
        "garden": 2000,
        "exterior": 3000
    }
}

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files or 'room_type' not in request.form:
        return jsonify({'error': 'Missing file or room_type'}), 400

    file = request.files['file']
    room_type = request.form['room_type'].lower()
    square_feet = float(request.form.get('square_feet', 0))

    if not file.filename:
        return jsonify({'error': 'No file selected'}), 400

    filename = file.filename
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)

    paint_gallons = round(square_feet / 350, 1)
    flooring_boxes = round(square_feet / 20, 1)

    suggestion = room_suggestions.get(room_type, "Design suggestion not available.")
    fixture_cost = pricing["fixture_cost_estimate"].get(room_type, 1000)

    budget = round(
        (paint_gallons * pricing["paint_per_gallon"]) +
        (flooring_boxes * pricing["flooring_per_box"]) +
        fixture_cost
    )

    return jsonify({
        'filename': filename,
        'room_type': room_type,
        'square_feet': square_feet,
        'suggestion': suggestion,
        'materials_needed': {
            'paint_gallons': paint_gallons,
            'flooring_boxes': flooring_boxes
        },
        'estimated_budget': f"${budget}"
    })

if __name__ == '__main__':
    app.run(debug=True)
