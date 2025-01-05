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
    # Render the scan page with an active button based on selection (optional)
    scan_type = request.args.get('scan_type')  # Get scan type from query string (optional)
    active_button = 'upload' if scan_type == 'upload' else 'webcam'  # Set active button (optional)
    return render_template('scan.html', active_button=active_button)  # Pass active button data (optional)


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

        # Display the message on the scan.html page (you might need to modify scan.html)
        return render_template('scan.html', scan_result=message)

    return jsonify({"error": "Invalid file type. Allowed types: .png, .jpg, .jpeg"}), 400


@app.route('/scan-webcam', methods=['GET'])
def scan_webcam():
    # Start the webcam feed for number plate detection
    message = process_webcam_feed()

    # Display the message on the scan.html page (you might need to modify scan.html)
    return render_template('scan.html', scan_result=message)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)