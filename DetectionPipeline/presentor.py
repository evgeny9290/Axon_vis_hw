from multiprocessing import Queue
import cv2
from datetime import datetime


def presenter_process(detections_input_queue: Queue) -> None:
    while True:
        item = detections_input_queue.get()
        if item is None:
            break

        frame, detections = item
        blurred = cv2.GaussianBlur(frame, (21, 21), 0)
        res = frame.copy()

        # Draw detections
        for (bbox, _) in detections:
            x, y, w, h = bbox
            res[y:y + h, x: x + w] = blurred[y:y + h, x: x + w]
            cv2.rectangle(res, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Draw timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        cv2.putText(res, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        # Show frame
        cv2.imshow("Presenter", res)
        if cv2.waitKey(1) != -1:
            break

    cv2.destroyAllWindows()