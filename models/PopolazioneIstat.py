import os
import pandas as pd


class PopolazioneIstat:
    _files_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files')
    _istat_pcm_link_file = os.path.join(_files_folder, 'link_pcm_istat.csv')
    _istat_file = os.path.join(_files_folder, 'DCIS_POPRES1_08102020132111719.csv')
    _istat = pd.DataFrame()

    @property
    def popolazione(self) -> pd.DataFrame:
        if self._istat.empty:
            istat = pd.read_csv(self._istat_file)
            istat_pcm_link = pd.read_csv(self._istat_pcm_link_file)
            istat = istat.merge(istat_pcm_link, how='inner', on='ITTER107')
            istat = istat[["codice_regione", "codice_provincia", "Value"]]
            self._istat = istat.rename(columns={"Value": "popolazione"})
        return self._istat

    @property
    def regioni_italia(self) -> pd.DataFrame:
        return self.popolazione[self.popolazione.codice_regione >= 0]

    @property
    def regioni(self) -> pd.DataFrame:
        return self.popolazione[self.popolazione.codice_regione > 0]

    @property
    def italia(self) -> pd.DataFrame:
        return self.popolazione[self.popolazione.codice_regione == 0]

    @property
    def provincie(self) -> pd.DataFrame:
        return self.popolazione[self.popolazione.codice_provincia > 0]
