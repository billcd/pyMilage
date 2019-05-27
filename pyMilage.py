import csv
from GpsTools import haversine_distance, LatLngAlt
from pprint import pprint


class TsheetsGpsPoint:
    fname = None
    lname = None
    username = None
    gmt_timestamp = None
    local_timestamp = None
    latitude = None
    longitude = None
    accuracy_in_meters = None
    lat_lng_alt = None


def dicts_to_tsheets_gps_points():
    pass


def csv_to_list_of_dicts(csv_file):
    point_list = []
    with open(csv_file) as f:
        records = csv.DictReader(f)
        for row in records:
            point_list.append(row)
    return point_list


def points_by_user_day(points):
    sorted_list = []
    for point in points:
        date, time = point['local_timestamp'].split()
        found = False
        for num, s in enumerate(sorted_list):
            if s['username'] == point['username'] and s['date'] == date:
                found = True
                sorted_list[num]['points'].append({
                            'time': time,
                            'latitude': point['latitude'],
                            'longitude': point['longitude']})

        if not found:
            sorted_list.append({'username': point['username'], 'date': date, 'points': [{
                            'time': time,
                            'latitude': point['latitude'],
                            'longitude': point['longitude']}, ]
                    })
    return sorted_list


def get_distance_from_points(points):
    distance = 0
    for num, point in enumerate(points):
        try:
            origin = LatLngAlt(float(point['latitude']), float(point['longitude']), 0)
            destination = LatLngAlt(float(points[num+1]['latitude']), float(points[num+1]['longitude']), 0)
            distance += haversine_distance(origin, destination)
        except IndexError:
            pass
    return distance / 5280
