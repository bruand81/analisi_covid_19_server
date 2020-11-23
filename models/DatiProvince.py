import pandas as pd
import numpy as np
import math

from models.DataUtils import get_last_days_of_data
from models.PopolazioneIstat import PopolazioneIstat


class DatiProvince:
    _repo_path = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master"
    _province = f'{_repo_path}/dati-json/dpc-covid19-ita-province.json'
    _province_csv = f'{_repo_path}/dati-province/dpc-covid19-ita-province.csv'
    _variation_columns_province = ['totale_casi']
    _istat = PopolazioneIstat()
    _dati_provinciali = None
    __max_days = np.inf

    @property
    def max_days(self):
        return self.__max_days

    @max_days.setter
    def max_days(self, var):
        if var > 0:
            self.__max_days = var
        else:
            self.__max_days = np.inf

    def __init_province(self):
        print('Processamento dati riepilogativi provinciali')
        try:
            self._dati_provinciali = pd.read_json(self._province)
        except ValueError as e:
            print(f'Si è verificato un errore con il json. Tento di usare il csv: {e}')
            self._dati_provinciali = pd.read_csv(self._province_csv)
        self._dati_provinciali.fillna(0, inplace=True)
        self._dati_provinciali = self._dati_provinciali.merge(
            self._istat.provincie[['codice_provincia', 'popolazione']], how='outer', on='codice_provincia')
        self._dati_provinciali['incidenza'] = (self._dati_provinciali['totale_casi'] / (
                    self._dati_provinciali['popolazione'] / 100000))

        self._dati_provinciali['incidenza'].fillna(0, inplace=True)
        self._dati_provinciali['incidenza'] = self._dati_provinciali['incidenza'].round(decimals=2)

        counties = self._dati_provinciali.codice_provincia.unique()

        increments = pd.Series([])
        increments_percentage = pd.Series([])
        increments_7dma = pd.Series([])
        increments_3dma = pd.Series([])
        nuovi_positivi_7dsum = pd.Series([])

        for county in counties:
            selected_rows = self._dati_provinciali.codice_provincia == county
            tmp = self._dati_provinciali[selected_rows][self._variation_columns_province].diff()
            is_nan = tmp.isnull()
            row_has_nan = is_nan.any(axis=1)
            rows_cleaned = self._dati_provinciali[selected_rows][row_has_nan]
            tmp[row_has_nan] = rows_cleaned[self._variation_columns_province]
            increments = pd.concat([increments, tmp], axis=0)
            increments_percentage = pd.concat([increments_percentage, tmp.pct_change(fill_method='ffill')], axis=0)
            increments_7dma = pd.concat([increments_7dma, tmp.rolling(window=7).mean()], axis=0)
            increments_3dma = pd.concat([increments_3dma, tmp.rolling(window=3).mean()], axis=0)
            nuovi_positivi_7dsum = nuovi_positivi_7dsum.append(tmp.totale_casi.rolling(window=7).sum())

        increments.columns = ['variazione_' + str(col) for col in increments.columns]
        increments_percentage.columns = ['percentuale_variazione_' + str(col) for col in increments_percentage.columns]
        increments_3dma.columns = ['variazione_' + str(col) + '_3dma' for col in increments_3dma.columns]
        increments_7dma.columns = ['variazione_' + str(col) + '_7dma' for col in increments_7dma.columns]

        self._dati_provinciali = pd.concat(
            [self._dati_provinciali, increments, increments_percentage, increments_3dma, increments_7dma], axis=1)
        incidenza_7d = nuovi_positivi_7dsum.div(self._dati_provinciali['popolazione']/100000)
        incidenza_7d.replace([np.inf, -np.inf], np.nan, inplace=True)
        incidenza_7d.fillna(0, inplace=True)
        incidenza_7d = incidenza_7d.round(decimals=2)
        self._dati_provinciali['incidenza_7d'] = incidenza_7d
        self._dati_provinciali.replace([np.inf, -np.inf], np.nan, inplace=True)
        self._dati_provinciali.fillna(0, inplace=True)
        self._dati_provinciali['date'] = pd.to_datetime(self._dati_provinciali['data'])
        self._dati_provinciali['formatted_date'] = self._dati_provinciali.date.dt.strftime('%d/%m/%Y')

    @property
    def dati_provinciali(self) -> pd.DataFrame:
        if self._dati_provinciali is None:
            self.__init_province()
        if math.isinf(self.max_days):
            return self._dati_provinciali
        else:
            return get_last_days_of_data(self.max_days, self._dati_provinciali)

    @property
    def dati_provinciali_latest(self) -> pd.DataFrame:
        return self.dati_provinciali[self.dati_provinciali.date == self.dati_provinciali.date.max()]
