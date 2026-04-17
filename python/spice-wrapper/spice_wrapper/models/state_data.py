from typing import Dict
import numpy as np


class StateData:
    def __init__(self) -> None:
        self.state: np.ndarray = None
        self.light_time: float = None
        self.x_km: float = None
        self.y_km: float = None
        self.z_km: float = None
        self.velocity_x: float = None
        self.velocity_y: float = None
        self.velocity_z: float = None


    def set_state(self, state: np.ndarray):
        self.state = state
        self.x_km = float(state[0])
        self.y_km = float(state[1])
        self.z_km = float(state[2])
        self.velocity_x = float(state[3])
        self.velocity_y = float(state[4])
        self.velocity_z = float(state[5])


    def set_light_time(self, ltime: float):
        self.light_time = ltime


    def dump_data(self) -> Dict:
        ret = {
            "x_position": self.x_km,
            "y_position": self.y_km,
            "z_position": self.z_km,
            "velocity_x": self.velocity_x,
            "velocity_y": self.velocity_y,
            "velocity_z": self.velocity_z
        }

        return ret


    def distance_as_dict(self) -> Dict | None:
        if self.is_distance_valid() is False:
            return None

        distance = {
            "x_position": self.x_km,
            "y_position": self.y_km,
            "z_position": self.z_km
        }

        return distance


    def velocity_as_dict(self) -> Dict | None:
        if self.is_velocity_valid() is False:
            return None

        velocity = {
            "velocity_x": self.velocity_x,
            "velocity_y": self.velocity_y,
            "velocity_z": self.velocity_z
        }

        return velocity


    def is_distance_valid(self) -> bool:
        if self.x_km is None:
            return False

        if self.y_km is None:
            return False

        if self.z_km is None:
            return False

        return True


    def is_velocity_valid(self) -> bool:
        if self.velocity_x is None:
            return False

        if self.velocity_y is None:
            return False

        if self.velocity_z is None:
            return False

        return True
