from multiprocessing import Queue
from typing import Generator
import cv2
from pathlib import Path


def streamer_process(video_path: Path, output_queue: Queue) -> None:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"Error: Cannot open video {video_path}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        output_queue.put(frame)

    cap.release()
    print("[Streamer] Done.")


if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    vid_path = current_dir / "People-6387.mp4"
    x = streamer(vid_path)
    print(x)
