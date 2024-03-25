from pathlib import Path
from ultralytics import YOLO
from typing import Union, List
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Detection:
    image: np.ndarray
    box: List[int]
    conf: float


class Detector:
    def __init__(self, detection_model: Union[str, Path], device: str):
        self.device = device
        self.model = YOLO(model=detection_model)

    def run(self, images: List[np.ndarray]) -> List[List[Detection]]:
        predictions = self.model.predict(images, device=self.device, verbose=False)
        results = []
        for image, detection in zip(images, predictions):
            image_detections = []
            if detection.boxes:
                det_boxes = detection.boxes.cpu().data.numpy().astype(int).tolist()
                det_confs = detection.boxes.cpu().conf.numpy().tolist()
                for det_box, det_conf in zip(det_boxes, det_confs):
                    x_min, x_max, y_min, y_max = det_box[0], det_box[2], det_box[1], det_box[3]
                    image_detections.append(Detection(image[y_min:y_max, x_min:x_max, :], det_box[:4], det_conf))
            results.append(image_detections)
        return results
