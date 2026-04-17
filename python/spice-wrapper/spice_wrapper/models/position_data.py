import numpy as np

class PositionData:
    def __init__(self) -> None:
        self.position: np.ndarray = None
        self.light_time: float = None


    def set_position(self, position: np.ndarray):
        self.position = position


    def set_light_time(self, ltime: float):
        self.light_time = ltime
