

# import cv2

# # Set up the video capture for the webcam
# cap = cv2.VideoCapture(0)  # Use 0 for webcam, or replace with video file path
# frameWidth = 640
# frameHeight = 480
# cap.set(3, frameWidth)      # Set frame width
# cap.set(4, frameHeight)     # Set frame height
# cap.set(10, 150)            # Set brightness

# # Load Haar Cascade Classifier for detecting number plates
# faceCascade = cv2.CascadeClassifier("Resourses/haarcascade_russian_plate_number.xml")

# while True:
#     # Capture video frame by frame
#     success, img = cap.read()
#     if not success:
#         print("Failed to capture image")
#         break

#     # Convert the captured frame to grayscale
#     imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Detect number plates in the frame
#     plates = faceCascade.detectMultiScale(imgGray, 1.1, 4)

#     # Draw rectangles around the detected number plates
#     for (x, y, w, h) in plates:
#         if w * h > 500:  # Filter out small detections
#             cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Blue rectangle for plate
#             imgR = img[y:y + h, x:x + w]  # Cropped region of interest
#             cv2.putText(img, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)

#             # Display the cropped number plate
#             cv2.imshow("Cropped Plate", imgR)

#     # Display the result frame
#     cv2.imshow("Result", img)

#     # Exit the loop when the 'q' key is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the video capture and close all OpenCV windows
# cap.release()
# cv2.destroyAllWindows()





# *********************************************




# import cv2
# import requests
# import time

# # API Details (Replace with actual API URL and key)
# # "https://rto-challan-basic-api.p.rapidapi.com/api/v1/challan-basic"
# API_URL = "https://rto-challan-basic-api.p.rapidapi.com/api/v2/challan-basic"
# API_KEY = "c396f9657fmsh67e74d4ebf1e5b4p18194fjsn709658ca389a"  # Replace with your API key

# # Function to fetch vehicle data from API
# def fetch_vehicle_data(number_plate):


#     try:
#         response = requests.get(
#             API_URL,
#             params={"plate": number_plate},
#             headers={"Authorization": f"Bearer {API_KEY}"}
#         )
#         if response.status_code == 200:
#             data = response.json()
#             return data
#         else:
#             return {"error": "Failed to fetch data from API"}
#     except Exception as e:
#         return {"error": str(e)}

# # Haar Cascade for number plate detection
# plate_cascade = cv2.CascadeClassifier("Resourses/haarcascade_russian_plate_number.xml")

# # Initialize webcam
# cap = cv2.VideoCapture(0)
# cap.set(3, 640)  # Frame width
# cap.set(4, 480)  # Frame height

# print("Real-Time Vehicle Monitoring System Started. Press 'q' to quit.")

# while True:
#     success, img = cap.read()
#     if not success:
#         print("Failed to capture video.")
#         break

#     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

#     for (x, y, w, h) in plates:
#         if w * h > 500:  # Filter out small detections
#             cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
#             number_plate = "MH12AB1234"  # Simulating detected plate for demo purposes
#             # Call the API to fetch vehicle data
#             vehicle_data = fetch_vehicle_data(number_plate)

#             # Display fetched data
#             if "error" not in vehicle_data:
#                 owner = vehicle_data.get("owner", "Unknown")
#                 pending_amount = vehicle_data.get("pending_amount", 0)
#                 violations = ", ".join(vehicle_data.get("violations", []))

#                 message = (
#                     f"Owner: {owner}\n"
#                     f"Pending Amount: ₹{pending_amount}\n"
#                     f"Violations: {violations}\n"
#                 )
#             else:
#                 message = f"Error: {vehicle_data['error']}"

#             print(message)
#             cv2.putText(img, number_plate, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#     # Show the result in real-time
#     cv2.imshow("Vehicle Monitoring", img)

#     # Exit on pressing 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Cleanup
# cap.release()
# cv2.destroyAllWindows()





# ************************************  api
# import cv2
# import requests
# import time

# # API Details

# API_URL = "https://api.attestr.com/api/v1/public/checkx/rc"  # Replace with the actual API URL
# API_KEY = "YOUR_ACTUAL_API_KEY_HERE"  # Replace with your API key

# # Function to fetch vehicle data from API
# def fetch_vehicle_data(number_plate):
#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "Content-Type": "application/json"
#     }
#     params = {"plate": number_plate}  # Adjust key if required by the API
    
