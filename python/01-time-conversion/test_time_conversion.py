import sys
import os

from time_conversion import TimeConverter


def main():
    if len(sys.argv) < 2:
        print("Invalid arguements. Expected:")
        print("\tpython3 time_conversion.py <config-file.json>")
        os._exit(100)

    config_file = sys.argv[1]

    converter = TimeConverter()
    if converter.load_config(config_file) is False:
        print("Failed to execute TimeConverter - Failed to load config file")
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
        et = converter.convert_utc_to_et(utc, debug=True)
        converter.convert_et_calendar(et, debug=True)
        converter.convert_et_to_utc(et, debug=True)
        print()

    print("Done!")


if __name__ == "__main__":
    main()
