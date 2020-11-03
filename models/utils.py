import numpy as np
from datetime import datetime
import pytz


def localize_datetime(d: datetime) -> datetime:
    return pytz.utc.localize(d)


def convert_to_datetime(d) -> datetime:
    return pytz.utc.localize(datetime.strptime(np.datetime_as_string(d, unit='s'), '%Y-%m-%dT%H:%M:%S'))
