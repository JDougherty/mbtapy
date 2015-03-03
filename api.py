import requests

api_url = 'http://realtime.mbta.com/developer/api/v2/'

# This API key is open to all developers for use in development. It may change at any time; if it does check
# http://realtime.mbta.com/Portal/Content/Download/APIKey.txt for a new one. Do not go into production using the open
# development key!


class Route(object):
    def __init__(self, route_id, route_name, route_hide=False):
        self.route_id = route_id
        self.route_name = route_name
        self.route_hide = route_hide

    def __repr__(self):
        return self.route_id

class MbtaApi(object):
    # This API key is open to all developers for use in development. It may change at any time; if it does check
    # http://realtime.mbta.com/Portal/Content/Download/APIKey.txt for a new one. Do not go into production using the
    # open development key!
    api_key = 'wX9NwuHnZU2ToO7GmGR9uw'

    def __init__(self, api_key=None):
        if api_key:
            self.api_key = api_key

    def _api_routes(self,format='json'):
        function = 'routes'
        params = {'api_key': self.api_key, 'format': format}
        r = requests.get(api_url+function, params=params)
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
            result.append(Route(route['route_id'],
                                route['route_name'],
                                "route_hide" in route)
                                )
        return result


