from multiprocessing import Queue
import cv2
from datetime import datetime


def presenter_process(input_queue: Queue) -> None:
    while True:
        item = input_queue.get()
        if item is None:
            print("[Presenter] Shutdown signal received.")
            break

        frame, detections = item

        # Draw detections
        for (bbox, _) in detections:
            x, y, w, h = bbox
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Draw timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        # Show frame
        cv2.imshow("Presenter", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    print("[Presenter] Finished displaying.")