from backtesting.backtest import BackTestSA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class IMeanReversion(BackTestSA):

    def __init__(self, csv_path, date_col, max_holding, ub_mult, lb_mult,
                 up_filter, down_filter, long_lookback, short_lookback):

        super().__init__(csv_path, date_col, max_holding)
        # target and stop losses mults
        self.ub_mult = ub_mult
        self.lb_mult = lb_mult
        # conditions
        self.up_filter = up_filter
        self.down_filter = down_filter
        # lookbacks
        self.long_lookback = long_lookback  # n
        self.short_lookback = short_lookback  # k

    def generate_signals(self):
        df = self.dmgt.df

        df['min_24'] = df.close.rolling(self.short_lookback).min()
        df['max_24'] = df.close.rolling(self.short_lookback).max()

        df['longs'] = ((df.close <= df.min_24) &
                       (df.close > df.close.shift(self.long_lookback) *
                        self.up_filter)) * 1
        df['shorts'] = ((df.close >= df.max_24) &
                        (df.close < df.close.shift(self.long_lookback) *
                        self.down_filter)) * -1

        df['entry'] = df.longs + df.shorts
        # uncomment to shift signal to enter on next close
        df['entry'] = df.entry.shift(1)

        df.dropna(inplace=True)


if __name__ == "__main__":
    csv_path = "clean_data/cleaned_btc.csv"  # change this to your folder/filename
    date_col = 'timestamp'
    max_holding = 300  # 300minutes
    ub_mult = 1.02  # target / stop
    lb_mult = 0.98  # target / stop
    up_filter = 1.03  # change this to change filter for longs
    down_filter = 0.97  # change this for shorts filter

    long_lookback = 60*24*30
    short_lookback = 60*24

    Imv = IMeanReversion(csv_path, date_col, max_holding, ub_mult,
                         lb_mult, up_filter, down_filter, long_lookback,
                         short_lookback)

    Imv.run_backtest()
    Imv.show_performace()