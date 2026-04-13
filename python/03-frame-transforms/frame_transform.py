import spiceypy
import json
import numpy as np

class FrameTransform:
    def __init__(self) -> None:
        self.spice = spiceypy


    # @TODO: Really need to make this its own handler
    # May have to create a python package for this...
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


    def get_rotation_matrix(self, init_frame: str, to_frame: str, et: float) -> np.ndarry | None:
        rot_matrix = None
        try:
            rot_matrix = self.spice.pxform(init_frame, to_frame, et)
        except Exception as e:
            print(f"Error - {str(e)}")
            return None

        return rot_matrix


    def rotate_vector(self, position: np.ndarray, rot_matrix: np.ndarray) -> np.ndarray | None:
        rot_vector = None
        try:
            rot_vector = self.spice.mxv(rot_matrix, position)
        except Exception as e:
            print(f"Error - {str(e)}")

        return rot_vector


    def get_angle_between_positions(self, pos_1: np.array, pos_2: np.array) -> float | None:
        angle = None

        try:
            angle = self.spice.vsep(pos_1, pos_2)
            angle = self.spice.convrt(angle, "RADIANS", "DEGREES")
        except Exception as e:
            print(f"Error - {str(e)}")
            return None

        return angle
