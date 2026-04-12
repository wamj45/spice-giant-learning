import os
import sys

from state_query import StateQuerier

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

    querier = StateQuerier(REF_FRAME, AB_CORRECTION)
    if querier.load_config(config_file) is False:
        print("Failed to load config file")
        os._exit(101)

    # Curiosity landing on Mars - 2012-08-06T05:17:57
    utc = "2012-08-06T05:17:57"
    et = querier.spice.str2et(utc)
    print(f"====== Curiosity Landing: {utc} ======\n")

    mars_wrt_earth_position = querier.get_position("MARS BARYCENTER", et, "EARTH")
    if mars_wrt_earth_position is None:
        print("Failed to get PositionData for [MARS] w.r.t [EARTH]")
        os._exit(102)

    print("Mars position relative to Earth (km):")
    print(f"  X: {mars_wrt_earth_position.position[0]:.3f}")
    print(f"  Y: {mars_wrt_earth_position.position[1]:.3f}")
    print(f"  Z: {mars_wrt_earth_position.position[2]:.3f}")
    print(f"  Light time: {mars_wrt_earth_position.light_time:.3f} seconds\n")

    distance = querier.get_distance("MARS BARYCENTER", et, "EARTH")
    if distance is None:
        print("Failed to get distance from MARS to EARTH")
        os._exit(103)

    print(f"Distance Earth -> Mars: {distance:.3f} km")
    print(f"Distance Earth -> Mars: {distance / KM_PER_AU:.6f} AU\n")

    mars_wrt_earth_state = querier.get_state("MARS BARYCENTER", et, "EARTH")
    if mars_wrt_earth_state is None:
        print("Failed to get StateData for [MARS] w.r.t [EARTH]")
        os._exit(104)

    print("Mars full state relative to Earth:")
    print(f"  Position (km): [{mars_wrt_earth_state.state[0]:.1f}, {mars_wrt_earth_state.state[1]:.1f}, {mars_wrt_earth_state.state[2]:.1f}]")
    print(f"  Velocity (km/s): [{mars_wrt_earth_state.state[3]:.3f}, {mars_wrt_earth_state.state[4]:.3f}, {mars_wrt_earth_state.state[5]:.3f}]")

    querier.spice.kclear()

    print("\nDone!")


if __name__ == "__main__":
    main()
