import tempfile

from fer import FER, Video


def process_video(location):
    face_detector = FER(mtcnn=True)
    input_video = Video(location, outdir=tempfile.gettempdir())
    processing_data = input_video.analyze(
        face_detector,
        display=False,
        save_video=False,
        save_frames=True,
    )
    return processing_data
