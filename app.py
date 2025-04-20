from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Dummy room classification function
def classify_room_type(image_path):
    # Placeholder logic: randomly assign a room type or analyze filename
    filename = os.path.basename(image_path).lower()
    if "bath" in filename:
        return "bathroom"
    elif "kitchen" in filename:
        return "kitchen"
    elif "bed" in filename:
        return "bedroom"
    elif "garage" in filename:
        return "garage"
    elif "yard" in filename or "garden" in filename:
        return "backyard"
    elif "face" in filename or "exterior" in filename:
        return "exterior"
    elif "hall" in filename:
        return "hallway"
    elif "dining" in filename:
        return "dining_room"
    elif "base" in filename:
        return "basement"
    else:
        return "living_room"

# Suggestions and pricing data
room_data = {
    "living_room": {
        "suggestion": "Scandinavian cozy: white oak flooring, neutral tones, matte black accents.",
        "paint_per_sqft": 0.0028,
        "flooring_per_sqft": 0.05,
        "budget_per_sqft": 4.5
    },
    "kitchen": {
        "suggestion": "Modern kitchen: white cabinets, subway tiles, matte black faucet.",
        "paint_per_sqft": 0.0025,
        "flooring_per_sqft": 0.04,
        "budget_per_sqft": 6.0
    },
    "bathroom": {
        "suggestion": "Spa bathroom: ceramic tiles, floating vanity, LED mirrors.",
        "paint_per_sqft": 0.0020,
        "flooring_per_sqft": 0.03,
        "budget_per_sqft": 7.5
    },
    "bedroom": {
        "suggestion": "Warm and modern: neutral wall paint, engineered wood floor, soft lighting.",
        "paint_per_sqft": 0.0026,
        "flooring_per_sqft": 0.045,
        "budget_per_sqft": 4.0
    },
    "basement": {
        "suggestion": "Finished basement: luxury vinyl flooring, bright walls, pot lights.",
        "paint_per_sqft": 0.0028,
        "flooring_per_sqft": 0.05,
        "budget_per_sqft": 3.5
    },
    "hallway": {
        "suggestion": "Bright hallway: white walls, baseboard trim, accent light fixtures.",
        "paint_per_sqft": 0.0022,
        "flooring_per_sqft": 0.04,
        "budget_per_sqft": 3.0
    },
    "dining_room": {
        "suggestion": "Contemporary dining: wood floors, warm white paint, chandelier.",
        "paint_per_sqft": 0.0025,
        "flooring_per_sqft": 0.05,
        "budget_per_sqft": 5.0
    },
    "garage": {
        "suggestion": "Utility garage: epoxy floor, wall racks, LED panels.",
        "paint_per_sqft": 0.001,
        "flooring_per_sqft": 0.02,
        "budget_per_sqft": 2.5
    },
    "backyard": {
        "suggestion": "Landscaped backyard: pavers, grass patch, lighting.",
        "paint_per_sqft": 0,
        "flooring_per_sqft": 0.02,
        "budget_per_sqft": 8.0
    },
    "exterior": {
        "suggestion": "Modern curb appeal: dark siding, light trim, smart lighting.",
        "paint_per_sqft": 0.003,
        "flooring_per_sqft": 0,
        "budget_per_sqft": 9.0
    }
}

@app.route('/upload
