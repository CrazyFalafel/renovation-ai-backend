import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image

app = Flask(__name__)
CORS(app)

def generate_suggestions(room_type, square_feet):
    # Realistic suggestions and cost estimates based on room type
    suggestions = {
        "kitchen": {
            "style": "Modern white with subway tiles and open shelves.",
            "paint_gallons": round(square_feet / 350, 1),
            "flooring_boxes": round(square_feet / 20, 1),
            "base_cost": 1400
        },
        "bathroom": {
            "style": "Minimalist: ceramic tiles, light gray walls, matte fixtures.",
            "paint_gallons": round(square_feet / 400, 1),
            "flooring_boxes": round(square_feet / 25, 1),
            "base_cost": 1000
        },
        "living_room": {
            "style": "Scandinavian cozy: white oak flooring, neutral tones, matte black accents.",
            "paint_gallons": round(square_feet / 360, 1),
            "flooring_boxes": round(square_feet / 20, 1),
            "base_cost": 1100
        },
        "bedroom": {
            "style": "Calm tones: greige walls, vinyl plank floors, minimal decor.",
            "paint_gallons": round(square_feet / 370, 1),
            "flooring_boxes": round(square_feet / 22, 1),
            "base_cost": 950
        },
        "basement": {
            "style": "Durable rustic: waterproof vinyl, white walls, recessed lighting.",
            "paint_gallons": round(square_feet / 360, 1),
            "flooring_boxes": round(square_feet / 18, 1),
            "base_cost": 1200
        },
        "dining_room": {
            "style": "Elegant: crown molding, herringbone floors, warm neutrals.",
            "paint_gallons": round(square_feet / 340, 1),
            "flooring_boxes": round(square_feet / 20, 1),
            "base_cost": 1300
        },
        "hallway": {
            "style": "Clean modern: white walls, darker wood floors, accent lighting.",
            "paint_gallons": round(square_feet / 400, 1),
            "flooring_boxes": round(square_feet / 22, 1),
            "base_cost": 600
        },
        "garage": {
            "style": "Utility-focused: epoxy floors, durable white paint.",
            "paint_gallons": round(square_feet / 300, 1),
            "flooring_boxes": 0,
            "base_cost": 700
        },
        "garden": {
            "style": "Functional greenery: paving stones, raised planters.",
            "paint_gallons": 0,
            "flooring_boxes": round(square_feet / 30, 1),
            "base_cost": 850
        },
        "facade": {
            "style": "Curb appeal: fresh siding/paint, black trim, clean lines.",
            "paint_gallons": round(square_feet / 250, 1),
            "flooring_boxes": 0,
            "base_cost": 2000
        }
    }

    if room_type not in suggestions:
        return None

    s = suggestions[room_type]
    budget = s["base_cost"] + (s["paint_gallons"] * 60) + (s["flooring_boxes"] * 55)

    return {
        "suggestion": s["style"],
        "materials_needed": {
            "paint_gallons": s["paint_gallons"],
            "flooring_boxes": s["flooring_boxes"]
        },
        "estimated_budget": f"${round(budget)}"
    }

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files or 'room_type' not in request.form:
        return jsonify({'error': 'Missing file or room type'}), 400

    file = request.files['file']
    room_type = request.form['room_type'].lower().replace(" ", "_")
    square_feet = int(request.form.get('square_feet', 0))

    suggestion = generate_suggestions(room_type, square_feet)
    if not suggestion:
        return jsonify({'error': f'Room type \"{room_type}\" not recognized.'}), 400

    return jsonify({
        'filename': file.filename,
        'room_type': room_type,
        'square_feet': square_feet,
        **suggestion
    })

# Run with proper host and port binding for Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
