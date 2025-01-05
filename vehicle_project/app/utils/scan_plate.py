import cv2
import pytesseract
import json
import time
import os

# Path to Tesseract executable (adjust for macOS)
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"  # Adjust if installed elsewhere

def fetch_vehicle_data(number_plate):
    try:
        if not os.path.exists("data.json"):
            return {"error": "data.json file not found"}

        with open("data.json", "r") as file:
            data = json.load(file)

        return data.get(number_plate, {"error": "Number plate not found"})
    except json.JSONDecodeError as e:
        return {"error": f"JSON format error: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}

def process_uploaded_image(image_path):
    plate_cascade = cv2.CascadeClassifier("vehicle_project/app/haarcascade_russian_plate_number.xml")

    if plate_cascade.empty():
        return "Error: Could not load number plate cascade."

    img = cv2.imread(image_path)
    if img is None:
        return "Error: Could not read the image."

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    if len(plates) == 0:
        return "No plates detected in the image."

    for (x, y, w, h) in plates:
        if w * h > 500:
            plate_img = img[y:y + h, x:x + w]
            plate_img_gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)

            detected_plate = pytesseract.image_to_string(
                plate_img_gray,
                config="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            ).strip()

            detected_plate = "".join(char for char in detected_plate if char.isalnum())
            if detected_plate:
                vehicle_data = fetch_vehicle_data(detected_plate)
                if "error" not in vehicle_data:
                    owner = vehicle_data.get("owner", "Unknown")
                    pending_amount = vehicle_data.get("pending_amount", 0)
                    violations = vehicle_data.get("violations", [])
                    violations_text = ", ".join(violations) if violations else "None"
                    return f"Owner: {owner}\nPending Amount: {pending_amount}\nViolations: {violations_text}"
                else:
                    return vehicle_data["error"]
            else:
                return "No valid number plate detected or OCR failed."

    return "No plates detected."

def process_webcam_feed():
    plate_cascade = cv2.CascadeClassifier("vehicle_project/app/haarcascade_russian_plate_number.xml")

    if plate_cascade.empty():
        return "Error: Could not load number plate cascade."

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Error: Could not open webcam."

    cap.set(3, 640)  # Frame width
    cap.set(4, 480)  # Frame height

    while True:
        success, img = cap.read()
        if not success:
            return "Failed to capture video."

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

        for (x, y, w, h) in plates:
            if w * h > 500:
                plate_img = img[y:y + h, x:x + w]
                plate_img_gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)

                detected_plate = pytesseract.image_to_string(
                    plate_img_gray,
                    config="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                ).strip()

                detected_plate = "".join(char for char in detected_plate if char.isalnum())
                if detected_plate:
                    vehicle_data = fetch_vehicle_data(detected_plate)
                    if "error" not in vehicle_data:
                        owner = vehicle_data.get("owner", "Unknown")
                        pending_amount = vehicle_data.get("pending_amount", 0)
                        violations = vehicle_data.get("violations", [])
                        violations_text = ", ".join(violations) if violations else "None"
                        message = f"Owner: {owner}\nPending Amount: {pending_amount}\nViolations: {violations_text}"
                    else:
                        message = vehicle_data["error"]
                else:
                    message = "No valid number plate detected or OCR failed."
                return message

    cap.release()
    return "Webcam feed stopped."
