import pandas as pd
from datetime import datetime, timedelta


def get_last_days_of_data( max_days: int, data: pd.DataFrame) -> pd.DataFrame:
    d = datetime.today() - timedelta(days=max_days)
    return data[data['date'] > d]