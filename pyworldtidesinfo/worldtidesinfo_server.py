"""gather function objects thal allow to manage Word Tides Info server API V2."""
# python library
# Python library
import logging
import time

import requests

_LOGGER = logging.getLogger(__name__)


# Component library
PLOT_CURVE_UNIT_FT = "feet"
PLOT_CURVE_UNIT_M = "meters"
# This parameter is directly used in URL
SERVER_API_VERSION = "v3"


class Server_Parameter:
    """Manage Parameter."""

    def __init__(
        self,
        key,
        lat,
        lon,
        vertical_ref,
        tide_station_distance,
        tide_prediction_duration,
        plot_color,
        plot_background,
        unit_curve_picture,
    ):
        """Initialize the parameters."""
        self._version = SERVER_API_VERSION
        self._key = key
        self._lat = lat
        self._lon = lon
        self._vertical_ref = vertical_ref
        self._tide_station_distance = tide_station_distance
        self._tide_prediction_duration = tide_prediction_duration
        self._plot_color = plot_color
        self._plot_background = plot_background
        self._unit_curve_picture = unit_curve_picture

    def compare_parameter(self, parameter):
        """Compare the parameter given to the stored ones."""
        result = False
        try:
            if (
                parameter._version == self._version
                and parameter._key == self._key
                and parameter._lat == self._lat
                and parameter._lon == self._lon
                and parameter._vertical_ref == self._vertical_ref
                and parameter._tide_station_distance == self._tide_station_distance
                and parameter._tide_prediction_duration
                == self._tide_prediction_duration
                and parameter._plot_color == self._plot_color
                and parameter._plot_background == self._plot_background
                and parameter._unit_curve_picture == self._unit_curve_picture
            ):
                result = True
            else:
                _LOGGER.debug(
                    "Parameter differ : lat recorded %s vs expected %s",
                    parameter._lat,
                    self._lat,
                )
                _LOGGER.debug(
                    "Parameter differ : lon recorded %s vs expected %s",
                    parameter._lon,
                    self._lon,
                )
                result = False
        except:
            result = False
        return result

    def get_latitude(self):
        """Retrieve the ref latitude."""
        return self._lat

    def get_longitude(self):
        """Retrieve the ref longitude."""
        return self._lon

    def get_tide_station_distance(self):
        """Retrieve the tide station distance given o fetch tide station."""
        return self._tide_station_distance

    def change_ref_point(self, lat, lon):
        """Set a new reference lat/long."""
        self._lat = lat
        self._lon = lon


