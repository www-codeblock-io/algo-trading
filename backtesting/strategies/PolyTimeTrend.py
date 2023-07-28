from backtesting.backtest import BackTestSA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class PolyTrend(BackTestSA):

    def __init__(self, csv_path, date_col, max_holding,
                 lookback, look_ahead, long_thres, short_thres,
                 ub_mult, lb_mult, long_tp, long_sl,
                 short_tp, short_sl):

        super().__init__(csv_path, date_col, max_holding)

        self.lookback = lookback
        self.look_ahead = look_ahead

        self.long_thres = long_thres
        self.short_thres = short_thres

        self.ub_mult = ub_mult
        self.lb_mult = lb_mult

        self.long_tp = long_tp
        self.long_sl = long_sl
        self.short_tp = short_tp
        self.short_sl = short_sl

    @staticmethod
    def rolling_tt(series, n):
        """

        :param series: close price for eth/btc in pandas series
        :param n: lookahead from constructor
        :return: prediction for close_{+n}
        """

        y = series.values.reshape(-1, 1)
        t = np.arange(len(y))
        X = np.c_[np.ones_like(y), t, t ** 2]
        betas = np.linalg.inv(X.T @ X) @ X.T @ y
        new_vals = np.array([1, t[-1] + n, (t[-1] + n) ** 2])
        # beta0 + beta1 * t[-1]+n + beta2 * (t[-1]+n)**2
        pred = new_vals @ betas
        return pred

    def generate_signals(self):
        df = self.dmgt.df
        n = self.look_ahead
        df['preds'] = df.close.rolling(self.lookback).apply(self.rolling_tt,
                                                            args=(n,),
                                                            raw=False)
        # predicted change column
        df['pdelta'] = (df.preds / df.close) - 1
        df['longs'] = (df.pdelta > self.long_thres) * 1
        df['shorts'] = (df.pdelta < self.short_thres) * -1
        df['entry'] = df.longs + df.shorts
        df.dropna(inplace=True)

    def run_backtest(self):

        self.generate_signals()
        for row in self.dmgt.df.itertuples():
            if row.entry == 1:

                if self.open_pos is False:
                    # setting the target and stop, see BacktestSA class to
                    # see why this works
                    self.ub_mult = self.long_tp
                    self.lb_mult = self.long_sl
                    self.open_long(row.t_plus)
                else:
                    self.monitor_open_positions(row.close, row.Index)
            elif row.entry == -1:

                if self.open_pos is False:
                    self.ub_mult = self.short_sl
                    self.lb_mult = self.short_tp
                    self.open_short(row.t_plus)
                else:
                    self.monitor_open_positions(row.close, row.Index)

            elif self.open_pos:
                self.monitor_open_positions(row.close, row.Index)
            else:
                self.add_zeros()

        self.add_trade_cols()


if __name__ == '__main__':
    csv_path = "clean_data/cleaned_btc.csv"
    date_col = 'timestamp'
    max_holding = 12 * 12
    # I fixed this at 24 hour minimum, 60min = 24, 30min = 48 etc
    lookback = 12 * 24
    look_ahead = 4  # periods ahead to predict for each endpoint of the model
    # if model predicts a price that represents an increase of 3% we enter
    long_thres = 0.03
    short_thres = -0.03  # opposite of above
    ub_mult = 1.02
    lb_mult = 0.98
    long_tp = 1.03  # long target in %
    long_sl = 0.98  # long stop loss
    short_tp = 0.96  # short target
    short_sl = 1.025  # short stop loss

    Poly = PolyTrend(csv_path, date_col, max_holding,
                     lookback, look_ahead, long_thres,
                     short_thres, ub_mult, lb_mult, long_tp,
                     long_sl, short_tp, short_sl)

    Poly.dmgt.change_resolution('5min')
    Poly.run_backtest()
    Poly.show_performace()
    print(abs(Poly.dmgt.df.direction).sum())