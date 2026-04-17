from typing import Dict
import numpy as np


class PositionData:
    def __init__(self) -> None:
        self.position: np.ndarray = None
        self.light_time: float = None
        self.x_km: float = None
        self.y_km: float = None
        self.z_km: float = None


    def set_position(self, position: np.ndarray):
        self.position = position
        self.x_km = float(position[0])
        self.y_km = float(position[1])
        self.z_km = float(position[2])


    def set_light_time(self, ltime: float):
        self.light_time = ltime


    def position_as_dict(self) -> Dict | None:
        if self.is_position_valid() is False:
            return None

        position = {
            "x": self.x_km,
            "y": self.y_km,
            "z": self.z_km
        }

        return position


    def is_position_valid(self) -> bool:
        if self.x_km is None:
            return False

        if self.y_km is None:
            return False

        if self.z_km is None:
            return False

        return True