class WorldTidesInfo_server:
    """Class to manage the Word Tide Info server."""

    def __init__(
        self,
        key,
        lat,
        lon,
        vertical_ref,
        tide_station_distance,
        tide_prediction_duration,
        plot_color,
        plot_background,
        unit_curve_picture,
    ):
        """Initialize the parameters."""
        # parameter
        self._Server_Parameter = Server_Parameter(
            key,
            lat,
            lon,
            vertical_ref,
            tide_station_distance,
            tide_prediction_duration,
            plot_color,
            plot_background,
            unit_curve_picture,
        )

        # information from server
        self.last_tide_station_raw_data = None
        self.last_tide_station_request_time = None
        self.last_tide_station_request_credit = 0
        self.last_tide_station_request_error_value = None
        # information from server
        self.last_tide_raw_data = None
        self.last_tide_raw_data_request_time = None
        self.last_tide_request_credit = 0
        self.last_tide_request_error_value = None

    def change_ref_point(self, lat, lon):
        """Change the reference point."""
        self._Server_Parameter.change_ref_point(lat, lon)

    def give_parameter(self):
        """Give the parameter."""
        return self._Server_Parameter

    def retrieve_tide_station_credit(self):
        """Give the last credit used (tide station)."""
        return self.last_tide_station_request_credit

    def retrieve_tide_station_err_value(self):
        """Give the last error (tide station)."""
        return self.last_tide_station_request_error_value

    def retrieve_tide_station_raw_data(self):
        """Give the last raw data (tide station)."""
        return self.last_tide_station_raw_data

    def retrieve_tide_station_request_time(self):
        """Give the last request time (tide station)."""
        return self.last_tide_station_request_time

    def retrieve_tide_station(self):
        """Retrieve information related tide station only."""
        current_time = time.time()
        data_has_been_received = False
        data = None

        resource = (
            "https://www.worldtides.info/api/{}?stations"
            "&key={}&lat={}&lon={}&stationDistance={}"
        ).format(
            self._Server_Parameter._version,
            self._Server_Parameter._key,
            self._Server_Parameter._lat,
            self._Server_Parameter._lon,
            self._Server_Parameter._tide_station_distance,
        )
        try:
            data_get = requests.get(resource, timeout=10)
            if data_get.status_code == 200:
                data = data_get.json()
                data_has_been_received = True
                error_value = None
            else:
                error_value = data_get.status_code
                data_has_been_received = False
                data = None

        except ValueError as err:
            error_value = err.args
            data_has_been_received = False
            data = None

        # information from server
        self.last_tide_station_raw_data = data
        self.last_tide_station_request_time = current_time
        if data_has_been_received:
            self.last_tide_station_request_credit = data["callCount"]
        else:
            self.last_tide_station_request_credit = 0
        self.last_tide_station_request_error_value = error_value

        return data_has_been_received

    def retrieve_tide_credit(self):
        """Give the last credit used (tide info)."""
        return self.last_tide_request_credit

    def retrieve_tide_err_value(self):
        """Give the last error (tide info)."""
        return self.last_tide_request_error_value

    def retrieve_tide_raw_data(self):
        """Give the last raw data (tide info)."""
        return self.last_tide_raw_data

    def retrieve_tide_request_time(self):
        """Give the last request time (tide info)."""
        return self.last_tide_request_time

    def retrieve_tide_height_over_one_day(self, datum_flag):
        """Retrieve information related to tide."""
        current_time = time.time()
        data_has_been_received = False
        data = None

        datums_string = ""
        if datum_flag:
            datums_string = "&datums"

        # prediction + 1 day --> to manage midnight
        tide_prediction_total_duration = (
            self._Server_Parameter._tide_prediction_duration + 1
        )

        # 3 days --> to manage one day beyond midnight and one before midnight
        resource = (
            "https://www.worldtides.info/api/{}?extremes&days={}&date=today&heights&plot&timemode=24&step=900"
            "&key={}&lat={}&lon={}&datum={}&stationDistance={}&color={}&background={}&units={}{}"
        ).format(
            self._Server_Parameter._version,
            tide_prediction_total_duration,
            self._Server_Parameter._key,
            self._Server_Parameter._lat,
            self._Server_Parameter._lon,
            self._Server_Parameter._vertical_ref,
            self._Server_Parameter._tide_station_distance,
            self._Server_Parameter._plot_color,
            self._Server_Parameter._plot_background,
            self._Server_Parameter._unit_curve_picture,
            datums_string,
        )
        try:
            data_get = requests.get(resource, timeout=10)
            if data_get.status_code == 200:
                data = data_get.json()
                data_has_been_received = True
                error_value = None
            else:
                error_value = data_get.status_code
                data_has_been_received = False
                data = None

        except ValueError as err:
            data = None
            data_has_been_received = False
            error_value = err.args
        # information from server
        self.last_tide_raw_data = data
        self.last_tide_request_time = current_time
        if data_has_been_received:
            self.last_tide_request_credit = data["callCount"]
        else:
            self.last_tide_request_credit = 0
        self.last_tide_request_error_value = error_value

        return data_has_been_received


