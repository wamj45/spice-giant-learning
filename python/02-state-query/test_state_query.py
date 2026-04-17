import os
import sys

from spice_wrapper.spice_wrapper import SpiceWrapper

'''
Query position, distance, and state of Mars relative to Earth
at the time of the Curiosity rover landing (2012-08-06T05:17:57 UTC).

Demonstrates spkpos(), spkezr(), and vnorm() using SPICE generic kernels.
Source: https://spiceypy.readthedocs.io/en/main/remote_sensing.html#solution-rs-1
'''

KM_PER_AU = 1.496e8
REF_FRAME = "J2000"
AB_CORRECTION = "LT+S" # lighttime and stellar aberration


def main():
    if len(sys.argv) < 2:
        print("Invalid arguments. Expected:")
        print("\tpython3 state_queries.py <config-file.json>")
        os._exit(100)

    config_file = sys.argv[1]

    spice_wrapper = SpiceWrapper()
    if spice_wrapper.initialize(config_file) is False:
        print("Failed to intialize SpiceWrapper")
        os._exit(101)

    # Curiosity landing on Mars - 2012-08-06T05:17:57
    utc = "2012-08-06T05:17:57"
    et = spice_wrapper.convert_utc_to_et(utc)
    print(f"====== Curiosity Landing: {utc} ======\n")

    mars_wrt_earth_position = spice_wrapper.get_position("MARS BARYCENTER", et, "EARTH", REF_FRAME, AB_CORRECTION)
    if mars_wrt_earth_position is None:
        print("Failed to get PositionData for [MARS] w.r.t [EARTH]")
        os._exit(102)

    print(f"Mars position relative to Earth (km):\n{mars_wrt_earth_position.position_as_dict()}")
    print(f"  Light time: {mars_wrt_earth_position.light_time:.3f} seconds\n")

    distance = spice_wrapper.distance_between_bodies("MARS BARYCENTER", et, "EARTH", REF_FRAME, AB_CORRECTION)
    if distance is None:
        print("Failed to get distance from MARS to EARTH")
        os._exit(103)

    print(f"Distance Earth -> Mars: {distance:.3f} km")
    print(f"Distance Earth -> Mars: {distance / KM_PER_AU:.6f} AU\n")

    mars_wrt_earth_state = spice_wrapper.get_state("MARS BARYCENTER", et, "EARTH", REF_FRAME, AB_CORRECTION)
    if mars_wrt_earth_state is None:
        print("Failed to get StateData for [MARS] w.r.t [EARTH]")
        os._exit(104)

    print("Mars full state relative to Earth:")
    print(f"\t{mars_wrt_earth_state.distance_as_dict()}")
    print(f"\t{mars_wrt_earth_state.velocity_as_dict()}")

    spice_wrapper.clear()

    print("\nDone!")


if __name__ == "__main__":
    main()
