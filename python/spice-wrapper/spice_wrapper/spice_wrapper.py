import spiceypy

from spice_wrapper.util.kernel_manager import KernelManager


class SpiceWrapper:
    def __init__(self) -> None:
        self.kernel_manager: KernelManager = None
        self.spice: object = None


    def initialize(self, kernel_config: str) -> bool:
        self.spice = spiceypy

        self.kernel_manager = KernelManager()
        if self.kernel_manager.load_config(kernel_config) is False:
            print(f"Error - Failed to load kernel config: [{kernel_config}]")
            return False

        if self.load_kernels() is False:
            return False

        print("SpicePy instance ready!\n")

        return True


    def load_kernels(self) -> bool:
        try:
            self.spice.furnsh(self.kernel_manager.get_time_kernel())
            self.spice.furnsh(self.kernel_manager.get_spk_kernel())
            self.spice.furnsh(self.kernel_manager.get_pck_kernel())
        except Exception as e:
            print(f"Error - {str(e)}")
            return False

        return True


    def convert_utc_to_et(self, timestamp: str, verbose: bool=False) -> float:
        et = self.spice.str2et(timestamp)

        if verbose is True:
            print(f"UTC: [{timestamp}] -> ET [{et:.3f}]")

        return et


    def convert_et_calendar(self, et: float, verbose: bool=False) -> str:
        et_cal = self.spice.etcal(et)

        if verbose is True:
            print(f"ET: [{et:.3f}] -> ET Calendar: [{et_cal}]")

        return et_cal


    def convert_et_to_utc(self, et: float, verbose: bool=False) -> str:
        utc = self.spice.et2utc(et, "C", 3)

        if verbose is True:
            print(f"ET: [{et:.3f}] -> UTC: [{utc}]")

        return utc


    def get_position(self, target: str, et: float, observer: str, ref_frame: str, ab_corr: str) -> PositionData | None:
        try:
            position, light_time = self.spice.spkpos(target, et, ref_frame, ab_corr, observer)
        except Exception as e:
            print(f"\nError - {str(e)}")
            return None

        position_data = PositionData()
        position_data.set_position(position)
        position_data.set_light_time(light_time)

        return position_data


    def get_state(self, target: str, et: float, observer: str, ref_frame: str, ab_corr: str) -> StateData | None:
        try:
            state, light_time = self.spice.spkezr(target, et, ref_frame, ab_corr, observer)
        except Exception as e:
            print(f"\nError - {str(e)}")
            return None

        state_data = StateData()
        state_data.set_state(state)
        state_data.set_light_time(light_time)

        return state_data


    def distance_between_bodies(self, target: str, et: float, observer: str) -> float | None:
        position_data = self.get_position(target, et, observer)
        if position_data is None:
            print(f"Failed to get distance for [{target}] - Invalid position data")
            return None

        distance = self.spice.vnorm(position_data.position)

        return distance
