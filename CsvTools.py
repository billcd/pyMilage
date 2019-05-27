import csv


def csv_to_list_of_dicts(csv_file):
    point_list = []
    with open(csv_file) as f:
        records = csv.DictReader(f)
        for row in records:
            point_list.append(row)
    return point_list
