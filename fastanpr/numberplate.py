from typing import List, Tuple, Dict


class NumberPlate:
    def __init__(
            self,
            det_box: List[int],
            det_conf: float,
            rec_poly:  List[List[List[int]]] = None,
            rec_text: List[str] = None,
            rec_conf: List[float] = None
    ):
        self.det_box = det_box
        self.det_conf = det_conf

        # if ocr is successful
        if all(r is not None for r in [rec_poly, rec_text, rec_conf]):
            if len(rec_poly) > 1:
                # merge ocrs if multiple recognised
                self.rec_poly, self.rec_text, self.rec_conf = self._clean_ocr(rec_poly, rec_text, rec_conf)
            else:
                # just clean the ocr text
                self.rec_poly, self.rec_text, self.rec_conf = rec_poly[0], self._clean_text(rec_text[0]), rec_conf[0]
        else:
            self.rec_poly, self.rec_text, self.rec_conf = None, None, None

    def __str__(self) -> str:
        return (f"NumberPlate(det_box={self.det_box}, det_conf={self.det_conf}, rec_poly={self.rec_poly}, "
                f"rec_text={self.rec_text}, rec_conf={self.rec_conf})")

    def __repr__(self) -> str:
        return self.__str__()

    def to_dict(self) -> Dict:
        """Converts attributes to dictionary"""
        return {
            attr: getattr(self, attr) for attr in dir(self)
            if not attr.startswith('_') and not callable(getattr(self, attr))
        }

    def _clean_ocr(
            self, boxes: List[List[List[int]]], texts: List[str], confidences: List[float]
    ) -> Tuple[List[List[int]], str, float]:
        """Clean multiple ocr boxes from recognition model."""

        # Clean recognised texts removing relatively smaller ones
        boxes, texts, confidences = self._denoise_ocr_boxes(boxes, texts, confidences)

        # Merge recognised texts
        return self._merge_boxes(boxes), self._merge_texts(texts), self._merge_confs(confidences)

    def _merge_texts(self, texts: List[str], delimiter: str = "") -> str:
        """Merge multiple texts into one."""
        return self._clean_text(delimiter.join(texts))

    @staticmethod
    def _denoise_ocr_boxes(
            boxes: List[List[List[int]]], texts: List[str], confs: List[float]
    ) -> Tuple[List[List[List[int]]], List[str], List[float]]:
        """Remove noisy ocr boxes detected by the recognition model. Boxes less than half the height of the longest text
        will be removed."""

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
    def _merge_boxes(boxes: List[List[List[int]]]) -> List[List[int]]:
        """Merge multiple boxes into one."""

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
    def _merge_confs(confidences: List[float]) -> float:
        """Merge multiple confidences into one."""
        result = 1.0
        for confidence in confidences:
            result *= confidence
        return result

    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean text by removing non-alphanumerics."""
        return "".join([t for t in text if t.isalnum()])
