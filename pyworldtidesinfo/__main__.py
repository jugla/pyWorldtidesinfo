"""Main to use the atome library."""
import argparse
import sys
import time
from datetime import datetime, timedelta


from pyworldtidesinfo.worldtidesinfo_server import (
    PLOT_CURVE_UNIT_FT,
    WorldTidesInfo_server,
    give_info_from_raw_data,
)


def next_tide_state(tide_info, current_time):
    """Compute next tide state."""
    # Get next tide time
    next_tide = tide_info.give_next_tide_in_epoch(current_time)
    if next_tide.get("error") is None:
        tidetime = time.strftime("%H:%M", time.localtime(next_tide.get("tide_time")))
        tidetype = next_tide.get("tide_type")
        tide_string = f"{tidetype} tide at {tidetime}"
        return tide_string
    else:
        return None


def main():
    """Define the main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key", required=True, help="WorldidesInfo Key")
    parser.add_argument("-l", "--lat", required=True, help="latitude")
    parser.add_argument("-L", "--long", required=True, help="longitude")

    args = parser.parse_args()

    # Least Astronomic Tide
    vertical_ref = "LAT"
    # 20km
    server_tide_station_distance = 20
    plot_color = "2,102,255"
    plot_background = "255,255,255"
    unit_curve_picture = PLOT_CURVE_UNIT_FT
    # 1 day of prediction
    tide_prediction_duration = 1

    worldtidesinfo_server = WorldTidesInfo_server(
        args.key,
        args.lat,
        args.long,
        vertical_ref,
        server_tide_station_distance,
        tide_prediction_duration,
        plot_color,
        plot_background,
        unit_curve_picture,
    )
    # example to retrieve applied parameter:
    # worldtidesinfo_server_parameter = worldtidesinfo_server.give_parameter()

    if worldtidesinfo_server.retrieve_tide_station():
        init_data = worldtidesinfo_server.retrieve_tide_station_raw_data()

    # retrieve the datum
    datum_flag = True
    if worldtidesinfo_server.retrieve_tide_height_over_one_day(datum_flag):
        data = worldtidesinfo_server.retrieve_tide_raw_data()
        # process information
        tide_info = give_info_from_raw_data(data)
        datum_content = tide_info.give_datum()

    if init_data is not None and data is not None and datum_content is not None:
        # example to retrieve init data:
        # init_tide_info = give_info_from_raw_data(init_data)
        tide_info = give_info_from_raw_data(data)

        current_time = time.time()
        current_height_value = tide_info.give_current_height_in_UTC(current_time)
        print("current height :", current_height_value.get("current_height"))
        print("next tide :", next_tide_state(tide_info, current_time))
    else:
        print("no data")
        return 1


if __name__ == "__main__":
    sys.exit(main())
