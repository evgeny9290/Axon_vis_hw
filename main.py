from multiprocessing import Process, Queue
from pathlib import Path

from streamer import streamer_process
from detector import detector_process
from presentor import presenter_process


def main():
    queue_raw = Queue(maxsize=10)         # From Streamer to Detector
    queue_detected = Queue(maxsize=10)    # From Detector to Presenter (TBD)

    video_path = Path(__file__).resolve().parent / "People-6387.mp4"

    p_streamer = Process(target=streamer_process, args=(video_path, queue_raw))
    p_detector = Process(target=detector_process, args=(queue_raw, queue_detected))
    p_presenter = Process(target=presenter_process, args=(queue_detected,))

    p_streamer.start()
    p_detector.start()
    p_presenter.start()

    p_streamer.join()
    queue_raw.put(None)  # shutdown detector
    p_detector.join()
    queue_detected.put(None)  # shutdown presenter
    p_presenter.join()

    print("[Main] Pipeline completed.")


if __name__ == "__main__":
    main()
