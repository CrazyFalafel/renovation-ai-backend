from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Pricing per item based on Montreal averages
PRICES = {
    "paint_gallon": 45,
    "flooring_box": 90
}

# Room types with suggestions and basic cost multipliers
ROOM_DATABASE = {
    "kitchen": {
        "suggestion": "Modern minimalist with white cabinets and subway tile backsplash.",
        "paint_factor": 0.003,
        "flooring_factor": 0.045
    },
    "bathroom": {
        "suggestion": "Spa-inspired with light tiles, floating vanity, and LED mirrors.",
        "paint_factor": 0.002,
        "flooring_factor": 0.03
    },
    "bedroom": {
        "suggestion": "Warm tones with laminate flooring and built-in closet upgrades.",
        "paint_factor": 0.0028,
        "flooring_factor": 0.04
    },
    "living_room": {
        "suggestion": "Scandinavian cozy: white oak flooring, neutral tones, matte black accents.",
        "paint_factor": 0.0028,
        "flooring_factor": 0.05
    },
    "basement": {
        "suggestion": "Industrial-modern with polished concrete floors and soft LED lighting.",
        "paint_factor": 0.003,
        "flooring_factor": 0.035
    },
    "hallway": {
        "suggestion": "Functional with high-durability paint and ceramic tile.",
        "paint_factor": 0.0018,
        "flooring_factor": 0.02
    },
    "dining_room": {
        "suggestion": "Elegant setup with engineered hardwood and pendant lighting.",
        "paint_factor": 0.0025,
        "flooring_factor": 0.04
    },
    "garage": {
        "suggestion": "Epoxy-coated floor with wall storage systems.",
        "paint_factor": 0.0015,
        "flooring_factor": 0.01
    },
    "backyard": {
        "suggestion": "Add a deck, planter boxes, and soft LED string lighting.",
        "paint_factor": 0,
        "flooring_factor": 0.008
    },
    "exterior": {
        "suggestion": "Modern curb appeal with black trim, cedar siding, and paver walkway.",
        "paint_factor": 0.0025,
        "flooring_factor": 0.01
    }
}

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files or 'room_type' not in request.form:
        return jsonify({'error': 'Missing file or room type.'}), 400

    file = request.files['file']
    square_feet = float(request.form.get('square_feet', 0))
    room_type = request.form['room_type']

    if room_type not in ROOM_DATABASE:
        return jsonify({'error': f'Room type "{room_type}" not recognized. Try kitchen, bathroom, living room, or bedroom.'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    suggestion = ROOM_DATABASE[room_type]['suggestion']
    paint_factor = ROOM_DATABASE[room_type]['paint_factor']
    flooring_factor = ROOM_DATABASE[room_type]['flooring_factor']

    paint_gallons = round(square_feet * paint_factor, 1)
    flooring_boxes = round(square_feet * flooring_factor, 1)
    budget = round((paint_gallons * PRICES["paint_gallon"]) + (flooring_boxes * PRICES["flooring_box"]))

    return jsonify({
        "filename": file.filename,
        "square_feet": square_feet,
        "room_type": room_type,
        "suggestion": suggestion,
        "materials_needed": {
            "paint_gallons": paint_gallons,
            "flooring_boxes": flooring_boxes
        },
        "estimated_budget": budget
    })

if __name__ == '__main__':
    app.run(debug=True)
