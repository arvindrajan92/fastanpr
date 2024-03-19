import cv2
import pytest
import Levenshtein
import numpy as np
from typing import List
from pathlib import Path
from fastanpr import FastANPR

fastanpr = FastANPR()


@pytest.mark.asyncio
async def test_image_3d():
    file = Path(__file__).parent / 'images/image001.jpg'
    expected_plates = ['BVH826']
    predicted_plates = (await fastanpr.run(image_path_to_ndarray(str(file))))[0]

    # same number of plates predicted
    assert len(predicted_plates) == len(expected_plates)

    # ocr box is inside detected box
    assert all(
        ocr_box_encapsulates_detected_box(poly_to_bbox(predicted_plate.rec_poly), predicted_plate.det_box)
        for predicted_plate in predicted_plates
    )

    # maximum Levenshtein distance must be 1
    assert all(
        min(Levenshtein.distance(predicted_plate.rec_text, expected_plates) for expected_plates in expected_plates) <= 1
        for predicted_plate in predicted_plates
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'file, expected_plates', [
        (Path(__file__).parent / 'images/image001.jpg', ['BVH826']),
        (Path(__file__).parent / 'images/image002.jpg', ['XJIIMES', 'FEIIDEK']),
        (Path(__file__).parent / 'images/image003.jpg', ['CLS7145', '319ZBA']),
        (Path(__file__).parent / 'images/image004.jpg', ['560ZPC']),
        (Path(__file__).parent / 'images/image005.jpg', ['ERS73W']),
        (Path(__file__).parent / 'images/image006.jpg', ['BPN325']),
    ]
)
async def test_image_4d(file: str, expected_plates: List[str]):
    predicted_plates = (await fastanpr.run([image_path_to_ndarray(str(file))]))[0]

    # same number of plates predicted
    assert len(predicted_plates) == len(expected_plates)

    # ocr box is inside detected box
    assert all(
        ocr_box_encapsulates_detected_box(poly_to_bbox(predicted_plate.rec_poly), predicted_plate.det_box)
        for predicted_plate in predicted_plates
    )

    # minimum Levenshtein distance must be 1
    assert all(
        min(Levenshtein.distance(predicted_plate.rec_text, expected_plates) for expected_plates in expected_plates) <= 1
        for predicted_plate in predicted_plates
    )


def ocr_box_encapsulates_detected_box(ocr_box: List[int], det_box: List[int]) -> bool:
    return (ocr_box[0] >= det_box[0] and ocr_box[1] >= det_box[1] and
            ocr_box[2] <= det_box[2] and ocr_box[3] <= det_box[3])


def poly_to_bbox(poly: List[List[int]]) -> List[int]:
    x_coordinates = [point[0] for point in poly]
    y_coordinates = [point[1] for point in poly]
    x_min = min(x_coordinates)
    y_min = min(y_coordinates)
    x_max = max(x_coordinates)
    y_max = max(y_coordinates)
    return [x_min, y_min, x_max, y_max]


def image_path_to_ndarray(file: str) -> np.ndarray:
    return cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2RGB)
