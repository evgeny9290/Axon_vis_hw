from multiprocessing import Queue
from typing import Tuple, List
import cv2
import imutils

BBox = Tuple[int, int, int, int]
Detection = Tuple[BBox, cv2.Mat]


class Detector:
    def __init__(self, min_area: int = 500):
        self.first_frame = None
        self.min_area = min_area

    def detect(self, frame: cv2.Mat) -> Tuple[cv2.Mat, List[Detection]]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.first_frame is None:
            self.first_frame = gray
            return frame, []

        frame_delta = cv2.absdiff(self.first_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        dilated = cv2.dilate(thresh, None, iterations=2)

        cnts = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        detections: List[Detection] = []

        for c in cnts:
            if cv2.contourArea(c) < self.min_area:
                continue

            x, y, w, h = cv2.boundingRect(c)
            crop_thresh = dilated[y:y + h, x:x + w]
            detections.append(((x, y, w, h), crop_thresh))

        return frame, detections


def detector_process(input_queue: Queue, output_queue: Queue) -> None:
    detector = Detector()
    while True:
        frame = input_queue.get()
        if frame is None:
            break

        frame_out, detections = detector.detect(frame)
        output_queue.put((frame_out, detections))
