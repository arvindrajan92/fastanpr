import numpy as np
from pathlib import Path
from ultralytics import YOLO
from paddleocr import PaddleOCR

from .numberplate import NumberPlate
from typing import Union, List

__version__ = "0.1.2"


class FastANPR:
    def __init__(
            self,
            detection_model: Union[str, Path] = Path(__file__).parent / 'best.pt',
            device: str = "cpu"
    ):
        self.detector = YOLO(model=detection_model)
        self.recogniser = PaddleOCR(
            lang="en",
            use_angle_cls=True,
            show_log=False,
            use_gpu=False if device == "cpu" else device
        )
        self.device = device

    async def run(self, images: Union[np.ndarray, List[np.ndarray]]) -> List[List[NumberPlate]]:
        """Runs ANPR on a list of images and return a list of detected number plates."""
        # Images are expected to be numpy arrays of dimension 3 (HWC) or 4 (BHWC), or list of numpy arrays
        if isinstance(images, np.ndarray):
            if len(images.shape) == 3:
                images = [images]
            elif len(images.shape) == 4:
                images = [image for image in images]
            else:
                raise ValueError(f"Expected ndarray images of dimension 3 or 4, but {len(images.shape)} received.")
        elif isinstance(images, List):
            pass
        else:
            raise ValueError(f"Expected images of type ndarray or List[ndarray], but {type(images).__name__} received.")

        # Detect number plates
        detections = self.detector.predict(images, device=self.device, verbose=False)

        # OCR detected number plates
        results = []
        for image, detection in zip(images, detections):
            image_results = []
            detection = detection.cpu()
            if detection.boxes:
                det_boxes = detection.boxes.data.numpy().astype(int).tolist()
                det_confs = detection.boxes.conf.numpy().tolist()
                for det_box, det_conf in zip(det_boxes, det_confs):
                    x_min, x_max, y_min, y_max = det_box[0], det_box[2], det_box[1], det_box[3]
                    ocrs = self.recogniser.ocr(image[y_min:y_max + 1, x_min:x_max + 1, :], cls=False)[0]

                    if ocrs:
                        boxes = [[[int(b[0] + x_min), int(b[1] + y_min)] for b in ocr[0]] for ocr in ocrs]
                        texts = [pcr[1][0] for pcr in ocrs]
                        confidences = [pcr[1][1] for pcr in ocrs]

                        image_results.append(NumberPlate(det_box[:4], det_conf, boxes, texts, confidences))
                    else:
                        image_results.append(NumberPlate(det_box[:4], det_conf))
            results.append(image_results)

        return results
