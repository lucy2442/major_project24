import cv2
import numpy as np
from sort import Sort

# Initialize SORT tracker
tracker = Sort()

# Pre-configured paths for the YOLO model and class names
yolo_weights_path = r"C:\Users\Ajay\OneDrive\Desktop\rough\andvace_cctv\major_project24\vehicle_project\app\yolov4\yolov4.weights"
yolo_config_path = r"C:\Users\Ajay\OneDrive\Desktop\rough\andvace_cctv\major_project24\vehicle_project\app\yolov4\yolov4.cfg"
yolo_class_names_path = r"C:\Users\Ajay\OneDrive\Desktop\rough\andvace_cctv\major_project24\vehicle_project\app\yolov4\coco.names"

# Video output path (fixed)
output_video_path = r"C:\Users\Ajay\OneDrive\Desktop\rough\andvace_cctv\major_project24\vehicle_project\app\output_video.avi"


# Load YOLO model
def load_yolo_model(weights_path, config_path, class_names_path):
    """Load YOLO model and return the model along with class names."""
    model = cv2.dnn.readNet(weights_path, config_path)
    model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    with open(class_names_path, "r") as f:
        classes = f.read().strip().split("\n")

    return model, classes


def detect_objects(frame, width, height, model, classes):
    """Run YOLO object detection on the frame."""
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (224, 224), (0, 0, 0), True, crop=False)
    model.setInput(blob)
    detections = model.forward(model.getUnconnectedOutLayersNames())

    boxes = []
    confidences = []
    class_ids = []

    for detection in detections:
        for obj in detection:
            scores = obj[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and classes[class_id] in ["car", "truck", "bus"]:
                center_x = int(obj[0] * width)
                center_y = int(obj[1] * height)
                w = int(obj[2] * width)
                h = int(obj[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(confidence)
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)
    detections_list = []
    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            detections_list.append([x, y, x + w, y + h, confidences[i]])

    return detections_list


def process_video(input_video_path):
    """Process video for vehicle detection and counting."""
    model, classes = load_yolo_model(yolo_weights_path, yolo_config_path, yolo_class_names_path)

    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {input_video_path}")
        return

    frame_count = 0
    vehicle_counter = 0
    vehicles_crossed = {}

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Define video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    line_y = 1000  # Y-coordinate of the counting line
    tilt_angle = -10  # Angle of the tilt in degrees
    frame_skip = 2  # Process every 2nd frame
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue  # Skip frames

        height, width, _ = frame.shape

        # Tilted line coordinates
        x1 = 0
        y1 = line_y
        x2 = width
        y2 = line_y + int(np.tan(np.deg2rad(tilt_angle)) * width)
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 6)  # Counting line

        # Object detection
        detections_list = detect_objects(frame, width, height, model, classes)

        # Update tracker
        tracked_objects = tracker.update(np.array(detections_list))

        for obj in tracked_objects:
            x1, y1, x2, y2, obj_id = map(int, obj)

            # Get the center of the object
            center_y = (y1 + y2) // 2

            if obj_id not in vehicles_crossed:
                vehicles_crossed[obj_id] = {'state': 'below', 'counted': False}

            if vehicles_crossed[obj_id]['state'] == 'below' and center_y > line_y and not vehicles_crossed[obj_id][
                'counted']:
                vehicle_counter += 1
                vehicles_crossed[obj_id]['state'] = 'crossed'
                vehicles_crossed[obj_id]['counted'] = True

            # Draw a rectangle around the vehicle
            color = (0, 255, 0) if vehicles_crossed[obj_id]['state'] == 'crossed' else (255, 0, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 6)
            cv2.putText(frame, f"ID: {obj_id}", (x1, y1 - 40), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)

        # Resize frame for display
        resized_frame = cv2.resize(frame, (800, 450))
        cv2.putText(resized_frame, f"Count: {vehicle_counter}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

        # Write the frame to the output video
        out.write(frame)

        # Display the frame
        cv2.imshow("Vehicle Tracking", resized_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Processed video saved to {output_video_path}")


# Example of using the function
if __name__ == "__main__":
    input_video_path = r"C:\Users\Ajay\OneDrive\Desktop\rough\andvace_cctv\major_project24\vehicle_project\app\two.mov"
    process_video(input_video_path)
