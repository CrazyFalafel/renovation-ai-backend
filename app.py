from flask import Flask, request, jsonify, render_template
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_room_type(file_path):
    # Simulated room detection - replace with actual ML model if needed
    filename = os.path.basename(file_path).lower()
    if "bath" in filename:
        return "bathroom"
    elif "kitchen" in filename:
        return "kitchen"
    elif "bed" in filename:
        return "bedroom"
    elif "living" in filename:
        return "living_room"
    elif "garage" in filename:
        return "garage"
    elif "yard" in filename:
        return "backyard"
    elif "exterior" in filename:
        return "exterior"
    else:
        return "living_room"  # default

def generate_suggestions(room_type, sqft):
    suggestions = {
        'bathroom': ["Install new tiles", "Replace vanity", "Add LED mirror"],
        'kitchen': ["Upgrade cabinets", "Install backsplash", "New countertop"],
        'bedroom': ["Add accent wall", "Install dimmable lights", "Closet organizer"],
        'living_room': ["Open concept layout", "New paint color", "Modern light fixtures"],
        'garage': ["Epoxy flooring", "Storage wall system", "LED strip lighting"],
        'backyard': ["Deck upgrade", "Add garden boxes", "Outdoor lighting"],
        'exterior': ["Replace siding", "Add stone veneer", "Upgrade front door"],
    }
    return suggestions.get(room_type, ["Update flooring", "Neutral color palette", "Modern light fixtures"])

def estimate_budget(room_type, sqft):
    rates = {
        'bathroom': 110,
        'kitchen': 130,
        'bedroom': 45,
        'living_room': 55,
        'garage': 35,
        'backyard': 25,
        'exterior': 40
    }
    rate = rates.get(room_type.lower(), 50)
    return int(sqft * rate)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    sqft = int(request.form.get('sqft', 200))
    room_type = request.form.get('room_type', '')
    theme = request.form.get('theme', '')

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    if room_type == 'auto':
        room_type = detect_room_type(file_path)

    suggestions = generate_suggestions(room_type, sqft)
    budget = estimate_budget(room_type, sqft)

    return render_template('result.html',
                           room_type=room_type,
                           sqft=sqft,
                           suggestions=suggestions,
                           budget=budget,
                           theme=theme)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