class give_info_from_raw_data:
    """Give a set of function to decode retrieved data."""

    def __init__(self, data):
        """Set data."""
        self._data = data

    def give_tide_in_epoch(self, current_epoch_time, next_tide_flag):
        """Give Tide info from X seconds from epoch."""
        if self._data is None:
            return {"error": "no data"}

        current_time = int(current_epoch_time)
        next_tide = 0
        for tide_index in range(len(self._data["extremes"])):
            if self._data["extremes"][tide_index]["dt"] < current_time:
                next_tide = tide_index
        if next_tide_flag:
            if self._data["extremes"][next_tide]["dt"] < current_time:
                next_tide = next_tide + 1
        if next_tide >= len(self._data["extremes"]):
            return {"error": "no date in future"}
        if next_tide_flag is False:
            if self._data["extremes"][next_tide]["dt"] > current_time:
                return {"error": "no date in past"}

        tide_time = self._data["extremes"][next_tide]["dt"]

        tide_type = "None"
        if "High" in str(self._data["extremes"][next_tide]["type"]):
            tide_type = "High"
        elif "Low" in str(self._data["extremes"][next_tide]["type"]):
            tide_type = "Low"
        else:
            tide_type = "None"

        return {"tide_type": tide_type, "tide_time": tide_time}

    def give_next_tide_in_epoch(self, current_epoch_time):
        """Give Next Tide info from X seconds from epoch."""
        next_tide_flag = True
        return self.give_tide_in_epoch(current_epoch_time, next_tide_flag)

    def give_previous_tide_in_epoch(self, current_epoch_time):
        """Give Previous Tide info from X seconds from epoch."""
        next_tide_flag = False
        return self.give_tide_in_epoch(current_epoch_time, next_tide_flag)

    def give_vertical_ref(self):
        """Give Vertical Ref (LAT,...)."""
        if self._data is None:
            return {"error": "no data"}
        elif "responseDatum" in self._data:
            return {"vertical_ref": self._data["responseDatum"]}
        else:
            return {"error": "no vertical ref"}

    def give_tidal_station_used(self):
        """Give Tidal Station."""
        if self._data is None:
            return {"error": "no data"}
        elif "station" in self._data:
            return {"station": self._data["station"]}
        else:
            return {"error": "no reference station used"}

    def give_high_low_tide_in_UTC(self, current_epoch_time, next_tide_flag):
        """Give High/Low Tide info from X seconds from epoch."""
        if self._data is None:
            return {"error": "no data"}

        current_time = int(current_epoch_time)

        # Next tide
        next_tide = 0
        for tide_index in range(len(self._data["extremes"])):
            if self._data["extremes"][tide_index]["dt"] < current_time:
                next_tide = tide_index

        # Managed the case where next_tide has not been updated : if next_tide=0 perform a check
        if next_tide_flag:
            if self._data["extremes"][next_tide]["dt"] < current_time:
                next_tide = next_tide + 1

        if next_tide >= len(self._data["extremes"]):
            return {"error": "no date in future"}

        # As we are looking also for next one
        if (next_tide + 1) >= len(self._data["extremes"]):
            return {"error": "no date in future for next one"}

        if not next_tide_flag:
            if self._data["extremes"][next_tide]["dt"] > current_time:
                return {"error": "no date in past"}

        if "High" in str(self._data["extremes"][next_tide]["type"]):
            high_tide_time_utc = self._data["extremes"][next_tide]["date"]
            high_tide_time_epoch = self._data["extremes"][next_tide]["dt"]
            high_tide_height = self._data["extremes"][next_tide]["height"]

            low_tide_time_utc = self._data["extremes"][next_tide + 1]["date"]
            low_tide_time_epoch = self._data["extremes"][next_tide + 1]["dt"]
            low_tide_height = self._data["extremes"][next_tide + 1]["height"]

        elif "Low" in str(self._data["extremes"][next_tide]["type"]):
            high_tide_time_utc = self._data["extremes"][next_tide + 1]["date"]
            high_tide_time_epoch = self._data["extremes"][next_tide + 1]["dt"]
            high_tide_height = self._data["extremes"][next_tide + 1]["height"]

            low_tide_time_utc = self._data["extremes"][next_tide]["date"]
            low_tide_time_epoch = self._data["extremes"][next_tide]["dt"]
            low_tide_height = self._data["extremes"][next_tide]["height"]

        return {
            "high_tide_time_utc": high_tide_time_utc,
            "high_tide_time_epoch": high_tide_time_epoch,
            "high_tide_height": high_tide_height,
            "low_tide_time_utc": low_tide_time_utc,
            "low_tide_time_epoch": low_tide_time_epoch,
            "low_tide_height": low_tide_height,
        }

    def give_tide_extrema_within_time_frame(self, epoch_frame_min, epoch_frame_max):
        """Retrieve data extrema from frame_min to frame_max."""
        if self._data is None:
            return {"error": "no data"}

        extrema_value = []
        extrema_time = []
        extrema_type = []
        for extrema_index in range(len(self._data["extremes"])):
            extrema_current_value = self._data["extremes"][extrema_index]["height"]
            extrema_current_time = self._data["extremes"][extrema_index]["dt"]
            extrema_current_type = self._data["extremes"][extrema_index]["type"]
            # retrieve height and time
            if (extrema_current_time > epoch_frame_min) and (
                extrema_current_time < epoch_frame_max
            ):
                extrema_value.append(extrema_current_value)
                extrema_time.append(extrema_current_time)
                extrema_type.append(extrema_current_type)
        return {
            "extrema_value": extrema_value,
            "extrema_epoch": extrema_time,
            "extrema_type": extrema_type,
        }

    def give_next_high_low_tide_in_UTC(self, current_epoch_time):
        """Give Next High/Low Tide info from X seconds from epoch."""
        next_tide_flag = True
        return self.give_high_low_tide_in_UTC(current_epoch_time, next_tide_flag)

    def give_current_high_low_tide_in_UTC(self, current_epoch_time):
        """Give Previous High/Low Tide info from X seconds from epoch."""
        next_tide_flag = False
        return self.give_high_low_tide_in_UTC(current_epoch_time, next_tide_flag)

    def give_current_height_in_UTC(self, current_epoch_time):
        """Give current height at X seconds from epoch."""
        current_time = int(current_epoch_time)

        if self._data is None:
            return {"error": "no data"}

        # The height
        current_height_index = 0
        for height_index in range(len(self._data["heights"])):
            if self._data["heights"][height_index]["dt"] < current_time:
                current_height_index = height_index
        current_height = self._data["heights"][current_height_index]["height"]
        current_height_utc = self._data["heights"][current_height_index]["date"]
        current_height_epoch = self._data["heights"][current_height_index]["dt"]

        return {
            "current_height": current_height,
            "current_height_utc": current_height_utc,
            "current_height_epoch": current_height_epoch,
        }

    def give_tide_prediction_within_time_frame(self, epoch_frame_min, epoch_frame_max):
        """Retrieve data from frame_min to frame_max."""
        if self._data is None:
            return {"error": "no data"}

        height_value = []
        height_time = []
        for height_index in range(len(self._data["heights"])):
            height_current_value = self._data["heights"][height_index]["height"]
            height_current_time = self._data["heights"][height_index]["dt"]
            # retrieve height and time
            if (height_current_time > epoch_frame_min) and (
                height_current_time < epoch_frame_max
            ):
                height_value.append(height_current_value)
                height_time.append(height_current_time)
        return {
            "height_value": height_value,
            "height_epoch": height_time,
        }

    def give_station_list_info(self):
        """Give Tide Station List."""
        if self._data is None:
            return None
        return self._data["stations"]

    def give_used_station_info(self):
        """Give used tidal station info."""
        if self._data is None:
            return {"error": "no_data"}

        if len(self._data["stations"]) > 0:
            return {
                "tide_station_used_name": self._data["stations"][0]["name"],
                "tide_station_lat": self._data["stations"][0]["lat"],
                "tide_station_long": self._data["stations"][0]["lon"],
            }
        return {"error": "used station not found"}

    def give_used_station_info_from_name(self, station_name):
        """Give used tidal station info."""
        if station_name is None:
            return {"error": "no_station_name"}

        if self._data is None:
            return {"error": "no_data"}

        tide_station_index = 0
        tide_station_index_found = False

        if len(self._data["stations"]) > 0:
            for name_index in range(len(self._data["stations"])):
                if self._data["stations"][name_index]["name"] == station_name:
                    tide_station_index = name_index
                    tide_station_index_found = True
        if tide_station_index_found is True:
            return {
                "tide_station_used_name": self._data["stations"][tide_station_index][
                    "name"
                ],
                "tide_station_lat": self._data["stations"][tide_station_index]["lat"],
                "tide_station_long": self._data["stations"][tide_station_index]["lon"],
                "tide_station_timezone": self._data["stations"][tide_station_index][
                    "timezone"
                ],
            }
        return {"error": "used station detailed not found"}

    def give_station_around_info(self):
        """Give tidal station around info."""
        if self._data is None:
            return {"error": "no_data"}

        station_around_nb = len(self._data["stations"])
        station_around_name = ""
        if len(self._data["stations"]) > 0:
            station_around_name = ""
            for name_index in range(len(self._data["stations"])):
                station_around_name = (
                    station_around_name
                    + "; "
                    + self._data["stations"][name_index]["name"]
                )
        else:
            station_around_name = "None"

        return {
            "station_around_nb": station_around_nb,
            "station_around_name": station_around_name,
        }

    def give_nearest_station_time_zone(self):
        """Give the nearest tide station time zone."""
        if self._data is None:
            return {"error": "no_data"}
        if len(self._data["stations"]) > 0:
            return {"time_zone": self._data["stations"][0]["timezone"]}
        else:
            return {"error": "no station around"}

    def give_datum(self):
        """Give the datum ie different height LAT/CD/MSL/... ."""
        if self._data is None:
            return {"error": "no data"}
        elif "datums" in self._data:
            return {"datums": self._data["datums"]}
        else:
            return {"error": "no_datums"}

    def give_plot_picture_without_header(self):
        """Give picture in base 64 without the format header."""
        if self._data is None:
            return {"error": "no data"}
        elif "plot" in self._data:
            std_string = "data:image/png;base64,"
            str_to_convert = self._data["plot"][
                len(std_string) : len(self._data["plot"])
            ]
            return {"image": str_to_convert}
        else:
            return {"error": "no_image"}


