import asyncio
import numpy as np
import pkg_resources
from pathlib import Path
from ultralytics import YOLO
from paddleocr import PaddleOCR

from .numberplate import NumberPlate
from typing import Union, List, Tuple


class FastANPR:
    def __init__(
            self,
            detection_model: Union[str, Path] = pkg_resources.resource_filename('fastanpr', 'best.pt'),
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
                    ocrs = self.recogniser.ocr(image[y_min:y_max+1, x_min:x_max+1, :], cls=False)[0]

                    if ocrs:
                        boxes = [[[int(b[0] + x_min), int(b[1] + y_min)] for b in ocr[0]] for ocr in ocrs]
                        texts = [pcr[1][0] for pcr in ocrs]
                        confidences = [pcr[1][1] for pcr in ocrs]

                        if len(ocrs) > 1:
                            # Clean recognised texts removing relatively smaller ones
                            boxes, texts, confidences = await self._denoise_ocr_boxes(boxes, texts, confidences)

                            # Merge recognised texts
                            merged_box, merged_text, merged_conf = await asyncio.gather(
                                self._merge_boxes(boxes),
                                self._merge_texts(texts),
                                self._merge_confidences(confidences)
                            )

                            image_results.append(
                                NumberPlate(det_box[:4], det_conf, merged_box, merged_text, merged_conf)
                            )
                        else:
                            image_results.append(NumberPlate(det_box[:4], det_conf, boxes[0], texts[0], confidences[0]))
                    else:
                        image_results.append(NumberPlate(det_box[:4], det_conf))
            results.append(image_results)

        return results

    @staticmethod
    async def _denoise_ocr_boxes(
            boxes: List[List[List[int]]], texts: List[str], confs: List[float]
    ) -> Tuple[List[List[List[int]]], List[str], List[float]]:
        # get the longest box
        boxes_x_points = [[point[0] for point in box] for box in boxes]
        box_length = [max(box_x_points) - min(box_x_points) for box_x_points in boxes_x_points]
        longest_box_idx = max(enumerate(box_length), key=lambda x: x[1])[0]

        # get the height of the longest box
        longest_box_y_points = [point[1] for point in boxes[longest_box_idx]]
        longest_box_height = max(longest_box_y_points) - min(longest_box_y_points)

        # if it is smaller than half of the height of the longest box, remove the bos
        valid_idx = [
            idx for idx, box in enumerate(boxes) if
            (max(point[1] for point in box) - min(point[1] for point in box)) >= longest_box_height
        ]

        return [boxes[i] for i in valid_idx], [texts[i] for i in valid_idx], [confs[i] for i in valid_idx]

    @staticmethod
    async def _merge_boxes(boxes: List[List[List[int]]]) -> List[List[int]]:
        # Initialize variables to store min and max coordinates
        min_x = float('inf')
        min_y = float('inf')
        max_x = float('-inf')
        max_y = float('-inf')

        # Iterate through all boxes to find min and max coordinates
        for box in boxes:
            for point in box:
                min_x = min(min_x, point[0])
                min_y = min(min_y, point[1])
                max_x = max(max_x, point[0])
                max_y = max(max_y, point[1])

        # Construct the merged box
        merged_box = [
            [int(min_x), int(min_y)],
            [int(max_x), int(min_y)],
            [int(max_x), int(max_y)],
            [int(min_x), int(max_y)]
        ]

        return merged_box

    @staticmethod
    async def _merge_texts(texts: List[str], delimiter: str = " ") -> str:
        # Join texts
        return delimiter.join(texts)

    @staticmethod
    async def _merge_confidences(confidences: List[float]) -> float:
        # Multiply confidences
        result = 1.0
        for confidence in confidences:
            result *= confidence
        return result
