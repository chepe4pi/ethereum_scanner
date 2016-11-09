import datetime
import pytz


def timestamp_to_utc_datetime(timestamp):
    return datetime.datetime.utcfromtimestamp(int(timestamp)).replace(tzinfo=pytz.utc)
