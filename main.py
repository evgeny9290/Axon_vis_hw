from multiprocessing import Process, Queue
from pathlib import Path
from contextlib import AbstractContextManager

from streamer import streamer_process
from detector import detector_process
from presentor import presenter_process


class VideoPipeline(AbstractContextManager):
    def __init__(self, video_path: Path, queue_size: int = 10):
        self.video_path = video_path
        self.queue_raw = Queue(maxsize=queue_size)
        self.queue_detected = Queue(maxsize=queue_size)

        self.p_streamer = Process(target=streamer_process, args=(self.video_path, self.queue_raw))
        self.p_detector = Process(target=detector_process, args=(self.queue_raw, self.queue_detected))
        self.p_presenter = Process(target=presenter_process, args=(self.queue_detected,))

    def __enter__(self):
        self.p_streamer.start()
        self.p_detector.start()
        self.p_presenter.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.p_streamer.join()
        self.queue_raw.put(None)  # signal shutdown to detector
        self.p_detector.join()
        self.queue_detected.put(None)  # signal shutdown to presenter
        self.p_presenter.join()


def main():
    video_path = Path(__file__).resolve().parent / "People-6387.mp4"
    with VideoPipeline(video_path, queue_size=10):
        pass


if __name__ == "__main__":
    main()
