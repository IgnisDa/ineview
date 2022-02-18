import json

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


def process_video(location, unique_id):
    vid_cap = cv2.VideoCapture(location)
    success, image = vid_cap.read()
    count = 0
    data = []
    while success:
        detector = FER()
        d = detector.detect_emotions(image)
        success, image = vid_cap.read()
        if success and len(d) > 0:
            data.append(d)
        count += 1
    return json.loads(json.dumps(data, cls=NumpyEncoder))
