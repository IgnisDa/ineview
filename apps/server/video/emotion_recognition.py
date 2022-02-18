import contextlib
import json
import os
import tempfile

import cv2
import numpy as np
from fer import FER


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray) and obj.ndim == 1:
            return obj.tolist()
        elif isinstance(obj, np.generic):
            return obj.item()
        return json.JSONEncoder.default(self, obj)


def video_to_frames(pathIn, unique_id):
    vid_cap = cv2.VideoCapture(pathIn)
    success, image = vid_cap.read()
    count = 0
    paths = []
    while success:
        path = os.path.join(
            tempfile.gettempdir(), f"image-{unique_id}-frame-{count}.jpg"
        )
        if not cv2.imwrite(path, image):
            raise Exception("Could not write image")
        paths.append(path)
        success, image = vid_cap.read()
        count += 1
    return paths


def process_video(location, unique_id):
    paths = video_to_frames(location, unique_id)
    data = []
    for path in paths:
        img = cv2.imread(path)
        detector = FER(mtcnn=True)
        d = detector.detect_emotions(img)
        if len(d) > 0:
            data.append(d)
        with contextlib.suppress(FileNotFoundError):
            os.remove(path)
    return json.loads(json.dumps(data, cls=NumpyEncoder))
