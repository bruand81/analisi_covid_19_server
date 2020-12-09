import pandas as pd
import numpy as np
import math
from datetime import datetime
import os
from models.DataUtils import get_last_days_of_data
from models.PopolazioneIstat import PopolazioneIstat


class DatiRegioni:
    _repo_path = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master"
    _nazionale_csv = f'{_repo_path}/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv'
    _nazionale_latest_csv = f'{_repo_path}/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-latest.csv'
    _regioni_csv = f'{_repo_path}/dati-regioni/dpc-covid19-ita-regioni.csv'
    _nazionale = f'{_repo_path}/dati-json/dpc-covid19-ita-andamento-nazionale.json'
    _nazionale_latest = f'{_repo_path}/dati-json/dpc-covid19-ita-andamento-nazionale-latest.json'
    _regioni = f'{_repo_path}/dati-json/dpc-covid19-ita-regioni.json'
    _variation_columns = ['tamponi', 'casi_testati', 'terapia_intensiva', 'ricoverati_con_sintomi', 'deceduti',
                          'dimessi_guariti', 'isolamento_domiciliare', 'casi_da_screening',
                          'casi_da_sospetto_diagnostico']
    _full_data: pd.DataFrame = None
    _istat = PopolazioneIstat()
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

    def __init_full_data(self):
        print('Processamento dati riepilogativi nazionali e regionali')
        try:
            data_naz = pd.read_json(self._nazionale)
        except ValueError as e:
            print(f'Si è verificato un errore con il json. Tento di usare il csv: {e}')
            data_naz = pd.read_csv(self._nazionale_csv)

        try:
            data_reg = pd.read_json(self._regioni)
        except ValueError as e:
            print(f'Si è verificato un errore con il json. Tento di usare il csv: {e}')
            data_reg = pd.read_csv(self._regioni_csv)

        data_naz.sort_values(by='data', inplace=True)
        data_naz.fillna(0, inplace=True)
        data_naz['codice_regione'] = 0
        data_naz['denominazione_regione'] = 'Italia'
        data_naz['lat'] = 41.89277044
        data_naz['long'] = 12.48366722
        data_naz['note_test'] = data_naz.note_test.astype(str)
        data_naz['note_casi'] = data_naz.note_casi.astype(str)
        data_reg['note_test'] = data_reg.note_test.astype(str)
        data_reg['note_casi'] = data_reg.note_casi.astype(str)

        data_reg.fillna(0, inplace=True)

        self._full_data = pd.merge(data_naz, data_reg, how='outer')
        self._full_data['date'] = pd.to_datetime(self._full_data['data']).dt.normalize()
        self._full_data = self._full_data.merge(
            self.popolazione_istat_regioni_italia[['codice_regione', 'popolazione']],
            how='outer', on='codice_regione')
        self._full_data['incidenza'] = (
                    self._full_data['totale_casi'] / (self._full_data['popolazione'] / 100000)).round(
            decimals=2)

        regions = self._full_data.codice_regione.unique()

        nuovi_positivi_7dsum = pd.Series(index=self._full_data.index).fillna(0).astype(int)
        terapia_intensiva_7dsum = pd.Series(index=self._full_data.index).fillna(0).astype(int)
        deceduti_7dsum = pd.Series(index=self._full_data.index).fillna(0).astype(int)
        dimessi_guariti_7dsum = pd.Series(index=self._full_data.index).fillna(0).astype(int)
        ricoverati_con_sintomi_7dsum = pd.Series(index=self._full_data.index).fillna(0).astype(int)
        nuovi_positivi_7dma = pd.Series(index=self._full_data.index).fillna(0).astype(int)
        nuovi_positivi_3dma = pd.Series(index=self._full_data.index).fillna(0).astype(int)
        # casi_testati_7dma = pd.Series([])
        increments = pd.Series([])
        increments_percentage = pd.Series([])
        increments_7dma = pd.Series(name='nuovi_positivi_7dma')
        increments_3dma = pd.Series(name='nuovi_positivi_3dma')

        for region in regions:
            selected_rows = self._full_data.codice_regione == region
            tmp = self._full_data[selected_rows][self._variation_columns].diff()
            is_nan = tmp.isnull()
            row_has_nan = is_nan.any(axis=1)
            rows_cleaned = self._full_data[selected_rows][row_has_nan]
            tmp[row_has_nan] = rows_cleaned[self._variation_columns]
            increments = pd.concat([increments, tmp], axis=0)
            increments_percentage = pd.concat([increments_percentage, tmp.pct_change(fill_method='ffill')], axis=0)
            increments_7dma = pd.concat([increments_7dma, tmp.rolling(window=7).mean()], axis=0)
            increments_3dma = pd.concat([increments_3dma, tmp.rolling(window=3).mean()], axis=0)
            nuovi_positivi_7dma.iloc[self._full_data[selected_rows].index] = self._full_data[selected_rows].nuovi_positivi.rolling(window=7).mean()
            nuovi_positivi_3dma.iloc[self._full_data[selected_rows].index] = self._full_data[selected_rows].nuovi_positivi. rolling(window=3).mean()
            nuovi_positivi_7dsum.iloc[self._full_data[selected_rows].index] = self._full_data[selected_rows].nuovi_positivi.rolling(window=7).sum()
            terapia_intensiva_7dsum.iloc[tmp.index] = tmp.terapia_intensiva.rolling(window=7).sum()
            deceduti_7dsum.iloc[tmp.index] = tmp.deceduti.rolling(window=7).sum()
            dimessi_guariti_7dsum.iloc[tmp.index] = tmp.dimessi_guariti.rolling(window=7).sum()
            ricoverati_con_sintomi_7dsum.iloc[tmp.index] = tmp.ricoverati_con_sintomi.rolling(window=7).sum()

        increments.columns = ['variazione_' + str(col) for col in increments.columns]
        increments_percentage.columns = ['percentuale_variazione_' + str(col) for col in increments_percentage.columns]
        increments_3dma.columns = ['variazione_' + str(col) + '_3dma' for col in increments_3dma.columns]
        increments_7dma.columns = ['variazione_' + str(col) + '_7dma' for col in increments_7dma.columns]
        nuovi_positivi_7dma.fillna(0, inplace=True)
        nuovi_positivi_3dma.fillna(0, inplace=True)
        nuovi_positivi_7dsum.fillna(0, inplace=True)


        full_data = pd.concat([self._full_data, increments, increments_percentage, increments_3dma, increments_7dma],
                              axis=1)

        self._full_data = full_data

        self._full_data['terapia_intensiva_7dsum'] = terapia_intensiva_7dsum.fillna(0).astype(int)
        self._full_data['deceduti_7dsum'] = deceduti_7dsum.fillna(0).astype(int)
        self._full_data['dimessi_guariti_7dsum'] = dimessi_guariti_7dsum.fillna(0).astype(int)
        self._full_data['ricoverati_con_sintomi_7dsum'] = ricoverati_con_sintomi_7dsum.fillna(0).astype(int)
        self._full_data['incidenza_7d'] = (nuovi_positivi_7dsum / (self._full_data['popolazione'] / 100000)).round(
            decimals=2)
        self._full_data['nuovi_positivi_7dma'] = nuovi_positivi_7dma.astype('int')
        self._full_data['nuovi_positivi_3dma'] = nuovi_positivi_3dma.astype('int')
        self._full_data['nuovi_positivi_7dsum'] = nuovi_positivi_7dsum.astype('int')

        dates = self._full_data.sort_values(by=["date"]).date.unique()

        nuovi_positivi_7d_incr = pd.Series(index=self._full_data.index).fillna(0).astype(int)
        deceduti_7d_incr = pd.Series(index=self._full_data.index).fillna(0).astype(int)
        terapia_intensiva_7d_incr = pd.Series(index=self._full_data.index).fillna(0).astype(int)
        dimessi_guariti_7d_incr = pd.Series(index=self._full_data.index).fillna(0).astype(int)
        ricoverati_con_sintomi_7d_incr = pd.Series(index=self._full_data.index).fillna(0).astype(int)

        for day in dates:
            pdate = day - np.timedelta64(7, "D")
            if pdate in dates:
                for region in regions:
                    np7dsum = self._full_data[
                        (self._full_data.codice_regione == region) & (self._full_data.date == day)]
                    prev_np7dsum = self._full_data[
                        (self._full_data.codice_regione == region) & (self._full_data.date == pdate)]
                    nuovi_positivi_7d_incr.iloc[np7dsum.index] = np7dsum.nuovi_positivi_7dsum.values[0] - prev_np7dsum.nuovi_positivi_7dsum.values[0]
                    deceduti_7d_incr.iloc[np7dsum.index] = np7dsum.deceduti_7dsum.values[0] - prev_np7dsum.deceduti_7dsum.values[0]
                    terapia_intensiva_7d_incr.iloc[np7dsum.index] = np7dsum.terapia_intensiva_7dsum.values[0] - prev_np7dsum.terapia_intensiva_7dsum.values[0]
                    dimessi_guariti_7d_incr.iloc[np7dsum.index] = np7dsum.dimessi_guariti_7dsum.values[0] - prev_np7dsum.dimessi_guariti_7dsum.values[0]
                    ricoverati_con_sintomi_7d_incr.iloc[np7dsum.index] = np7dsum.ricoverati_con_sintomi_7dsum.values[0] - prev_np7dsum.ricoverati_con_sintomi_7dsum.values[0]
                    # print(f'{day}: {np7dsum.values[0]} - {prev_np7dsum.values[0]} = {nuovi_positivi_7d_incr.iloc[np7dsum.index].values[0]}')

        self._full_data["nuovi_positivi_7d_incr"] = nuovi_positivi_7d_incr.fillna(0).astype(int)
        self._full_data["deceduti_7d_incr"] = deceduti_7d_incr.fillna(0).astype(int)
        self._full_data["terapia_intensiva_7d_incr"] = terapia_intensiva_7d_incr.fillna(0).astype(int)
        self._full_data["dimessi_guariti_7d_incr"] = dimessi_guariti_7d_incr.fillna(0).astype(int)
        self._full_data["ricoverati_con_sintomi_7d_incr"] = ricoverati_con_sintomi_7d_incr.fillna(0).astype(int)

        self._full_data['percentuale_positivi_tamponi'] = self._full_data['totale_positivi'].divide(
            self._full_data['tamponi'])
        self._full_data['percentuale_positivi_tamponi_giornaliera'] = self._full_data['nuovi_positivi'].divide(
            self._full_data['variazione_tamponi'])
        self._full_data['percentuale_positivi_casi'] = self._full_data['totale_positivi'].divide(
            self._full_data['casi_testati'])
        self._full_data['percentuale_positivi_casi_giornaliera'] = self._full_data['nuovi_positivi'].divide(
            self._full_data['variazione_casi_testati'])
        self._full_data['percentuale_positivi_casi_7dma'] = self._full_data['nuovi_positivi_7dma'].divide(
            self._full_data['variazione_casi_testati_7dma'])
        self._full_data['percentuale_positivi_casi_3dma'] = self._full_data['nuovi_positivi_3dma'].divide(
            self._full_data['variazione_casi_testati_3dma'])
        self._full_data['CFR'] = self._full_data['deceduti'].divide(
            self._full_data['totale_casi'])

        self._full_data.replace([np.inf, -np.inf], np.nan, inplace=True)
        self._full_data.fillna(0, inplace=True)

    @property
    def popolazione_istat(self) -> pd.DataFrame:
        return self._istat.popolazione

    @property
    def popolazione_istat_regioni_italia(self) -> pd.DataFrame:
        return self._istat.regioni_italia

    @property
    def dati_nazionali(self) -> pd.DataFrame:
        if self._full_data is None:
            self.__init_full_data()
        if math.isinf(self.max_days):
            return self._full_data[self._full_data.codice_regione == 0]
        else:
            return get_last_days_of_data(self.max_days, self._full_data[self._full_data.codice_regione == 0])

    @property
    def dati_regionali(self) -> pd.DataFrame:
        if self._full_data is None:
            self.__init_full_data()
        if math.isinf(self.max_days):
            return self._full_data[self._full_data.codice_regione != 0]
        else:
            return get_last_days_of_data(self.max_days, self._full_data[self._full_data.codice_regione != 0])

    @property
    def dati_completi(self) -> pd.DataFrame:
        if self._full_data is None:
            self.__init_full_data()
        if math.isinf(self.max_days):
            return self._full_data
        else:
            return get_last_days_of_data(self.max_days, self._full_data)

    @property
    def dati_nazionali_latest(self) -> pd.DataFrame:
        return self.dati_nazionali[self.dati_nazionali.date == self.dati_nazionali.date.max()]

    @property
    def dati_regionali_latest(self) -> pd.DataFrame:
        return self.dati_regionali[self.dati_regionali.date == self.dati_regionali.date.max()]

    @property
    def dati_completi_latest(self) -> pd.DataFrame:
        return self.dati_completi[self.dati_completi.date == self.dati_completi.date.max()]

    @property
    def latest_update_date(self) -> datetime:
        try:
            data_naz = pd.read_json(self._nazionale_latest)
        except ValueError as e:
            print(f'Si è verificato un errore con il json. Tento di usare il csv: {e}')
            data_naz = pd.read_csv(self._nazionale_latest_csv)
        return pd.to_datetime(data_naz.data).max()
