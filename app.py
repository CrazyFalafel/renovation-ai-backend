import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import torch
from torchvision import transforms

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Dummy room type classifier (replace with real model if needed)
room_labels = ['kitchen', 'bathroom', 'living_room', 'bedroom', 'garage', 'backyard', 'exterior']

def dummy_classify_room(image_path):
    # Replace this with actual model logic
    return 'living_room'

@app.route('/')
def home():
    return "Renovation AI API is running."

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    room_type = request.form.get('room_type', 'auto')
    sqft = float(request.form.get('square_footage', 0))

    if room_type == 'auto':
        room_type = dummy_classify_room(filepath)

    suggestion = generate_suggestion(room_type)
    paint_gallons = round(sqft / 350, 2)
    flooring_boxes = round(sqft / 20, 2)
    budget = calculate_budget(room_type, sqft)

    return jsonify({
        'filename': filename,
        'room_type': room_type,
        'square_footage': sqft,
        'suggestion': suggestion,
        'materials': {
            'paint_gallons': paint_gallons,
            'flooring_boxes': flooring_boxes
        },
        'estimated_budget': budget
    })

def generate_suggestion(room_type):
    suggestions = {
        'kitchen': "Modern white cabinets, quartz countertops, subway tile backsplash.",
        'bathroom': "Spa-inspired: light grey tiles, glass shower, floating vanity.",
        'living_room': "Scandinavian cozy: white oak flooring, neutral tones, matte black accents.",
        'bedroom': "Minimalist: beige palette, soft lighting, sleek closet system.",
        'garage': "Epoxy floors, wall-mounted storage, overhead racks.",
        'backyard': "Deck upgrade, pergola with lighting, garden beds.",
        'exterior': "New siding, black window trims, updated front door with modern lighting."
    }
    return suggestions.get(room_type.lower(), "Neutral design with timeless finishes.")

def calculate_budget(room_type, sqft):
    rates = {
        'kitchen': 90,
        'bathroom': 110,
        'living_room': 55,
        'bedroom': 45,
        'garage': 35,
        'backyard': 25,
        'exterior': 40
    }
    rate = rates.get(room_type.lower(), 50)
    return int(sqft * rate)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
