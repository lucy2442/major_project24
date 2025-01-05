import cv2
import json
import pytesseract
import time
import os

# Path to Tesseract executable (adjust for macOS)
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"  # Adjust if installed elsewhere

if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
    print("Error: Tesseract executable not found at the specified path.")
    exit()

# Load data from data.json
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

# Load Haar Cascades
plate_cascade = cv2.CascadeClassifier("Resourses/haarcascade_russian_plate_number.xml")
if plate_cascade.empty():
    print("Error: Could not load number plate cascade. Check file path.")
    exit()

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

cap.set(3, 640)  # Frame width
cap.set(4, 480)  # Frame height

print("Real-Time Vehicle Monitoring System Started. Press 'q' to quit.")

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture video.")
        break

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)
    for (x, y, w, h) in plates:
        if w * h > 500:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            plate_img = img[y:y + h, x:x + w]

            if plate_img is None or plate_img.size == 0:
                continue

            plate_img_gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)

            try:
                detected_plate = pytesseract.image_to_string(
                    plate_img_gray,
                    config="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                ).strip()
                detected_plate = "".join(char for char in detected_plate if char.isalnum())
            except Exception as e:
                detected_plate = None

            if detected_plate:
                vehicle_data = fetch_vehicle_data(detected_plate)
                if "error" not in vehicle_data:
                    owner = vehicle_data.get("owner", "Unknown")
                    pending_amount = vehicle_data.get("pending_amount", 0)
                    violations = vehicle_data.get("violations", [])
                    violations_text = ", ".join(violations) if violations else "None"

                    message = (
                        f"Owner: {owner}\n"
                        f"Pending Amount: {pending_amount}\n"
                        f"Violations: {violations_text}"
                    )
                else:
                    message = f"Error: {vehicle_data['error']}"
            else:
                message = "Error: No valid number plate detected or OCR failed."

            print(message)
            cv2.putText(img, message, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("Vehicle Monitoring", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
