import spiceypy
import json

'''
Convert UTC time to ET time.
Source: https://spiceypy.readthedocs.io/en/main/remote_sensing.html#solution
'''

class TimeConverter:
    def __init__(self) -> None:
        self.spice = spiceypy


    def load_config(self, config_file: str) -> bool:
        try:
            with open(config_file, "r") as file:
                config = json.load(file)
        except Exception as e:
            print(f"\nError - {str(e)}")
            return False

        time_kernel = config["time_kernel"]
        self.spice.furnsh(time_kernel)
        print(f"Loaded Time Kernel from: [{time_kernel}]")

        return True


    def convert_utc_to_et(self, timestamp: str, debug: bool=True) -> float:
        et = self.spice.str2et(timestamp)

        if debug is True:
            print(f"UTC: [{timestamp}] -> ET [{et:.3f}]")

        return et


    def convert_et_calendar(self, et: float, debug: bool=False) -> str:
        et_cal = self.spice.etcal(et)

        if debug is True:
            print(f"ET: [{et:.3f}] -> ET Calendar: [{et_cal}]")

        return et_cal


    def convert_et_to_utc(self, et: float, debug: bool=False) -> str:
        utc = self.spice.et2utc(et, "C", 3)

        if debug is True:
            print(f"ET: [{et:.3f}] -> UTC: [{utc}]")

        return utc
