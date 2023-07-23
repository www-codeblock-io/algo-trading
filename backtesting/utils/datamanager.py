# features_creation.py
import pandas as pd


class DataManager:

    def __init__(self, csv_path, date_col):

        self.data = pd.read_csv(csv_path, parse_dates=[date_col],
                                index_col=date_col)

        # can use uniform to change this
        self.data['t_plus'] = self.data.open.shift(-1)

        self.data.dropna(inplace=True)

        self.df = self.data.copy()
        self.timeframe = '1min'

    def change_resolution(self, new_timeframe):

        resample_dict = {'volume': 'sum', 'open': 'first',
                         'low': 'min', 'high': 'max',
                         'close': 'last',
                         't_plus': 'last'}

        self.df = self.data.resample(new_timeframe).agg(resample_dict)
        self.timeframe = new_timeframe

    def update_sigtime_column(self, output_csv, check_both=False):
        """
        Update the 'sigtime' column based on the conditions specified.

        :param output_csv: the path for the output.csv file.
        :param check_both: Whether to check both 'time_newyork' and
        'time_london' columns, defaults to False.
        """
        if check_both:
            time_columns = ['time_newyork', 'time_london']
        else:
            time_columns = ['time_london']  # can choose 'time_newyork' here

        for time_column in time_columns:
            # Check if the specified time_column exists in the DataFrame
            if time_column not in self.df.columns:
                raise ValueError(
                    f"Column '{time_column}' does not exist in the "
                    f"DataFrame.")

            # Convert the time_column to datetime objects remove seconds and ms
            self.df[time_column] = \
                pd.to_datetime(self.df[time_column]).dt.floor('T')

        # function to set the value of 'sigtime' based on the conditions
        def set_sigtime(row):
            if check_both:
                if row['time_newyork'].hour == 9 and \
                        row['time_newyork'].minute == 30:
                    return 1
                elif row['time_london'].hour == 8 and \
                        row['time_london'].minute == 0:
                    return 1
            else:
                if row['time_newyork'].hour == 9 and \
                        row['time_newyork'].minute == 30:
                    return 1

            return 0

        # Apply the function to each row to update 'sigtime' column
        self.df['sigtime'] = self.df.apply(set_sigtime, axis=1)

        # Save the updated DataFrame back to the CSV file
        self.df.to_csv(output_csv,
                       date_format='%m/%d/%Y %H:%M', index=False)

    def generate_orders(self, lookback, buffer, filename):
        """
        Generates buy/sell orders at the break of the high/low of a previous-
        bar, designated in time by using set_sigtime() and a lookback period.
        """
        self.df['sig_long'] = self.df['high'].rolling(lookback).max()
        self.df['sig_short'] = self.df['low'].rolling(lookback).min()

        signal_df = pd.DataFrame(index=self.df.index,
                                 columns=['long_ord', 'short_ord']).fillna(0)
        long_ord_price, short_ord_price = 0, 0
        long_sig_flag, short_sig_flag = 0, 0

        for row in self.df.itertuples():
            if row.sigtime == 0 and short_sig_flag == long_sig_flag == 0:
                signal_df.loc[row.Index] = [0, 0]
            elif row.sigtime == 1:
                long_ord_price, short_ord_price = row.sig_long + buffer, \
                                                  row.sig_short - buffer
                signal_df.loc[row.Index] = [long_ord_price, short_ord_price]
                long_sig_flag = short_sig_flag = 1
            elif row.sigtime == 0 and (short_sig_flag or long_sig_flag):
                signal_df.loc[row.Index, ['short_ord', 'long_ord']] = [
                    short_ord_price, long_ord_price]

        # Merge the two dataframes and asign to datamanager df

        merged_df = self.df.merge(signal_df, how='left', left_index=True,
                                  right_index=True)
        merged_df[['short_ord', 'long_ord']] = merged_df[
            ['short_ord', 'long_ord']].ffill().bfill()
        merged_df.to_csv(filename)
