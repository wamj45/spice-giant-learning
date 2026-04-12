import spiceypy
import json

from models.position import PositionData
from models.state import StateData


class StateQuerier:
    def __init__(self, ref_frame: str, ab_corr: str) -> None:
        self.spice = spiceypy
        self.ref_frame = ref_frame
        self.ab_correction = ab_corr


    def load_config(self, config_file: str) -> bool:
        try:
            with open(config_file, "r") as file:
                config = json.load(file)
        except Exception as e:
            print(f"\nError - {str(e)}")
            return False

        try:
            self.spice.furnsh(config["time_kernel"])
            self.spice.furnsh(config["spk_kernel"])
            self.spice.furnsh(config["pck_kernel"])
        except Exception as e:
            print(f"\nError loading kernels - {str(e)}")
            return False

        print("Kernels loaded successfully\n")

        return True


    def get_position(self, target: str, et: float, observer: str) -> PositionData | None:
        try:
            position, light_time = self.spice.spkpos(target, et, self.ref_frame, self.ab_correction, observer)
        except Exception as e:
            print(f"\nError - {str(e)}")
            return None

        position_data = PositionData()
        position_data.set_position(position)
        position_data.set_light_time(light_time)

        return position_data


    def get_state(self, target: str, et: float, observer: str) -> StateData | None:
        try:
            state, light_time = self.spice.spkezr(target, et, self.ref_frame, self.ab_correction, observer)
        except Exception as e:
            print(f"\nError - {str(e)}")
            return None

        state_data = StateData()
        state_data.set_state(state)
        state_data.set_light_time(light_time)

        return state_data


    def get_distance(self, target: str, et: float, observer: str) -> float | None:
        position_data = self.get_position(target, et, observer)
        if position_data is None:
            print(f"Failed to get distance for [{target}] - Invalid position data")
            return None

        distance = self.spice.vnorm(position_data.position)

        return distance
