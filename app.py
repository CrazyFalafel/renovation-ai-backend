from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # 👈 This allows cross-origin requests (like from Netlify)

UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    square_feet = request.form.get('square_feet')
    if not square_feet:
        return jsonify({'error': 'Missing square footage'}), 400

    return jsonify({
        'message': 'Image received',
        'filename': filename,
        'square_feet': square_feet,
        'suggestion': 'Modern Scandinavian look with white oak flooring and matte black fixtures.',
        'materials_needed': {
            'paint_gallons': round(float(square_feet) / 350, 1),
            'flooring_boxes': round(float(square_feet) / 20, 1),
        },
        'products': [
            {'item': 'White Oak Vinyl Planks', 'link': 'https://www.homedepot.ca'},
            {'item': 'Matte Black Faucet', 'link': 'https://www.rona.ca'},
            {'item': 'Ultra Pure White Paint', 'link': 'https://www.homedepot.ca'}
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
