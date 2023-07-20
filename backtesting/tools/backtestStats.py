import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class BtStats:
    '''
    designed for use with crypto futures which have 24/7 opening hours, needs modified for other assets
    '''

    def N_annual(freq):
        '''
        :param freq: frequency of backtest as string
        :return: number of periods per annum for chosen freq
        '''
        if freq == '1min':
            return 365 * 60 * 24
        elif freq == '5min':
            return 12 * 24 * 365
        elif freq == '15min':
            return 4 * 24 * 365
        elif freq == '30min':
            return 48 * 365
        elif freq == '60min':
            return 24 * 365
        elif freq == '120min' or freq == '2H':
            return 12 * 365
        elif freq == '240min' or freq == '4H':
            return 6 * 365
        elif freq == '1D':
            return 365
        else:
            raise ValueError('Invalid freq')

    def sharpe_ratio(return_series, N):
        '''

        :param N: periods per annum
        :return: sharpe ratio as float
        '''
        mean = return_series.mean() * N
        sigma = return_series.std() * np.sqrt(N)
        return round(mean / sigma, 3)

    def calmar_ratio(return_series, N, max_drawdown):
        '''

        :param N: periods per annum
        :param max_drawdown: max drawdown from strategy
        :return: calmaro ratio as float
        '''
        return round(return_series.mean() * N / abs(max_drawdown), 3)

    def drawdowns(returns_series):
        '''
        takes simple returns series from backtest as pandas dataframe
        :return: vector of drawdowns with same length as return_series
        '''
        compounded = (returns_series + 1).cumprod()
        peak = compounded.expanding(min_periods=1).max()
        dd = (compounded / peak) - 1
        return round(dd, 3)

    def cagr(cum_rets_series, N):
        '''
        :param cum_rets_series: pandas series of compound returns
        :param N: Number of periods per year
        :return:
        '''

        cagr = float((cum_rets_series[-1:].values) ** (
                    1 / (len(cum_rets_series) / N))) - 1
        return round(cagr, 3)


class BacktestProfile:

    def __init__(self, bt, freq, ret_type='comp', spread=1 / 10988, fees=5e-4):
        if not isinstance(bt, pd.DataFrame):
            raise ValueError('bt must be pandas dataframe object')

        self.fees = fees + spread
        self.bt = bt
        self.bt.set_index(pd.to_datetime(bt['timestamp']), inplace=True)
        self.N = BtStats.N_annual(freq)
        self.ret_type = ret_type

        if self.ret_type == 'comp':
            self.bt['returns_no_fee'] = self.compound_ret(self.bt.returns)
            self.bt['returns_f'] = self.fees_calc(bt.returns, fees)
            self.bt['returns_fees'] = self.compound_ret(self.bt.returns_f)
        elif self.ret_type == 'simple':
            self.bt['returns_f'] = self.fees_calc(bt.returns, fees)
            self.bt['returns_no_fee'] = self.simple_returns(self.bt.returns)
            self.bt['returns_fees'] = self.simple_returns(self.bt.returns_f)
        else:
            raise ValueError(
                'Ret type not recognized must be: {comp} or {simple}')

        self.n_longs, self.n_shorts = self.total_trades(self.bt.direction)
        self.n_trades = self.n_longs + self.n_shorts

        # sharpe
        self.sharpe = BtStats.sharpe_ratio(self.bt.returns_f, self.N)
        # cagr
        self.cagr = BtStats.cagr(self.bt.returns_fees, self.N)
        # calculate drawdowns
        self.bt['dd'] = BtStats.drawdowns(self.bt.returns_f)
        # max drawdown
        self.max_dd = self.bt.dd.min()
        # calmar
        self.calmar = BtStats.calmar_ratio(self.bt.returns_f, self.N,
                                           self.max_dd)

        self.long_accuracy, self.short_accuracy = self.accuracy()

    @staticmethod
    def fees_calc(returns_col, fees):
        returns_col = np.where(returns_col != 0, returns_col - fees * 2, 0)
        return returns_col

    @staticmethod
    def simple_returns(returns_col):
        returns_col = returns_col.cumsum() + 1
        return returns_col

    @staticmethod
    def compound_ret(returns_col):
        returns_col = (returns_col + 1).cumprod()
        return returns_col

    @staticmethod
    def total_trades(direction_series):
        longs = direction_series[direction_series == 1].sum()
        shorts = direction_series[direction_series == -1].sum()
        return longs, abs(shorts)

    def accuracy(self):
        longs = self.bt[self.bt.direction == 1]
        shorts = self.bt[self.bt.direction == -1]
        long_acc = len(longs[longs.returns_f > 0]) / len(longs)
        short_acc = len(shorts[shorts.returns_f > 0]) / len(shorts)
        return round(long_acc, 3), round(short_acc, 3)

    def show_ratios(self):
        print(f"Sharpe: {self.sharpe}")
        print(f"calmar: {self.calmar}")
        print(f"cagr: {self.cagr}")
        print(f"max drawdown: {abs(self.max_dd)}")
        print(f"Long accuracy: {self.long_accuracy}")
        print(f"Short accuracy: {self.short_accuracy}")

    def show_perf(self, title):
        plt.style.use('ggplot')
        fig, axes = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})
        self.bt.returns_fees.plot(ax=axes[0], color='black')
        axes[0].set_title(title)
        axes[0].set_ylabel('Cumulative returns')
        self.bt.dd.plot(ax=axes[1], color='red')
        axes[1].set_title('drawdowns')
        plt.ylabel('Drawdowns')
        plt.tight_layout()
        plt.show()

        longs = self.bt[self.bt.direction == 1]
        shorts = self.bt[self.bt.direction == -1]
        fig, ax = plt.subplots()
        ax = sns.kdeplot(data=longs['returns_f'], label='longs', ax=ax)
        ax = sns.kdeplot(data=shorts['returns_f'], label='shorts', ax=ax)
        ax.set_title("Longs vs Shorts")
        plt.legend()
        plt.show()

        print('==' * 50)
        print(f"total longs: {self.n_longs}")
        print(f"total shorts: {self.n_shorts}")
        self.show_ratios()
        print('==' * 50)


if __name__ == '__main__':
    # change this to the path of your backtest results
    bt = pd.read_csv(
        "data/backtests/MomentumRSI_60min-BTC.csv")
    freq = '1min'
    BT = BacktestProfile(bt, freq)
    BT.show_perf("MomentumRSI_60min-BTC")