# add_time_columns.py
import pandas as pd
import pytz


def add_time_cols(df):
    """
    Convert Unix time index col to New York datetime and London datetime
    and store the result in the DataFrame.

    :param df: DataFrame with Unix timestamp as the index
    :return: DataFrame with added 'time_london' and 'time_newyork' columns
    """
    # Localize the index to UTC timezone if it's tz-naive
    if df.index.tz is None:
        df.index = df.index.tz_localize('UTC')

    # Convert localized Unix timestamp to New York timezone
    ny_timezone = pytz.timezone('America/New_York')
    df['time_newyork'] = df.index.tz_convert(ny_timezone).strftime(
        '%d/%m/%Y %H:%M')

    # Convert localized Unix timestamp to London timezone
    ldn_timezone = pytz.timezone('Europe/London')
    df['time_london'] = df.index.tz_convert(ldn_timezone).strftime(
        '%d/%m/%Y %H:%M')

    # Rearrange columns
    df = df[
        ['time_london', 'time_newyork', 'volume', 'open', 'low', 'high',
         'close']]

    return df


def main():
    csv_path = 'clean_data/cleaned_btc_2023.csv'
    date_col = 'timestamp'

    data = pd.read_csv(csv_path, parse_dates=[date_col], index_col=date_col)
    data.dropna(inplace=True)

    df_with_time_cols = add_time_cols(data)

    # Save the updated DataFrame back to the CSV file
    df_with_time_cols.to_csv(
        '../../data/clean_data/cleaned_btc_2023_timecols.csv',
        date_format='%d/%m/%Y %H:%M', index=True)


if __name__ == "__main__":
    main()
