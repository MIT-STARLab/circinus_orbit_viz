import datetime

def iso_string_to_dt(iso_string):
    return datetime.datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S.%fZ")