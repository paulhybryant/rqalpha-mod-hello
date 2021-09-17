from rqalpha.interface import AbstractMod
from datetime import date
from rqalpha.data.base_data_source import BaseDataSource
import pandas as pd

__config__ = {
    'data_path': None,
    'data_format': None,
    'start_date': None,
    'end_date': None,
}


class LocalDataSourceMod(AbstractMod):
    def __init__(self):
        pass

    def start_up(self, env, mod_config):
        env.set_data_source(
            LocalDataSource(env.config.base.data_bundle_path,
                            mod_config.data_path,
                            mod_config.data_format,
                            date.fromisoformat(mod_config.start_date),
                            date.fromisoformat(mod_config.end_date)))

    def tear_down(self, code, exception=None):
        pass


# Only provide bar data for frequency of 1d
class LocalDataSource(BaseDataSource):
    def __init__(self, path, data_path, data_format, start_date, end_date):
        super(LocalDataSource, self).__init__(path, None)
        if data_path and data_format and start_date and end_date:
            print('Reading data from %s' % data_path)
            if data_format == 'excel':
                self._df = pd.read_excel(data_path)
            if data_format == 'csv':
                self._df = pd.read_csv(data_path)
            print('Done reading %s' % data_path)
            self._instruments = set(self._df.order_book_id.to_list())
            self._df['date'] = self._df.date.astype(str)
            self._df = self._df.set_index(['order_book_id', 'date'])
            self._start_date = start_date
            self._end_date = end_date
        else:
            self._df = None
            self._start_date = None
            self._end_date = None

    def get_bar(self, instrument, dt, frequency):
        if self._df is None or frequency != '1d' or instrument.order_book_id not in self._instruments:
            return super(LocalDataSource,
                         self).get_bar(instrument, dt, frequency)

        return self._df.loc[(instrument.order_book_id,
                             str(dt.date()))].to_dict()

    def history_bars(self,
                     instrument,
                     bar_count,
                     frequency,
                     fields,
                     dt,
                     skip_suspended=True,
                     include_now=False,
                     adjust_type='pre',
                     adjust_orig=None):
        if self._df is None or frequency != '1d' or instrument.order_book_id not in self._instruments:
            return super(LocalDataSource,
                         self).history_bars(instrument, bar_count, frequency,
                                            fields, dt, skip_suspended)

        fields = [field for field in fields if field in self._df.columns]
        return self._df[fields].loc[(instrument.order_book_id,
                                     str(dt.date()))].as_matrix()

    def available_data_range(self, frequency):
        return self._start_date, self._end_date
