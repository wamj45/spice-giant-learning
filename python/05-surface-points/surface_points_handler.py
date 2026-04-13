import spiceypy
import json

from models.surface_point import SurfacePoint

'''
Compute surface intercept points on planetary bodies using SPICE.
Demonstrates subpnt() and subslr() for sub-observer and sub-solar points.
Used in OpNav for landmark navigation and illumination geometry.
Source: https://spiceypy.readthedocs.io/en/main/remote_sensing.html
'''

AB_CORRECTION = "LT+S"
COMPUTATION_METHOD = "INTERCEPT/ELLIPSOID"


class SurfacePointsHandler:
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


    def get_sub_observer_point(self, target: str, observer: str, et: float) -> SurfacePoint | None:
        try:
            spoint, trgepc, srfvec = self.spice.subpnt(
                COMPUTATION_METHOD,
                target,
                et,
                f"IAU_{target}",
                AB_CORRECTION,
                observer
            )

            radius, lon_rad, lat_rad = self.spice.reclat(spoint)
            lon_deg = lon_rad * self.spice.dpr()
            lat_deg = lat_rad * self.spice.dpr()

            dist = self.spice.vnorm(srfvec)

            surface_point = SurfacePoint()
            surface_point.setup(radius, lon_deg, lat_deg, dist, spoint)

            return surface_point

        except Exception as e:
            print(f"\nError - {str(e)}")

        return None


    def get_sub_solar_point(self, target: str, observer: str, et: float) -> SurfacePoint | None:
        '''
        Critical for OpNav - tells you where the target is most illuminated.
        '''
        try:
            spoint, trgepc, srfvec = self.spice.subslr(
                COMPUTATION_METHOD,
                target,
                et,
                f"IAU_{target}",
                AB_CORRECTION,
                observer
            )

            radius, lon_rad, lat_rad = self.spice.reclat(spoint)
            lon_deg = lon_rad * self.spice.dpr()
            lat_deg = lat_rad * self.spice.dpr()
            dist = self.spice.vnorm(srfvec)

            surface_point = SurfacePoint()
            surface_point.setup(radius, lon_deg, lat_deg, dist, spoint)

            return surface_point

        except Exception as e:
            print(f"\nError - {str(e)}")

        return None
