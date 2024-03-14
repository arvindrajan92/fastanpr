from typing import List


class NumberPlate:
    def __init__(
            self,
            det_box: List[int],
            det_conf: float,
            rec_box: List[List[int]] = None,
            rec_text: str = None,
            rec_conf: float = None
    ):
        self.det_box = det_box
        self.det_conf = det_conf
        self.rec_box = rec_box
        self.rec_text = rec_text
        self.rec_conf = rec_conf
        self.combined_conf = det_conf * rec_conf if rec_conf is not None else None

    def __str__(self) -> str:
        return (f"NumberPlate(det_box={self.det_box}, det_conf={self.det_conf}, rec_box='{self.rec_box}', "
                f"rec_text={self.rec_text}, rec_conf={self.rec_conf}, combined_conf={self.combined_conf})")

    def __repr__(self) -> str:
        return self.__str__()
