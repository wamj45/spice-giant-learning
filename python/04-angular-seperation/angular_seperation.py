import spiceypy
import json

AB_CORRECTION = "LT+S"
KM_PER_AU = 1.496e8
REF_FRAME = "J2000"

'''
Compute angular separation and phase angles between solar system bodies.
Demonstrates vsep(), dpr(), and illumination geometry.
Used in OpNav for sun-phase angles and target visibility checks.
Source: https://spiceypy.readthedocs.io/en/main/remote_sensing.html
'''

class AngularSeparation:
    def __init__(self) -> None:
        self.spice = spiceypy


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


    def get_separation(self, body_a: str, body_b: str, observer: str, et: float) -> float:
        pos_a, light_time = self.spice.spkpos(body_a, et, REF_FRAME, AB_CORRECTION, observer)
        pos_b, light_time = self.spice.spkpos(body_b, et, REF_FRAME, AB_CORRECTION, observer)

        angle_rad = self.spice.vsep(pos_a, pos_b)
        angle_degrees = angle_rad * self.spice.dpr()

        return angle_degrees


    def get_sun_phase_angle(self, target: str, observer: str, et: float) -> float:
        sun_from_target, light_time = self.spice.spkpos("SUN", et, REF_FRAME, AB_CORRECTION, target)
        obs_from_target, light_time = self.spice.spkpos(observer, et, REF_FRAME, AB_CORRECTION, target)

        angle_rad = self.spice.vsep(sun_from_target, obs_from_target)
        angle_degrees = angle_rad * self.spice.dpr()

        return angle_degrees


    def get_distance_au(self, target: str, observer: str, et: float) -> float:
        pos, light_time = self.spice.spkpos(target, et, REF_FRAME, AB_CORRECTION, observer)

        return self.spice.vnorm(pos) / KM_PER_AU
