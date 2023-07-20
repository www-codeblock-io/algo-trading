import pandas as pd
import datetime as dt
from logger import MyLogger

# instance of MyLogger, add False as last param to disable.
log = MyLogger('../logfile.txt', "datamanager.py", False)


class DataManager:

    def __init__(self, csv_path, date_col):

        self.data = pd.read_csv(csv_path, parse_dates=[date_col],
                                index_col=date_col)

        # can use uniform to change this
        self.data['t_plus'] = self.data.open.shift(-1)
        self.data['sigtime'] = self.data.index  # creates a column sigtime
        self.data.dropna(inplace=True)

        self.df = self.data.copy()
        self.timeframe = '1min'

    def change_sigtime(self, hours=0, mins=0):
        """
        :param hours: int of the hour bar you want a signal on, defaults to 0
        :param mins: int of the minutes you want a signal on, defaults to 0
        """
        self.data['sigtime'] = (self.data.index.time == dt.time(hours, mins))\
            .astype(int)

    def change_resolution(self, new_timeframe):

        resample_dict = {'volume': 'sum', 'open': 'first',
                         'low': 'min', 'high': 'max',
                         'close': 'last',
                         't_plus': 'last', 'sigtime': 'last'}

        self.df = self.data.resample(new_timeframe).agg(resample_dict)

        self.timeframe = new_timeframe




