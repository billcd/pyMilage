import math
from collections import namedtuple


LatLngAlt = namedtuple('LatLngAlt', 'lat, lng, alt')


def haversine_distance(origin, destination):
    """ Haversine formula to calculate the distance between two lat/long points on a sphere """
    # https://news.ycombinator.com/item?id=9282102
    # radius = 6371 # FAA approved globe radius in km
    radius = 3958.756 * 5280

    dlat = math.radians(destination.lat - origin.lat)
    dlon = math.radians(destination.lng - origin.lng)

    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(origin.lat)) * math.cos(
        math.radians(destination.lat)) * math.sin(dlon / 2) * math.sin(dlon / 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    d = radius * c

    # Return distance in feet
    return int(math.floor(d))


def compass_bearing(pointA, pointB):
    # https://gist.github.com/jeromer/2005586
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """

    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")
    """
    
    lat1 = math.radians(pointA.lat)
    lat2 = math.radians(pointB.lat)

    diff_long = math.radians(pointB.lng - pointA.lng)

    x = math.sin(diff_long) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                                           * math.cos(lat2) * math.cos(diff_long))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

