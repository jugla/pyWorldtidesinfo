"""Main to use the atome library."""
import argparse
import sys
import time
from datetime import datetime, timedelta


from pyworltidesinfo.worldtidesinfo_server import (
    PLOT_CURVE_UNIT_FT,
    WorldTidesInfo_server,
    give_info_from_raw_data,
)

def main():
    """Define the main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key", required=True, help="WorldidesInfo Key")
    parser.add_argument("-l", "--lat", required=True, help="latitude")
    parser.add_argument("-L", "--long", required=True, help="logitude")

    args = parser.parse_args()

    #Least Astronomic Tide
    vertical_ref="LAT"
    #20km
    server_tide_station_distance = 20
    plot_color = "2,102,255"
    plot_background = "255,255,255"
    unit_curve_picture = PLOT_CURVE_UNIT_FT

    worldtidesinfo_server = WorldTidesInfo_server(
            args.key,
            args.lat,
            args.lon,
            vertical_ref,
            server_tide_station_distance,
            plot_color,
            plot_background,
            unit_curve_picture,
    )
    worldtidesinfo_server_parameter = worldtidesinfo_server.give_parameter()

    if worldtidesinfo_server.retrieve_tide_station():
        init_data = worldtidesinfo_server.retrieve_tide_station_raw_data()
    #retrieve the datum
    datum_flag = True
    if self._worldtidesinfo_server.retrieve_tide_height_over_one_day(datum_flag):
        data = self._worldtidesinfo_server.retrieve_tide_raw_data()
        # process information
        tide_info = give_info_from_raw_data(data)
        datum_content = tide_info.give_datum()

    if (init_data is not None
    and data is not None
    and datum_content is not None):
       init_tide_info = give_info_from_raw_data(init_data)
       tide_info = give_info_from_raw_data(data)

       current_time = time.time()
       current_height_value = tide_info.give_current_height_in_UTC(current_time)
       print ("current height %s" , current_height_value.get("current_height"))
       print ("next tide %s", next_tide_state(tide_info, current_time))
    else:
       print ("no data")
       return 1


if __name__ == "__main__":
    sys.exit(main())

