from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os, json, uuid
from PIL import Image
import torch
import torchvision.transforms as transforms
from torchvision import models

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Load pretrained model
model = models.resnet18(pretrained=True)
model.eval()

# Mapping from image label to room type
imagenet_to_room = {
    'refrigerator': 'kitchen',
    'oven': 'kitchen',
    'bathtub': 'bathroom',
    'shower_curtain': 'bathroom',
    'sofa': 'living_room',
    'television': 'living_room',
    'bed': 'bedroom',
    'garage_door': 'garage',
    'patio': 'backyard',
    'mailbox': 'exterior'
}

# Room details
room_data = {
    "kitchen": {"suggestion": "Modern kitchen with white cabinets.", "paint": 0.003, "flooring": 0.04, "fixtures": 400},
    "bathroom": {"suggestion": "Spa-style bathroom with LED mirror.", "paint": 0.002, "flooring": 0.035, "fixtures": 500},
    "living_room": {"suggestion": "Cozy living room with oak floors.", "paint": 0.0028, "flooring": 0.05, "fixtures": 200},
    "bedroom": {"suggestion": "Warm bedroom with engineered wood.", "paint": 0.0025, "flooring": 0.04, "fixtures": 150},
    "basement": {"suggestion": "Finished basement with vinyl flooring.", "paint": 0.003, "flooring": 0.045, "fixtures": 300},
    "hallway": {"suggestion": "Simple hallway with tile.", "paint": 0.0018, "flooring": 0.02, "fixtures": 100},
    "dining_room": {"suggestion": "Elegant dining room.", "paint": 0.0025, "flooring": 0.04, "fixtures": 200},
    "garage": {"suggestion": "Garage with epoxy floor.", "paint": 0.0015, "flooring": 0.01, "fixtures": 300},
    "backyard": {"suggestion": "Deck with lighting and planters.", "paint": 0.0, "flooring": 0.01, "fixtures": 500},
    "exterior": {"suggestion": "Modern white/black exterior.", "paint": 0.002, "flooring": 0.01, "fixtures": 350}
}

def classify_room(path):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])
    img = Image.open(path).convert('RGB')
    tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        output = model(tensor)
    idx = torch.argmax(output).item()
    label_file = "imagenet_classes.txt"
    if not os.path.exists(label_file):
        import urllib.request
        urllib.request.urlretrieve(
            "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt",
            label_file)
    with open(label_file) as f:
        labels = [line.strip() for line in f.readlines()]
    label = labels[idx]
    return imagenet_to_room.get(label, "unknown")

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files or 'square_feet' not in request.form:
        return jsonify({'error': 'Missing data'}), 400

    file = request.files['file']
    sqft = float(request.form['square_feet'])
    room_type = request.form.get('room_type', 'auto')
    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    if room_type == 'auto':
        room_type = classify_room(path)

    if room_type not in room_data:
        return jsonify({'error': f'Unrecognized room type: {room_type}'}), 400

    room = room_data[room_type]
    paint = round(sqft * room['paint'], 1)
    floor = round(sqft * room['flooring'], 1)
    budget = round(paint * 45 + floor * 80 + room['fixtures'])

    result_id = str(uuid.uuid4())
    result = {
        "filename": filename,
        "room_type": room_type,
        "square_feet": sqft,
        "suggestion": room['suggestion'],
        "materials_needed": {"paint_gallons": paint, "flooring_boxes": floor},
        "estimated_budget": budget
    }
    with open(os.path.join(RESULTS_FOLDER, f"{result_id}.json"), 'w') as f:
        json.dump(result, f)

    return jsonify({"result_id": result_id, **result})

@app.route('/result/<rid>', methods=['GET'])
def view_result(rid):
    result_path = os.path.join(RESULTS_FOLDER, f"{rid}.json")
    if not os.path.exists(result_path):
        return jsonify({'error': 'Result not found'}), 404
    with open(result_path) as f:
        return jsonify(json.load(f))

if __name__ == '__main__':
    app.run(debug=True)
