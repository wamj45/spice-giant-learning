from typing import Dict
from typing import List
import json


class KernelManager:
    def __init__(self) -> None:
        self.kernel_config: Dict = {}
        self.time_kernel: str = None
        self.spk_kernel: str = None
        self.pck_kernel: str = None


    def _get_kernel_path(self, kernel_name: str) -> str | None:
        if kernel_name not in self.kernel_config:
            return None

        kernel = self.kernel_config[kernel_name]

        return kernel


    def load_config(self, config_file: str) -> bool:
        try:
            with open(config_file, "r") as file:
                self.kernel_config = json.load(file)
        except Exception as e:
            print(f"\nError - {str(e)}")
            return False

        return self.parse_config()


    def parse_config(self) -> bool:
        self.time_kernel = self._get_kernel_path(kernel_name="time_kernel")
        if self.time_kernel is None:
            print("Failed to load Time Kernel")

        self.spk_kernel = self._get_kernel_path("spk_kernel")
        if self.spk_kernel is None:
            print("Failed to load SPK Kernel")

        self.pck_kernel = self._get_kernel_path("pck_kernel")
        if self.pck_kernel is None:
            print("Failed to load PCK Kernel")

        return True


    def get_time_kernel(self) -> str | None:
        return self.time_kernel


    def get_spk_kernel(self) -> str | None:
        return self.spk_kernel


    def get_pck_kernel(self) -> str | None:
        return self.pck_kernel
