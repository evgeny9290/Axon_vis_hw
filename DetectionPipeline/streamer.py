from multiprocessing import Queue
import cv2
from pathlib import Path


def streamer_process(video_path: Path, frames_output_queue: Queue) -> None:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames_output_queue.put(frame)

    cap.release()
