import os
import sys

from angular_seperation import AngularSeparation

def main():
    if len(sys.argv) < 2:
        print("Invalid arguments. Expected:")
        print("\tpython3 angular_separation.py <config-file.json>")
        os._exit(100)

    config_file = sys.argv[1]

    separator = AngularSeparation()
    if separator.load_config(config_file) is False:
        print("Failed to load config file")
        os._exit(101)

    # OSIRIS-REx touches Bennu - 2020-10-20T23:00:00
    utc = "2020-10-20T23:00:00"
    print(f"====== OSIRIS-REx Touches Bennu: {utc} ======\n")

    et = separator.spice.str2et(utc)

    # Angular separation between planets as seen from Earth
    bodies = ["MARS BARYCENTER", "JUPITER BARYCENTER", "SATURN BARYCENTER", "VENUS"]
    print("Angular separation from Sun as seen from Earth:")
    for body in bodies:
        try:
            angle = separator.get_separation(body, "SUN", "EARTH", et)
            dist = separator.get_distance_au(body, "EARTH", et)
            print(f"  {body:<25} {angle:>8.3f} deg   {dist:.3f} AU away")
        except Exception as e:
            print(f"  {body:<25} Error: {str(e)}")

    # Phase angles for inner planets
    print("\nSun phase angles (sun-target-observer, observer=EARTH):")
    phase_bodies = ["MARS BARYCENTER", "VENUS", "JUPITER BARYCENTER"]
    for body in phase_bodies:
        try:
            phase = separator.get_sun_phase_angle(body, "EARTH", et)
            print(f"  {body:<25} {phase:>8.3f} deg")
        except Exception as e:
            print(f"  {body:<25} Error: {str(e)}")

    # Angular separation between Mars and Jupiter as seen from Earth
    mars_jup = separator.get_separation("MARS BARYCENTER", "JUPITER BARYCENTER", "EARTH", et)
    print(f"\nAngular separation Mars-Jupiter as seen from Earth: {mars_jup:.3f} deg")

    separator.spice.kclear()
    print("\nDone!")


if __name__ == "__main__":
    main()
