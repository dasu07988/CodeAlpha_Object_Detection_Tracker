import time
from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

prev_time = 0

cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    if not success:
        break

    results = model.track(
        frame,
        persist=True
    )

    object_count = len(results[0].boxes)

    annotated_frame = results[0].plot()

    current_time = time.time()

    fps = 1 / (current_time - prev_time) if current_time != prev_time else 0

    prev_time = current_time

    cv2.putText(
        annotated_frame,
        f"FPS: {int(fps)}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Objects: {object_count}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )

    cv2.imshow(
        "CodeAlpha Object Detection & Tracking",
        annotated_frame
    )

    key = cv2.waitKey(1)

    if key == ord("s"):

        filename = f"screenshots/detection_{int(time.time())}.jpg"

        cv2.imwrite(filename, annotated_frame)

        print(f"Saved: {filename}")

    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
