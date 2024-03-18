from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class NumberPlate:
    det_box: List[int]
    det_conf: float
    rec_poly: List[List[int]] = None
    rec_text: str = None
    rec_conf: float = None