#     try:
#         response = requests.get(API_URL, headers=headers, params=params)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             return {"error": f"API returned status code {response.status_code}: {response.text}"}
#     except Exception as e:
#         return {"error": str(e)}

# # Haar Cascade for number plate detection
# plate_cascade = cv2.CascadeClassifier("Resources/haarcascade_russian_plate_number.xml")

# # Initialize webcam
# cap = cv2.VideoCapture(0)
# cap.set(3, 640)  # Frame width
# cap.set(4, 480)  # Frame height

# print("Real-Time Vehicle Monitoring System Started. Press 'q' to quit.")

# while True:
#     success, img = cap.read()
#     if not success:
#         print("Failed to capture video.")
#         break

#     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

#     for (x, y, w, h) in plates:
#         if w * h > 500:  # Filter out small detections
#             cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
#             number_plate = "MH12AB1234"  # Replace with detected plate value
            
#             # Call the API to fetch vehicle data
#             vehicle_data = fetch_vehicle_data(number_plate)
            
#             # Display fetched data
#             if "error" not in vehicle_data:
#                 owner = vehicle_data.get("owner", "Unknown")
#                 pending_amount = vehicle_data.get("pending_amount", 0)
#                 violations = vehicle_data.get("violations", [])
#                 violations_text = ", ".join(violations) if violations else "None"

#                 message = (
#                     f"Owner: {owner}\n"
#                     f"Pending Amount: ₹{pending_amount}\n"
#                     f"Violations: {violations_text}\n"
#                 )
#             else:
#                 message = f"Error: {vehicle_data['error']}"

#             print(message)
#             cv2.putText(img, message, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#             time.sleep(1)  # Prevent rapid API calls

#     # Show the result in real-time
#     cv2.imshow("Vehicle Monitoring", img)

#     # Exit on pressing 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Cleanup
# cap.release()
# cv2.destroyAllWindows()


# ****************************All merge code
#C:\Program Files\Tesseract-OCR

import cv2
import json
import pytesseract
import time
import os

# Path to Tesseract executable (adjust for your setup)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
    print("Error: Tesseract executable not found at the specified path.")
    exit()

    

# Load data from data.json
def fetch_vehicle_data(number_plate):
    try:
        # Check if the file exists
        if not os.path.exists("data.json"):
            return {"error": "data.json file not found"}

        # Load data from JSON file
        with open("data.json", "r") as file:
            data = json.load(file)

        # Return data for the given number plate
        print(f"Detected Number Plate: {number_plate}")
        return data.get(number_plate, {"error": "Number plate not found"})
    except json.JSONDecodeError as e:
        return {"error": f"JSON format error: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}

# Load Haar Cascades
plate_cascade = cv2.CascadeClassifier("Resourses/haarcascade_russian_plate_number.xml")

# Verify cascade loading
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

# Signal line position
signal_line_y = 400  # Adjust this according to your setup

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture video.")
        break

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect number plates
    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)
    for (x, y, w, h) in plates:
        if w * h > 500:  # Filter out small detections
            # Draw rectangle around the detected plate
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Crop the detected plate area
            plate_img = img[y:y + h, x:x + w]

            # Check if the cropped image is valid
            if plate_img is None or plate_img.size == 0:
                print("Error: Cropped image is invalid or empty.")
                continue

            # Save cropped image for debugging (optional)
            cv2.imwrite("debug_plate_img.png", plate_img)

            # Convert the cropped image to grayscale before passing to Tesseract
            plate_img_gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)

            # Perform OCR on the cropped image
            try:
                detected_plate = pytesseract.image_to_string(
                    plate_img_gray,
                    config="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                ).strip()

                # Filter OCR output (remove unwanted characters)
                detected_plate = "".join(char for char in detected_plate if char.isalnum())
            except Exception as e:
                print(f"OCR Error: {str(e)}")
                detected_plate = None

            # Fetch vehicle data using the detected plate
            if detected_plate:
                vehicle_data = fetch_vehicle_data(detected_plate)

                # Display fetched data
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

            # Print and display the message
            print(message)
            cv2.putText(img, message, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            time.sleep(1)  # Prevent rapid updates

    # Draw the signal line for visualization
    cv2.line(img, (0, signal_line_y), (640, signal_line_y), (0, 255, 255), 2)

    # Show the result in real-time
    cv2.imshow("Vehicle Monitoring", img)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
