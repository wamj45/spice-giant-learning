import numpy as np

class SurfacePoint:
    def __init__(self) -> None:
        self.spoint: np.ndarry = None
        self.latitude_deg: float = None
        self.longitude_deg: float = None
        self.radius: float = None
        self.distance: float = None


    def setup(self, radius: float, long_deg: float, lat_deg: float, dist: float, spoint: np.ndarray):
        self.radius = radius
        self.longitude_deg = long_deg
        self.latitude_deg = lat_deg
        self.distance = dist
        self.spoint = spoint


    def is_valid(self) -> bool:
        if self.spoint is None:
            return False

        if self.latitude_deg is None:
            return False

        if self.longitude_deg is None:
            return False

        if self.radius is None:
            return False

        if self.distance is None:
            return False

        return True
