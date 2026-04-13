import os
import sys

from frame_transform import FrameTransform

REF_FRAME = "J2000"
AB_CORRECTION = "LT+S" # lighttime and stellar aberration


def main():
    if len(sys.argv) < 2:
        print("Invalid arguments. Expected:")
        print("\tpython3 frame_transforms.py <config-file.json>")
        os._exit(100)

    config_file = sys.argv[1]

    transformer = FrameTransform()
    if transformer.load_config(config_file) is False:
        print("Failed to load config file")
        os._exit(101)

    # New Horizons Pluto flyby - 2015-07-14T11:49:57
    utc = "2015-07-14T11:49:57"
    et = transformer.spice.str2et(utc)
    print(f"====== New Horizons Pluto Flyby: {utc} ======\n")

    mars_pos, light_time = transformer.spice.spkpos("MARS BARYCENTER", et, REF_FRAME, AB_CORRECTION, "EARTH")
    print("Mars position in J2000 frame (km):")
    print(f"  [{mars_pos[0]:.1f}, {mars_pos[1]:.1f}, {mars_pos[2]:.1f}]")

    j2000_wrt_earth = transformer.get_rotation_matrix(REF_FRAME, "IAU_EARTH", et)
    if j2000_wrt_earth is None:
        print("Failed to get rotation matrix")
        os._exit(102)

    print("\nRotation matrix J2000 -> IAU_EARTH:")
    for row in j2000_wrt_earth:
        print(f"  [{row[0]:10.6f}, {row[1]:10.6f}, {row[2]:10.6f}]")

    mars_earth_fixed = transformer.rotate_vector(mars_pos, j2000_wrt_earth)
    if mars_earth_fixed is None:
        print("Failed to compute rotation vector between: [MARS] - [EARTH]")
        os._exit(103)

    print("\nMars position in IAU_EARTH frame (km):")
    print(f"  [{mars_earth_fixed[0]:.1f}, {mars_earth_fixed[1]:.1f}, {mars_earth_fixed[2]:.1f}]")

    dist_j2000 = transformer.spice.vnorm(mars_pos)
    dist_earth_fixed = transformer.spice.vnorm(mars_earth_fixed)
    print("\nDistance check (should be identical):")
    print(f"  J2000 frame:     {dist_j2000:.3f} km")
    print(f"  IAU_EARTH frame: {dist_earth_fixed:.3f} km")

    sun_pos, light_time = transformer.spice.spkpos("SUN", et, REF_FRAME, AB_CORRECTION, "EARTH")
    angle = transformer.get_angle_between_positions(mars_pos, sun_pos)
    print(f"\nAngle between Mars and Sun as seen from Earth: {angle:.3f} degrees")

    transformer.spice.kclear()
    print("\nDone!")


if __name__ == "__main__":
    main()
