import sys
import os

from surface_points_handler import SurfacePointsHandler


def main():
    if len(sys.argv) < 2:
        print("Invalid arguments. Expected:")
        print("\tpython3 surface_points.py <config-file.json>")
        os._exit(100)

    config_file = sys.argv[1]

    surface_pts_handler = SurfacePointsHandler()
    if surface_pts_handler.load_config(config_file) is False:
        print("Failed to load config file")
        os._exit(101)

    # Curiosity landing on Mars - 2012-08-06T05:17:57
    utc = "2012-08-06T05:17:57"

    # future date
    # utc = "2030-01-01T00:00:00"

    et = surface_pts_handler.spice.str2et(utc)
    print(f"====== Curiosity Landing: {utc} ======\n")

    sub_obs = surface_pts_handler.get_sub_observer_point("MOON", "EARTH", et)
    if sub_obs is None:
        print("Failed to get sub-observer point")
        os._exit(102)

    print("Sub-observer point on Moon (point on Moon surface facing Earth):")
    print(f"  Latitude:  {sub_obs.latitude_deg:.3f} deg")
    print(f"  Longitude: {sub_obs.longitude_deg:.3f} deg")
    print(f"  Radius:    {sub_obs.radius:.3f} km")
    print(f"  Distance from Earth: {sub_obs.distance:.3f} km\n")

    sub_sol = surface_pts_handler.get_sub_solar_point("MOON", "EARTH", et)
    if sub_sol is None:
        print("Failed to get sub-solar point")
        os._exit(103)

    print("Sub-solar point on Moon (most illuminated point):")
    print(f"  Latitude:  {sub_sol.latitude_deg:.3f} deg")
    print(f"  Longitude: {sub_sol.longitude_deg:.3f} deg")
    print(f"  Radius:    {sub_sol.radius:.3f} km\n")

    lon_diff = abs(sub_obs.longitude_deg - sub_sol.longitude_deg)
    if lon_diff > 180:
        lon_diff = 360 - lon_diff

    print(f"Longitude difference sub-observer vs sub-solar: {lon_diff:.3f} deg")
    print("(0 deg = fully illuminated from Earth, 180 deg = fully in shadow)\n")

    surface_pts_handler.spice.kclear()

    print("Done!")


if __name__ == "__main__":
    main()
