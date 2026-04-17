import numpy as np

class StateData:
    def __init__(self) -> None:
        self.state: np.ndarray = None
        self.light_time: float = None


    def set_state(self, state: np.ndarray):
        self.state = state


    def set_light_time(self, ltime: float):
        self.light_time = ltime
