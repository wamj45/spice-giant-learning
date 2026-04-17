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
