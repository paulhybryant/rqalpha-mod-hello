from rqalpha.interface import AbstractMod
from datetime import date
from rqalpha.data.base_data_source import BaseDataSource
import pandas as pd

__config__ = {
    "data_path": None,
    "start_date": None,
    "end_date": None,
}


class LocalDataSourceMod(AbstractMod):
    def __init__(self):
        pass

    def start_up(self, env, mod_config):
        env.set_data_source(
            LocalDataSource(env.config.base.data_bundle_path,
                            mod_config.data_path,
                            date.fromisoformat(mod_config.start_date),
                            date.fromisoformat(mod_config.end_date)))

    def tear_down(self, code, exception=None):
        pass

# Only provide bar data for frequency of 1d
class LocalDataSource(BaseDataSource):
    def __init__(self, path, local_data_path, start_date, end_date):
        super(LocalDataSource, self).__init__(path, None)
        if local_data_path and start_date and end_date:
            self._df = pd.read_excel(local_data_path)
            self._df['date'] = self._df.date.astype(str)
            self._df = self._df.set_index(['order_book_id', 'date'])
            self._start_date = start_date
            self._end_date = end_date
        else:
            self._df = None
            self._start_date = None
            self._end_date = None

    def get_bar(self, instrument, dt, frequency):
        if self._df is None:
            return super(LocalDataSource,
                         self).get_bar(instrument, dt, frequency)

        if frequency != '1d':
            return super(LocalDataSource,
                         self).get_bar(instrument, dt, frequency)
        return self._df.loc[(instrument.order_book_id, str(dt.date()))].to_dict()

    def history_bars(self,
                     instrument,
                     bar_count,
                     frequency,
                     fields,
                     dt,
                     skip_suspended=True):
        if self._df is None:
            return super(LocalDataSource,
                         self).get_bar(instrument, dt, frequency)

        if frequency != '1d' or not skip_suspended:
            return super(LocalDataSource,
                         self).history_bars(instrument, bar_count, frequency,
                                            fields, dt, skip_suspended)

        fields = [field for field in fields if field in self._df.columns]
        return self._df[fields].loc[(instrument.order_book_id, str(dt.date()))].as_matrix()

    def available_data_range(self, frequency):
        return self._start_date, self._end_date
