from dataclasses import dataclass
from typing import List, Tuple, Union


@dataclass
class NumberPlate:
    det_box: List[int]
    det_conf: float
    rec_poly: Union[List[List[List[int]]], List[List[int]]] = None
    rec_text: Union[List[str], str] = None
    rec_conf: Union[List[float], float] = None

    def __post_init__(self):
        # if ocr is successful
        if all(r is not None for r in [self.rec_poly, self.rec_text, self.rec_conf]):
            if len(self.rec_poly) > 1:
                # merge ocrs if multiple recognised
                self.rec_poly, self.rec_text, self.rec_conf = _clean_ocr(
                    self.rec_poly, self.rec_text, self.rec_conf
                )
            else:
                # just clean the ocr text
                self.rec_poly = self.rec_poly[0]
                self.rec_text = _clean_text(self.rec_text[0])
                self.rec_conf = self.rec_conf[0]


def _clean_ocr(
        boxes: List[List[List[int]]], texts: List[str], confidences: List[float]
) -> Tuple[List[List[int]], str, float]:
    """Clean multiple ocr boxes from recognition model."""

    # Clean recognised texts removing relatively smaller ones
    boxes, texts, confidences = _denoise_ocr_boxes(boxes, texts, confidences)

    # Merge recognised texts
    return _merge_boxes(boxes), _merge_texts(texts), _merge_confs(confidences)


def _merge_texts(texts: List[str], delimiter: str = "") -> str:
    """Merge multiple texts into one."""
    return _clean_text(delimiter.join(texts))


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


def _merge_confs(confidences: List[float]) -> float:
    """Merge multiple confidences into one."""
    result = 1.0
    for confidence in confidences:
        result *= confidence
    return result


def _clean_text(text: str) -> str:
    """Clean text by removing non-alphanumerics."""
    return "".join([t for t in text if t.isalnum()])
