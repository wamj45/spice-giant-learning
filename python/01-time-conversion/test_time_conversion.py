import sys
import os

from spice_wrapper.spice_wrapper import SpiceWrapper

'''
Convert UTC time to ET time.
Source: https://spiceypy.readthedocs.io/en/main/remote_sensing.html#solution
'''


def main():
    if len(sys.argv) < 2:
        print("Invalid arguements. Expected:")
        print("\tpython3 test_time_conversion.py <config-file.json>")
        os._exit(100)

    config_file = sys.argv[1]

    wrapper = SpiceWrapper()
    if wrapper.initialize(config_file) is False:
        print("Failed to initialize SpiceWrapper")
        os._exit(101)

    TEST_TIMES = [
        "2004-01-04T04:35:00",
        "2011-05-01T12:00:00",
        "2012-08-06T05:17:57",
        "2015-07-14T11:49:57",
        "2020-10-20T23:00:00",
        "2023-09-24T14:52:00",
        "2004 jun 11 19:32:00"
    ]

    for utc in TEST_TIMES:
        print(f"Testing with UTC: [{utc}]")
        et = wrapper.convert_utc_to_et(utc, verbose=True)
        wrapper.convert_et_calendar(et, verbose=True)
        wrapper.convert_et_to_utc(et, verbose=True)
        print()

    wrapper.clear()

    print("Done!")


if __name__ == "__main__":
    main()
