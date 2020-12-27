import pandas as pd

from datetime import datetime

from models.utils import localize_datetime
import logging


class DatiRecenti:
    _repo_path = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master"
    _nazionale_csv = f'{_repo_path}/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-latest.csv'
    _regioni_csv = f'{_repo_path}/dati-regioni/dpc-covid19-ita-regioni-latest.csv'
    _nazionale = f'{_repo_path}/dati-json/dpc-covid19-ita-andamento-nazionale-latest.json'
    _regioni = f'{_repo_path}/dati-json/dpc-covid19-ita-regioni-latest.json'
    _province = f'{_repo_path}/dati-json/dpc-covid19-ita-province-latest.json'
    _province_csv = f'{_repo_path}/dati-province/dpc-covid19-ita-province-latest.csv'

    @property
    def last_update_date(self) -> datetime:
        date_province = self.last_update_date_provincie

        date_regioni = self.last_update_date_regioni

        date_nazionale = self.last_update_date_nazionale

        date = min(date_province, date_regioni, date_nazionale)
        return date

    @property
    def last_update_date_nazionale(self) -> datetime:
        return DatiRecenti.get_last_date_from_json_or_csv(self._nazionale, self._nazionale_csv)

    @property
    def last_update_date_regioni(self) -> datetime:
        return DatiRecenti.get_last_date_from_json_or_csv(self._regioni, self._regioni_csv)

    @property
    def last_update_date_provincie(self) -> datetime:
        return DatiRecenti.get_last_date_from_json_or_csv(self._province, self._province_csv)

    @staticmethod
    def get_last_date_from_json_or_csv(json, csv) -> datetime:
        try:
            df = pd.read_json(json)
        except ValueError as e:
            logging.getLogger().warning(f'Si è verificato un errore con il json. Tento di usare il csv: {e}')
            df = pd.read_csv(csv)
        d = pd.to_datetime(df.data.iloc[0])
        return localize_datetime(d.to_pydatetime())