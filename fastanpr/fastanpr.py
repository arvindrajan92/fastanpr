import numpy as np
from pathlib import Path
from typing import Union, List
from .detection import Detector
from .recognition import Recogniser
from .numberplate import NumberPlate


class FastANPR:
    def __init__(
            self,
            detection_model: Union[str, Path] = Path(__file__).parent / 'best.pt',
            device: str = "cpu"
    ):
        self.detector = Detector(detection_model=detection_model, device=device)
        self.recogniser = Recogniser(device=device)
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
        detections = self.detector.run(images)

        # OCR detected number plates
        results = []
        for image_detections in detections:
            image_results = []
            if image_detections:
                for detection in image_detections:
                    recognition = self.recogniser.run(detection.image)
                    if recognition:
                        offset_recog_poly = self._offset_recognition_poly(detection.box, recognition.poly)
                        image_results.append(
                            NumberPlate(
                                detection.box, detection.conf, offset_recog_poly, recognition.text, recognition.conf
                            )
                        )
                    else:
                        image_results.append(NumberPlate(detection.box, detection.conf))
            results.append(image_results)
        return results

    @staticmethod
    def _offset_recognition_poly(detection_box: List[int], recognition_poly: List[List[int]]) -> List[List[int]]:
        return [[point[0] + detection_box[0], point[1] + detection_box[1]] for point in recognition_poly]
