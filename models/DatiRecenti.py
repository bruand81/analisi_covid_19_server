import pandas as pd

from datetime import datetime

from models.utils import localize_datetime


class DatiRecenti:
    _repo_path = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master"
    _province = f'{_repo_path}/dati-province/dpc-covid19-ita-province-latest.csv'

    @property
    def last_update_date(self) -> datetime:
        df = pd.read_csv(self._province)
        date = pd.to_datetime(df.data.iloc[0])
        return localize_datetime(date.to_pydatetime())
