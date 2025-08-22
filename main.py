from multiprocessing import Process, Queue
from pathlib import Path
from contextlib import AbstractContextManager

from DetectionPipeline.streamer import streamer_process
from DetectionPipeline.detector import detector_process
from DetectionPipeline.presentor import presenter_process


class VideoPipeline(AbstractContextManager):
    def __init__(self, video_path: Path, queue_size: int = 10):
        self.video_path = video_path
        self.frames_queue = Queue(maxsize=queue_size)
        self.detections_queue = Queue(maxsize=queue_size)

        self.p_streamer = Process(target=streamer_process, args=(self.video_path, self.frames_queue))
        self.p_detector = Process(target=detector_process, args=(self.frames_queue, self.detections_queue))
        self.p_presenter = Process(target=presenter_process, args=(self.detections_queue,))

    def __enter__(self):
        self.p_streamer.start()
        self.p_detector.start()
        self.p_presenter.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.p_streamer.join()
        self.frames_queue.put(None)  # signal shutdown to detector
        self.p_detector.join()
        self.detections_queue.put(None)  # signal shutdown to presenter
        self.p_presenter.join()


def main():
    video_path = Path(__file__).resolve().parent / "Data" / "People-6387.mp4"
    with VideoPipeline(video_path, queue_size=10):
        pass


if __name__ == "__main__":
    main()
