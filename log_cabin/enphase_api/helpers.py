import datetime as dt

def dt_to_epoch_seconds(datetime: dt.datetime) -> int:
    # convert a python datetime to an integer unix timestamp in seconds
    if not datetime.tzinfo:
        raise ValueError("Please provide a TZ-aware datetime")
    return int(datetime.timestamp())


def epoch_seconds_to_dt(timestamp: int) -> dt.datetime:
    # convert an integer unix timestamp in seconds to a python datetime
    if isinstance(timestamp, dt.datetime):
        return timestamp
    return dt.datetime.fromtimestamp(int(timestamp), tz=dt.timezone.utc)