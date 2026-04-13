from typing import Dict
import json

# @TODO:
# This will need to be a python package
class KernelManager:
    def __init__(self) -> None:
        self.kernel_config: Dict = {}


    def load_config(self, config_file: str) -> bool:
        try:
            with open(config_file, "r") as file:
                self.kernel_config = json.load(file)
        except Exception as e:
            print(f"\nError - {str(e)}")
            return False

        return True


    def get_kernel(self, kernel_name: str) -> str | None:
        if kernel_name not in self.kernel_config:
            return None

        kernel = self.config[kernel_name]

        return kernel


    def get_time_kernel(self) -> str | None:
        return self.get_kernel("time_kernel")


    def get_spk_kernel(self) -> str | None:
        return self.get_kernel("spk")


    def get_pck_kernel(self) -> str | None:
        return self.get_kernel("pck")
