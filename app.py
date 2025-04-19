from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
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
            {
                'item': 'White Oak Vinyl Planks',
                'link': 'https://www.homedepot.ca/product/home-decorators-collection-7-5-inch-w-x-47-6-inch-l-walnut-luxury-vinyl-plank-flooring-24-74-sq-ft-case-/1001102516'
            },
            {
                'item': 'Matte Black Faucet',
                'link': 'https://www.rona.ca/en/product/project-source-matte-black-single-handle-bathroom-sink-faucet-4-in-centreset-85516028'
            },
            {
                'item': 'Ultra Pure White Paint',
                'link': 'https://www.homedepot.ca/product/behr-ultra-pure-white-paint-interior-eggshell-enamel-3-79l/1001111900'
            }
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
