import os
import sys
import time

try:
    import cv2
    from ultralytics import YOLO
except ImportError:
    print("[ERROR] OpenCV (cv2) or Ultralytics not installed.")
    sys.exit(1)

V2_MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../vision_models/experiments/grocery_yolov8_v2/weights/best.pt"))

def run_isolated_webcam_test():
    print("============================================================")
    print("   FRESHGUARD EXPERIMENTAL V2 WEBCAM CAMERA TEST SUITE     ")
    print("============================================================")

    if not os.path.exists(V2_MODEL_PATH):
        print(f"[ERROR] Experimental V2 model weights not found at: {V2_MODEL_PATH}")
        return "CAMERA_TEST_NOT_EXECUTED"

    print(f"[MODEL LOAD] Loading experimental V2 model from: {V2_MODEL_PATH}")
    model = YOLO(V2_MODEL_PATH)

    # Attempt to open default hardware webcam (index 0)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[STATUS] CAMERA_TEST_NOT_EXECUTED (No hardware webcam device detected in environment).")
        return "CAMERA_TEST_NOT_EXECUTED"

    print("[STATUS] Hardware webcam detected. Starting live vision inferencing stream...")
    print("Press 'q' in the camera window to exit.")

    frame_count = 0
    fps = 0.0

    while True:
        t0 = time.time()
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Failed to capture frame from webcam stream.")
            break

        frame_count += 1

        # Run experimental YOLOv8 v2 inference
        results = model.predict(frame, imgsz=640, conf=0.40, verbose=False)[0]

        # Draw bounding boxes and class labels
        detected_objects = len(results.boxes)
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            cls_name = model.names.get(cls_id, f"class_{cls_id}")

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label_text = f"{cls_name}: {conf:.2f}"
            cv2.putText(frame, label_text, (x1, max(y1 - 10, 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        t1 = time.time()
        fps = round(1.0 / max(t1 - t0, 0.001), 1)

        # Draw HUD overlays
        hud_text = f"FreshGuard V2 | Objects: {detected_objects} | FPS: {fps}"
        cv2.rectangle(frame, (0, 0), (640, 35), (20, 20, 20), -1)
        cv2.putText(frame, hud_text, (10, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

        cv2.imshow("FreshGuard AI — Experimental V2 Webcam Test", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[SUCCESS] Webcam test session closed cleanly.")
    return "CAMERA_TEST_SUCCESSFUL"

if __name__ == "__main__":
    status = run_isolated_webcam_test()
    print(f"Final Webcam Test Result: {status}")
