import pandas as pd

from datetime import datetime

from models.utils import localize_datetime


class DatiRecenti:
    _repo_path = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master"
    _province = f'{_repo_path}/dati-province/dpc-covid19-ita-province-latest.csv'
    _regioni = f'{_repo_path}/dati-regioni/dpc-covid19-ita-regioni-latest.csv'
    _nazionale = f'{_repo_path}/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-latest.csv'

    @property
    def last_update_date(self) -> datetime:
        df = pd.read_csv(self._province)
        date_province = pd.to_datetime(df.data.iloc[0])
        df = pd.read_csv(self._regioni)
        date_regioni = pd.to_datetime(df.data.iloc[0])
        df = pd.read_csv(self._nazionale)
        date_nazionale = pd.to_datetime(df.data.iloc[0])
        date = min(date_province.to_pydatetime(), date_regioni.to_pydatetime(), date_nazionale.to_pydatetime())
        return localize_datetime(date)
