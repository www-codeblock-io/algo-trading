from backtesting.backtest import BackTestSA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class MomentumRSI(BackTestSA):

    def __init__(self, csv_path, date_col, max_holding, ub_mult,
                 lb_mult, rsi_window, rsi_long=30, rsi_short=70,
                 ma_long=200, ma_short=50):

        super().__init__(csv_path, date_col, max_holding)

        self.ub_mult = ub_mult
        self.lb_mult = lb_mult

        # rsi parameters
        self.rsi_window = rsi_window
        self.rsi_long = rsi_long
        self.rsi_short = rsi_short

        # moving average parameters
        self.ma_long = ma_long
        self.ma_short = ma_short

    def calculate_rsi(self):
        """
        calculates RSI based on the window argument passed into constructor
        https://en.wikipedia.org/wiki/Relative_strength_index
        """
        df = self.dmgt.df
        # create change column
        df['change'] = df.close.diff()
        df['U'] = [x if x > 0 else 0 for x in df.change]
        df['D'] = [abs(x) if x < 0 else 0 for x in df.change]
        df['U'] = df.U.ewm(span=self.rsi_window,
                           min_periods=self.rsi_window-1).mean()
        df['D'] = df.D.ewm(span=self.rsi_window,
                           min_periods=self.rsi_window - 1).mean()

        df['RS'] = df.U / df.D
        df['RSI'] = 100 - 100/(1+df.RS)
        df.drop(['change', 'U', 'D', 'RS'],
                axis=1, inplace=True)

    def calculate_ma(self):
        """
        calculates two expontential movings averages, based on arguments passed
        into construtor
        """
        df = self.dmgt.df
        df['ma_long'] = df.close.ewm(span=self.ma_long,
                                     min_periods=self.ma_long-1).mean()
        df['ma_short'] = df.close.ewm(span=self.ma_short,
                                      min_periods=self.ma_short - 1).mean()

    def generate_signals(self):
        df = self.dmgt.df
        self.calculate_ma()
        self.calculate_rsi()
        df.dropna(inplace=True)

        # 1 if rsi < 30 & ma_short > ma_long, 0 otherwise
        df['longs'] = ((df.RSI < self.rsi_long) & (df.ma_short > df.ma_long))*1
        # -1 if rsi > 70 & ma_short < ma_long, 0 otherwise
        df['shorts'] = ((df.RSI > self.rsi_short) &
                        (df.ma_short < df.ma_long))*-1
        df['entry'] = df.longs + df.shorts
        df.dropna(inplace=True)


if __name__ == '__main__':
    # change this to data/cleaned_btc.csv for bitcoin data
    date_col = 'timestamp'
    csv_path = "clean_data/cleaned_btc.csv"
    # this is in time periods example 12 = 12 hours, if hourly,
    # 6hours if 30min periods etc
    max_holding = 12  # this is in time periods
    ub_mult = 1.01  # change this to change target (longs) stops (shorts)
    lb_mult = 0.99  # change this to change stops (longs) targets (shorts)
    rsi_window = 14
    rsi_long = 30
    rsi_short = 70
    ma_long = 200
    ma_short = 50

    M = MomentumRSI(csv_path, date_col, max_holding, ub_mult, lb_mult,
                    rsi_window, rsi_long, rsi_short, ma_long, ma_short)

    M.dmgt.change_resolution('60min')

    M.run_backtest()
    M.show_performace()
    # print number of trades
    print(abs(M.dmgt.df.direction).sum())
    # uncomment if you wish to save the backtest
    M.save_backtest('BTC')
