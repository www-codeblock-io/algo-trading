from backtesting.backtest import BackTestSA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date, time


class HigherLower(BackTestSA):
    def __init__(self, csv_path, date_col, max_holding):
        super().__init__(csv_path, date_col, max_holding)

    def generate_signals(self):
        df = self.dmgt.df

        df['longs'] = ((df.high > df.high.shift(1)) & (
                    df.high.shift(1) > df.high.shift(2))
                       & (df.close.shift(2) > df.high.shift(3))) * 1
        df['shorts'] = ((df.low < df.low.shift(1)) & (
                    df.low.shift(1) < df.low.shift(2))
                        & (df.close.shift(2) < df.low.shift(3))) * -1
        df['entry'] = df.shorts + df.longs
        df.dropna(inplace=True)

    def show_performace(self):
        plt.style.use('ggplot')
        self.dmgt.df.returns.cumsum().plot()
        plt.title(f"Strategy results for {self.dmgt.timeframe} timeframe")
        plt.show()

    def run_backtest(self):

        self.generate_signals()
        for row in self.dmgt.df.itertuples():
            if row.entry == 1:
                # adding logic for dymanic barriers
                if self.open_pos is False:
                    self.open_long(row.t_plus)
                else:
                    self.target_price = self.target_price * self.ub_mult
                    self.max_holding = self.max_holding + int(
                        (self.max_holding_limit / 3))
                    self.add_zeros()
            elif row.entry == -1:
                # adding logic for dymanic barriers
                if self.open_pos is False:
                    self.open_short(row.t_plus)
                else:
                    self.target_price = self.target_price * self.lb_mult
                    self.max_holding = self.max_holding + int(
                        (self.max_holding_limit / 3))
                    self.add_zeros()

            elif self.open_pos:
                self.monitor_open_positions(row.close, row.Index)
            else:
                self.add_zeros()

        self.add_trade_cols()

    def show_performace(self):
        plt.style.use('ggplot')
        self.dmgt.df.returns.cumsum().plot()
        plt.title(f"Strategy results for {self.dmgt.timeframe} timeframe")
        plt.show()

    def save_backtest(self):
        '''
        saves backtest to csv for further inspection
        '''
        strat_name = self.__class__.__name__
        tf = self.dmgt.timeframe
        self.dmgt.df.to_csv(f"../data/backtests/{strat_name}_{tf}.csv")


if __name__ == '__main__':
    csv_path = "clean_data/cleaned_btc.csv"
    date_col = 'timestamp'
    max_holding = 8

    HL = HigherLower(csv_path, date_col, max_holding)

    HL.dmgt.change_resolution("120min")

    HL.run_backtest()
    HL.show_performace()
    # 1049 trades with fixed stops and targets 981
    print(abs(HL.dmgt.df.direction).sum())

    # uncomment if you wish to save the backtest to folder
    HL.save_backtest()