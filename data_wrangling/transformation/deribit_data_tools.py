import pandas as pd
from datetime import datetime


def set_start_end_date(csvfile='filename.csv', startdate=None, enddate=None):
    """
    Load a CSV file into a DataFrame and slice it based on a specified start
    and end date.

    Parameters:
        csvfile (str): Path to the CSV file.
        startdate (str or datetime): Start date in the format 'YYYY-MM-DD HH:MM:SS' or as a datetime object.
        enddate (str or datetime): End date in the format 'YYYY-MM-DD HH:MM:SS' or as a datetime object.

    Returns:
        pandas.DataFrame: DataFrame containing the sliced data.

    Example:
        set_start_end_date('data.csv', '2023-01-01 00:00:00', '2023-01-31 23:59:59')
    """
    # Load csv to df
    df = pd.read_csv(csvfile)

    # Convert 'timestamp' column to datetime if it's not already
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Set 'timestamp' as the DataFrame index (if it's not already)
    df.set_index('timestamp', inplace=True)

    # Define the start and end timestamps
    if startdate is not None:
        if isinstance(startdate, str):
            start_timestamp = datetime.strptime(startdate, '%Y-%m-%d %H:%M:%S')
        else:
            start_timestamp = startdate
        df = df.loc[start_timestamp:]

    if enddate is not None:
        if isinstance(enddate, str):
            end_timestamp = datetime.strptime(enddate, '%Y-%m-%d %H:%M:%S')
        else:
            end_timestamp = enddate
        df = df.loc[:end_timestamp]

    return df
