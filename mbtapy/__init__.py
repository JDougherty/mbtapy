import requests
import datetime
from collections import OrderedDict


class Route(object):
    def __init__(self, route_id, route_name, route_hide=False):
        self.route_id = route_id
        self.route_name = route_name
        self.route_hide = route_hide

    def __repr__(self):
        return self.route_id


class Direction(object):
    def __init__(self, direction_id, direction_name):
        self.direction_id = direction_id
        self.direction_name = direction_name

    def __repr__(self):
        return self.direction_id


class Stop(object):
    def __init__(self, stop_order, stop_id, stop_name, parent_station, parent_station_name, stop_lat, stop_lon):
        self.stop_order = stop_order
        self.stop_id = stop_id
        self.stop_name = stop_name
        self.parent_station = parent_station
        self.parent_station_name = parent_station_name
        self.stop_lat = stop_lat
        self.stop_lon = stop_lon

    def __repr__(self):
        return self.stop_id


class Trip(object):
    def __init__(self, trip_id, trip_name):
        self.trip_id = trip_id
        self.trip_name = trip_name
        self.stops = OrderedDict()

    def __repr__(self):
        return self.trip_id


class TripStop(object):
    def __init__(self, stop_sequence, stop_id, stop_name, sch_arr_dt, sch_dep_dt):
        self.stop_sequence = stop_sequence
        self.stop_id = stop_id
        self.stop_name = stop_name
        self.sch_arr_dt = sch_arr_dt
        self.sch_dep_dt = sch_dep_dt

    def __repr__(self):
        return self.stop_id

    def sch_arr_dt_datetime(self):
        return datetime.datetime.fromtimestamp(float(self.sch_arr_dt))

    def sch_dep_dt_datetime(self):
        return datetime.datetime.fromtimestamp(float(self.sch_dep_dt))


class MbtaApi(object):
    # This API key is open to all developers for use in development. It may change at any time; if it does check
    # http://realtime.mbta.com/Portal/Content/Download/APIKey.txt for a new one. Do not go into production using the
    # open development key!
    api_key = 'wX9NwuHnZU2ToO7GmGR9uw'
    api_url = 'http://realtime.mbta.com/developer/api/v2/'
    response_format = 'json'

    def __init__(self, api_key=None):
        if api_key:
            self.api_key = api_key

    def _api_call(self, **kwargs):
        function = kwargs.pop("function", "")
        if function == "":
            raise TypeError("Required kwarg `function` not provided")
        if "api_key" not in kwargs:
            kwargs["api_key"] = self.api_key
        r = requests.get(self.api_url+function, params=kwargs)
        return r.json()

    def _api_routes(self):
        return self._api_call(function="routes")

    def _api_routesbystop(self, stop):
        return self._api_call(function="routesbystop", stop=stop)

    def _api_stopsbyroute(self, route):
        return self._api_call(function="stopsbyroute", route=route)

    def _api_stopsbylocation(self, lat, lon):
        return self._api_call(function="stopsbylocation", lat=lat, lon=lon)

    # TODO: Add support for optional parameters
    def _api_schedulebystop(self, stop):
        return self._api_call(function="schedulebystop", stop=stop)

    # TODO: Add support for optional parameters
    def _api_schedulebyroute(self, route):
        return self._api_call(function="schedulebyroute", route=route)

    # TODO: Add support for optional parameters
    def _api_schedulebytrip(self, trip):
        return self._api_call(function="schedulebytrip", trip=trip)

    def _api_predictionsbystop(self, stop, include_access_alerts=False, include_service_alerts=True):
        return self._api_call(function="predictionsbystop", stop=stop, include_access_alerts=include_access_alerts,
                              include_service_alerts=include_service_alerts)

    def _api_predictionsbyroute(self, route, include_access_alerts=False, include_service_alerts=True):
        return self._api_call(function="predictionsbyroute", route=route, include_access_alerts=include_access_alerts,
                              include_service_alerts=include_service_alerts)

    def _api_vehiclesbyroute(self, route):
        return self._api_call(function="vehiclesbyroute", route=route)

    def _api_predictionsbytrip(self, trip):
        return self._api_call(function="predictionsbytrip", trip=trip)

    def _api_vehiclesbytrip(self, trip):
        return self._api_call(function="vehiclesbytrip", trip=trip)

    def _api_alerts(self):
        return self._api_call(function="alerts")

    def get_routes_by_mode(self, mode_name):
        """
        Returns a list of routes for a given mode

        TODO: This function needs to be redesigned. Firstly, mode names are not unique (e.g, "Subway" is used more than
         once.
        """
        result = []
        routes_json = self._api_routes()
        modes = routes_json['mode']
        mode = None
        for m in modes:
            if m["mode_name"] == mode_name:
                mode = m
                break
        if not mode:
            return None
        routes = mode["route"]
        for route in routes:
            result.append(Route(route['route_id'], route['route_name'], "route_hide" in route))
        return result

    def get_stops_by_route(self, route):
        """
        Returns a dictionary keyed by Direction objects for a given Route. The values are lists of Stop objects for
        each Direction.
        """
        result = {}
        stops_json = self._api_stopsbyroute(route.route_id)
        directions = stops_json['direction']
        for direction in directions:
            direction_obj = Direction(direction['direction_id'], direction['direction_name'])
            result[direction_obj] = []
            stops = direction["stop"]
            for stop in stops:
                stop_obj = Stop(stop["stop_order"], stop["stop_id"], stop["stop_name"], stop["parent_station"],
                                stop["parent_station_name"], stop["stop_lat"], stop["stop_lon"])
                result[direction_obj].append(stop_obj)
        return result

    def get_schedule_by_route(self, route):
        """
        Returns a dictionary keyed by Direction objects for a given Route. The values are lists of Trip objects for
        each Direction.
        """
        result = {}
        schedules_json = self._api_schedulebyroute(route.route_id)
        directions = schedules_json['direction']
        for direction in directions:
            direction_obj = Direction(direction['direction_id'], direction['direction_name'])
            result[direction_obj] = []
            for trip in direction['trip']:
                trip_obj = Trip(trip["trip_id"], trip["trip_name"])
                for tripstop in trip["stop"]:
                    tripstop_obj = TripStop(tripstop["stop_sequence"], tripstop["stop_id"], tripstop["stop_name"],
                                            tripstop["sch_arr_dt"], tripstop["sch_dep_dt"])
                    trip_obj.stops[tripstop_obj.stop_id] = tripstop_obj
                result[direction_obj].append(trip_obj)
        return result
