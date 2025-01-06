import cv2
import pytesseract
import json
import os

# Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# Path to Haar Cascade
plate_cascade_path = "/Users/rohit12300/PycharmProjects/major_project24/vehicle_project/app/haarcascade_russian_plate_number.xml"

plate_cascade = cv2.CascadeClassifier(plate_cascade_path)

if plate_cascade.empty():
    raise Exception("Error: Could not load Haar Cascade. Check the file path.")

def fetch_vehicle_data(number_plate):
    data_file = "/Users/rohit12300/PycharmProjects/major_project24/vehicle_project/app/data.json"
    if not os.path.exists(data_file):
        return {"error": "data.json file not found"}
    try:
        with open(data_file, "r") as file:
            data = json.load(file)
        return data.get(number_plate, {"error": "Number plate not found"})
    except Exception as e:
        return {"error": str(e)}

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
                    vehicle_data = fetch_vehicle_data(plate_text)
                    return {"plate": plate_text, **vehicle_data}
        return {"error": "No plate detected"}
    except Exception as e:
        return {"error": str(e)}
