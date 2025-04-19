from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_room_suggestion(room_type, square_feet):
    sqf = float(square_feet)
    suggestion = ""
    paint_gallons = round(sqf / 350, 1)
    flooring_boxes = round(sqf / 20, 1)

    # Price estimates
    paint_cost = paint_gallons * 60   # average $60 per gallon in Quebec
    flooring_cost = flooring_boxes * 50  # average $50 per box
    misc_cost = 300  # general fixtures, small upgrades
    total_budget = round(paint_cost + flooring_cost + misc_cost)

    if room_type == "living room":
        suggestion = "Use warm neutral tones, white oak or maple flooring, and consider soft LED ceiling lighting."
    elif room_type == "kitchen":
        suggestion = "Consider white shaker cabinets, subway tile backsplash, and light grey quartz counters with matte black handles."
        misc_cost = 1500  # kitchens have appliances/fixtures
    elif room_type == "bathroom":
        suggestion = "Opt for ceramic wall tiles, floating vanity, matte black faucet, and a light grey or powder blue paint."
        misc_cost = 1000
    elif room_type == "bedroom":
        suggestion = "Soft beige or light grey paint, laminate flooring, and simple lighting fixtures with warm ambiance."
    elif room_type == "basement":
        suggestion = "Use vinyl plank flooring, moisture-resistant paint, and drop ceiling tiles for easy access."
        misc_cost = 800
    else:
        suggestion = "Modern finish with paint, flooring, and minimal decor."
    
    total_budget = round(paint_cost + flooring_cost + misc_cost)

    return {
        "suggestion": suggestion,
        "materials_needed": {
            "paint_gallons": paint_gallons,
            "flooring_boxes": flooring_boxes
        },
        "budget_estimate": f"${total_budget} CAD (estimated)"
    }

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'room_type' not in request.form_
