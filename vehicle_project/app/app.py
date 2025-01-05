from flask import Flask, render_template, request, jsonify
import os
import pytesseract
from werkzeug.utils import secure_filename
from utils.scan_plate import fetch_vehicle_data, process_uploaded_image, process_webcam_feed

app = Flask(__name__)

# Configure the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"  # Adjust path as needed

# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    # Render the main page
    return render_template('index.html')

@app.route('/scan')
def scan():
    # Render the scan page
    return render_template('scan.html')

@app.route('/scan-image', methods=['POST'])
def scan_image():
    # Handle the uploaded image for scanning the number plate
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the uploaded image
        message = process_uploaded_image(file_path)

        return jsonify({"message": message}), 200

    return jsonify({"error": "Invalid file type. Allowed types: .png, .jpg, .jpeg"}), 400

@app.route('/scan-webcam', methods=['GET'])
def scan_webcam():
    # Start the webcam feed for number plate detection
    message = process_webcam_feed()
    return jsonify({"message": message}), 200
@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    # Save image and process (you can call the existing function for image processing)
    image_path = os.path.join('uploads', file.filename)
    file.save(image_path)

    # Process the image and return response
    message = process_uploaded_image(image_path)  # Your function here
    return jsonify({"message": message})

@app.route('/process_webcam_feed', methods=['POST'])
def process_webcam_feed():
    if 'webcam_image' not in request.files:
        return jsonify({"message": "No webcam image"}), 400

    file = request.files['webcam_image']
    image_path = os.path.join('uploads', 'webcam_image.jpg')
    file.save(image_path)

    # Process the webcam feed and return response
    message = process_uploaded_image(image_path)  # Your function here
    return jsonify({"message": message})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)
