from flask import Flask, render_template, request, jsonify,redirect, url_for, flash, session
import os
import cv2
import pytesseract
import json
import sqlite3
import base64
import numpy as np
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"  # Adjust path as needed
# Path to Haar Cascade
plate_cascade_path = "/Users/rohit12300/PycharmProjects/major_project24/vehicle_project/app/haarcascade_russian_plate_number.xml"
plate_cascade = cv2.CascadeClassifier(plate_cascade_path)
if plate_cascade.empty():
    raise Exception("Error: Could not load Haar Cascade. Check the file path.")

# Configure the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('login.html')
@app.route("/home_index")
def index():
    return render_template('index.html')
from werkzeug.security import check_password_hash

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check credentials
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the password for security
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            # Store user in the database
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            conn.close()

            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists. Please choose a different username.', 'danger')

    return render_template('signup.html')






# Function to fetch vehicle data from a JSON file
def fetch_vehicle_data(number_plate):
    data_file = "/Users/rohit12300/PycharmProjects/major_project24/vehicle_project/app/data.json"
    if not os.path.exists(data_file):
        return {"error": "data.json file not found"}
    try:
        with open(data_file, "r") as file:
            data = json.load(file)

        # Check if the plate exists in data, return the corresponding data if present
        if number_plate in data:
            return data[number_plate]
        else:
            return {"error": "Number plate not found in data."}
    except Exception as e:
        return {"error": str(e)}


# Function to process the frame for plate detection
def process_frame(frame):
    try:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        plates = plate_cascade.detectMultiScale(gray_frame, 1.1, 4)

        for (x, y, w, h) in plates:
            if w * h > 500:
                plate_img = frame[y:y + h, x:x + w]
                plate_text = pytesseract.image_to_string(
                    plate_img,
                    config="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                ).strip()
                plate_text = "".join(char for char in plate_text if char.isalnum())

                if plate_text:
                    # Fetch the data only if the plate exists in data.json
                    vehicle_data = fetch_vehicle_data(plate_text)

                    # If data is found, return it, else return an error message
                    if "error" not in vehicle_data:
                        return {"plate": plate_text, **vehicle_data}
                    else:
                        return {"error": vehicle_data["error"]}

        return {"error": "No plate detected"}
    except Exception as e:
        return {"error": str(e)}





@app.route('/violations')
def violations():
    return render_template('voilation.html')
@app.route('/home_reports')
def home_reports():
    return render_template('report.html')
@app.route('/home_profile')
def home_profile():
    return render_template('profile.html')
@app.route('/scan')
def scan():
    # Render the scan page with an active button based on selection (optional)
    scan_type = request.args.get('scan_type')  # Get scan type from query string (optional)
    active_button = 'upload' if scan_type == 'upload' else 'webcam'  # Set active button (optional)
    return render_template('scan.html', active_button=active_button)  # Pass active button data (optional)


@app.route('/process-frame', methods=['POST'])
def process_frame_endpoint():
    try:
        data = request.json
        frame_data = data.get("frame")
        if not frame_data:
            return jsonify({"success": False, "error": "No frame data provided."})

        # Decode the base64 frame
        _, frame_str = frame_data.split(",", 1)
        frame_bytes = base64.b64decode(frame_str)
        nparr = np.frombuffer(frame_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Process the frame
        result = process_frame(frame)
        if "error" not in result:
            return jsonify({"success": True, **result})
        else:
            return jsonify({"success": False, "error": result["error"]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


# Load the JSON data
def load_challans_data():
    with open('data/challans.json') as f:
        return json.load(f)


@app.route('/check_challans', methods=['POST'])
def check_challans():
    # Log vehicle number
    print(f"Request Form: {request.form}")

    if 'vehicle_number' not in request.form:
        return jsonify({'error': 'Vehicle number is missing'}), 400

    vehicle_number = request.form['vehicle_number']

    # Simulate checking challans
    with open('/Users/rohit12300/PycharmProjects/major_project24/data1.json') as f:
        data = json.load(f)

    if vehicle_number in data:
        vehicle_info = data[vehicle_number]
        response = {
            'status': 'success',
            'data': {
                'vehicle_number': vehicle_number,
                'owner': vehicle_info['owner'],
                'pending_amount': vehicle_info['pending_amount'],
                'violations': vehicle_info['violations']
            }
        }
    else:
        response = {'status': 'error', 'data': 'Vehicle number not found.'}

    # Log response
    print(f"Response: {response}")
    return jsonify(response)
@app.route('/detect_triple_seat', methods=['POST'])
def detect_triple_seat():
    # Simulate detection (you should replace this with actual image processing)
    vehicle_image = request.files.get('vehicleImage')
    if vehicle_image:
        # Simulate random result
        result = "Triple seat violation detected!" if random.random() > 0.5 else "No triple seat violation detected."
        return jsonify({"result": result})
    return jsonify({"error": "No image provided"}), 400


# Route to handle red line violation detection
@app.route('/detect_red_line', methods=['POST'])
def detect_red_line():
    # Simulate detection (you should replace this with actual image processing)
    red_line_image = request.files.get('redLineImage')
    if red_line_image:
        # Simulate random result
        result = "Red line violation detected!" if random.random() > 0.5 else "No red line violation detected."
        return jsonify({"result": result})
    return jsonify({"error": "No image provided"}), 400



if __name__ == '__main__':
    app.run(debug=True)