class give_info_from_raw_datums_data:
    """Decode datum information."""

    def __init__(self, datums_data):
        """Set data."""
        self._datums_data = datums_data

    def give_mean_water_spring_datums_offset(self):
        """Retrieve MWS mean water spring height ."""
        if self._datums_data is None:
            return {"error": "no data"}
        MHW_index = 0
        MLW_index = 0
        for ref_index in range(len(self._datums_data)):
            if self._datums_data[ref_index]["name"] == "MHWS":
                MHW_index = ref_index
            if self._datums_data[ref_index]["name"] == "MLWS":
                MLW_index = ref_index
        datum_offset_MHWS = self._datums_data[MHW_index]["height"]
        datum_offset_MLWS = self._datums_data[MLW_index]["height"]

        return {
            "datum_offset_MHWS": datum_offset_MHWS,
            "datum_offset_MLWS": datum_offset_MLWS,
        }


class give_info_from_raw_data_N_and_N_1:
    """Give a set of function to decode info from current or previous data."""

    def __init__(self, data, previous_data):
        """Set the flip flop data."""
        self._info = give_info_from_raw_data(data)
        self._previous_info = give_info_from_raw_data(previous_data)

    def give_current_height_in_UTC(self, current_epoch_time):
        """Give current height tide in current or previous data ."""
        result = self._info.give_current_height_in_UTC(current_epoch_time)
        if result.get("error") is None:
            return result
        else:
            previous_result = self._previous_info.give_current_height_in_UTC(
                current_epoch_time
            )
            return previous_result

    def give_high_low_tide_in_UTC(self, current_epoch_time, next_tide_flag):
        """Give high low tide in current or previous data ."""
        result = self._info.give_high_low_tide_in_UTC(
            current_epoch_time, next_tide_flag
        )
        if result.get("error") is None:
            return result
        else:
            previous_result = self._previous_info.give_high_low_tide_in_UTC(
                current_epoch_time, next_tide_flag
            )
            return previous_result

    def give_next_high_low_tide_in_UTC(self, current_epoch_time):
        """Give next high low tide in current or previous data ."""
        next_tide_flag = True
        return self.give_high_low_tide_in_UTC(current_epoch_time, next_tide_flag)

    def give_current_high_low_tide_in_UTC(self, current_epoch_time):
        """Give previous high low tide in current or previous data ."""
        next_tide_flag = False
        return self.give_high_low_tide_in_UTC(current_epoch_time, next_tide_flag)

    def give_tide_in_epoch(self, current_epoch_time, next_tide_flag):
        """Give tide in current or previous data ."""
        result = self._info.give_tide_in_epoch(current_epoch_time, next_tide_flag)
        if result.get("error") is None:
            return result
        else:
            previous_result = self._previous_info.give_tide_in_epoch(
                current_epoch_time, next_tide_flag
            )
            return previous_result

    def give_next_tide_in_epoch(self, current_epoch_time):
        """Give next tide in current or previous data ."""
        next_tide_flag = True
        return self.give_tide_in_epoch(current_epoch_time, next_tide_flag)

    def give_previous_tide_in_epoch(self, current_epoch_time):
        """Give previous tide in current or previous data ."""
        next_tide_flag = False
        return self.give_tide_in_epoch(current_epoch_time, next_tide_flag)

    def give_vertical_ref(self):
        """Give vertical ref in current or previous data ."""
        result = self._info.give_vertical_ref()
        if result.get("error") is None:
            return result
        else:
            previous_result = self._previous_info.give_vertical_ref()
            return previous_result

    def give_tidal_station_used(self):
        """Give tidal station used in current or previous data ."""
        result = self._info.give_tidal_station_used()
        if result.get("error") is None:
            return result
        else:
            previous_result = self._previous_info.give_tidal_station_used()
            return previous_result

    def give_nearest_station_time_zone(self):
        """Give tidal station time zone in current or previous data ."""
        result = self._info.give_nearest_station_time_zone()
        if result.get("error") is None:
            return result
        else:
            previous_result = self._previous_info.give_nearest_station_time_zone()
            return previous_result

    def give_datum(self):
        """Give tidal datum in current or previous data ."""
        result = self._info.give_datum()
        if result.get("error") is None:
            return result
        else:
            previous_result = self._previous_info.give_datum()
            return previous_result

    def give_plot_picture_without_header(self):
        """Give plot picture in current or previous data ."""
        result = self._info.give_plot_picture_without_header()
        if result.get("error") is None:
            return result
        else:
            previous_result = self._previous_info.give_plot_picture_without_header()
            return previous_result
