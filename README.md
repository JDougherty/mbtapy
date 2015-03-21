# MBTApy

## Description
MBTApy is a wrapper around the MBTA-REALTIME API (v2)

## Dependencies
See `requirements.txt`

## Documentation
Detailed documentation is not yet available. 

Example code to get all upcoming trips for a given mode of transportation:

```python  

    import mbtapy
    apiobj = mbtapy.MbtaApi()
    routes = apiobj.get_routes_by_mode("Commuter Rail")
    for route in routes:
        schedules = apiobj.get_schedule_by_route(route)
        print "Route: %s" % route
        print "  Upcoming schedules:"
        for direction in schedules:
            print "  Direction: %s" % direction.direction_name
            for trip in schedules[direction]:
                print "    ", trip.trip_name
                for stop_id, tripstop_obj in trip.stops.items():
                    print "      %s (%s)" % (tripstop_obj.stop_name, tripstop_obj.sch_arr_dt_datetime())

```

The API specification is available directly from the [MBTA](http://realtime.mbta.com/Portal/Content/Documents/MBTA-realtime_APIDocumentation_v2_0_1_2014-09-08.pdf).



## Licensing and Copyright
MBTApy is licensed under the Apache License v2.0. See included `LICENSE` for more information. 

Copyright&copy; 2015 Joseph W. Dougherty