from paddleocr import PaddleOCR
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass(frozen=True)
class Recognition:
    text: str
    poly: List[List[int]]
    conf: float


class Recogniser:
    def __init__(self, device: str):
        self.device = device
        self.model = PaddleOCR(
            lang="en", use_angle_cls=True, show_log=False, use_gpu=False if device == "cpu" else device
        )

    def run(self, image) -> Optional[Recognition]:
        predictions = self.model.ocr(image, cls=False)[0]

        if predictions:
            polys = [[[int(point[0]), int(point[1])] for point in prediction[0]] for prediction in predictions]
            texts = [prediction[1][0] for prediction in predictions]
            confs = [prediction[1][1] for prediction in predictions]

            if len(polys) > 1:
                # merge ocrs if multiple recognised
                clean_poly, clean_text, clean_conf = _clean_ocr(polys, texts, confs)
            else:
                # just clean the ocr text
                clean_poly = polys[0]
                clean_text = _clean_text(texts[0])
                clean_conf = confs[0]
            return Recognition(clean_text, clean_poly, clean_conf)
        else:
            return None


def _clean_ocr(
        polys: List[List[List[int]]], texts: List[str], confidences: List[float]
) -> Tuple[List[List[int]], str, float]:
    """Clean multiple ocr boxes from recognition model."""

    # Clean recognised texts removing relatively smaller ones
    polys, texts, confidences = _denoise_ocr_boxes(polys, texts, confidences)

    # Merge recognised texts
    return _merge_polys(polys), _merge_texts(texts), _merge_confs(confidences)


def _merge_texts(texts: List[str], delimiter: str = "") -> str:
    """Merge multiple texts into one."""
    return _clean_text(delimiter.join(texts))


def _denoise_ocr_boxes(
        polys: List[List[List[int]]], texts: List[str], confs: List[float]
) -> Tuple[List[List[List[int]]], List[str], List[float]]:
    """Remove noisy ocr boxes detected by the recognition model. Boxes less than half the height of the longest text
    will be removed."""

    # get the longest box
    polys_x_points = [[point[0] for point in poly] for poly in polys]
    poly_length = [max(poly_x_points) - min(poly_x_points) for poly_x_points in polys_x_points]
    longest_poly_idx = max(enumerate(poly_length), key=lambda x: x[1])[0]

    # get the height of the longest box
    longest_poly_y_points = [point[1] for point in polys[longest_poly_idx]]
    longest_poly_height = max(longest_poly_y_points) - min(longest_poly_y_points)

    # if it is smaller than half of the height of the longest box, remove the bos
    valid_idx = [
        idx for idx, poly in enumerate(polys) if
        (max(point[1] for point in poly) - min(point[1] for point in poly)) >= longest_poly_height
    ]

    return [polys[i] for i in valid_idx], [texts[i] for i in valid_idx], [confs[i] for i in valid_idx]


def _merge_polys(polys: List[List[List[int]]]) -> List[List[int]]:
    """Merge multiple boxes into one."""

    # Initialize variables to store min and max coordinates
    min_x = float('inf')
    min_y = float('inf')
    max_x = float('-inf')
    max_y = float('-inf')

    # Iterate through all boxes to find min and max coordinates
    for box in polys:
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
