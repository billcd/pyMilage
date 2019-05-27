from CsvTools import csv_to_list_of_dicts
from GpsTools import haversine_distance, LatLngAlt


class GpsPoint:
    """ Object is a single GPS point for a single user. """
    username = None
    date = None
    time = None
    lat_lng_alt = None

    def __init__(self, username, date, time, lat_lng_alt):
        self.username = username
        self.date = date
        self.time = time
        self.lat_lng_alt = lat_lng_alt

    @staticmethod
    def distance_between_points(points):
        distance = 0
        for num, point in enumerate(points):
            try:
                distance += haversine_distance(point.lat_lng_alt, points[num + 1].lat_lng_alt)
            except IndexError:
                # We've hit the end of the list.
                pass
        return distance / 5280

    @staticmethod
    def tsheets_csv_to_gpspoints(csvfile):
        points = []
        for point in csv_to_list_of_dicts(csvfile):
            date, time = point['local_timestamp'].split()
            gps_point = GpsPoint(point['username'], date, time, LatLngAlt(float(point['latitude']), float(point['longitude']), 0))
            points.append(gps_point)
        return points


class GpsUserDayLog:
    """ Object is a list of GPS points for one day and one user. """
    username = None
    date = None
    gps_points = []

    def __init__(self, username, date, points):
        self.username = username
        self.date = date
        self.gps_points = points

    def get_distance_for_day(self):
        # make sure the points are sorted by time
        points = self.gps_points
        points.sort(key=lambda r: r.time)
        return GpsPoint.distance_between_points(points)

    @staticmethod
    def points_to_day_log_list(points):
        dll = []
        for gp in points:
            found = False
            for num, dl in enumerate(dll):
                if dl.username == gp.username and dl.date == gp.date:
                    found = True
                    dll[num].gps_points.append(gp)
            if not found:
                dll.append(GpsUserDayLog(gp.username, gp.date, [gp, ]))
        return dll
