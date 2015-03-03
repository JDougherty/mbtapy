import requests
import datetime


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
        self.stops = []

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

    def __init__(self, api_key=None, response_format=None):
        if api_key:
            self.api_key = api_key
        if response_format:
            self.response_format = response_format

    def _api_routes(self):
        function = 'routes'
        params = {'api_key': self.api_key, 'format': self.response_format}
        r = requests.get(self.api_url+function, params=params)
        return r.json()

    def _api_stopsbyroute(self, route_id):
        function = 'stopsbyroute'
        params = {'api_key': self.api_key, 'format': self.response_format, 'route': route_id}
        r = requests.get(self.api_url+function, params=params)
        return r.json()

    def _api_schedulebyroute(self, route_id):
        function = "schedulebyroute"
        params = {'api_key': self.api_key, 'format': self.response_format, 'route': route_id}
        r = requests.get(self.api_url+function, params=params)
        return r.json()

    def get_commuter_rail_routes(self):
        """
        Returns a list of routes on the Commuter Rail
        """
        result = []
        routes_json = self._api_routes()
        modes = routes_json['mode']
        cr_mode = None
        for mode in modes:
            if mode["mode_name"] == "Commuter Rail":
                cr_mode = mode
                break
        if not cr_mode:
            return None
        routes = cr_mode["route"]
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
                    trip_obj.stops.append(tripstop_obj)
                result[direction_obj].append(trip_obj)
        return result