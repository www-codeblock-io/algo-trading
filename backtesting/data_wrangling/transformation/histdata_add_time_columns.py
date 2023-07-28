import pandas as pd
import pytz


def convert_to_cet_with_dst(dt):
    # Assuming the original data is in Eastern Standard Time (EST) without
    # daylight savings
    est_tz = pytz.timezone('EST')
    cet_tz = pytz.timezone('Europe/Berlin')
    dt_est = est_tz.localize(dt)
    dt_cet = dt_est.astimezone(cet_tz)
    return dt_cet


def add_time_cols(df):
    """
    Add a new column 'time_germany' with Central European Time (CET) with daylight savings
    and store the result in the DataFrame.

    :param df: DataFrame with 'timestamp' as a column
    :return: DataFrame with added 'time_germany' column
    """
    df = df.copy()  # Make a copy to avoid modifying the original DataFrame

    df['timestamp'] = pd.to_datetime(df['timestamp'])  # Convert 'timestamp' to datetime if not already
    df['time_germany'] = df['timestamp'].map(convert_to_cet_with_dst)

    # Drop any duplicate 'time_germany' column if exists
    df = df.loc[:, ~df.columns.duplicated()]

    return df

def main():
    csv_path = '../../data/clean_data/cleaned_dax_jun2023.csv'

    data = pd.read_csv(csv_path)
    data.dropna(inplace=True)

    df_with_time_cols = add_time_cols(data)

    # Drop the duplicate first row
    df_with_time_cols.drop_duplicates(subset=['timestamp'], keep='first', inplace=True)

    # Set 'timestamp' as the index
    df_with_time_cols.set_index('timestamp', inplace=True)

    # Move 'time_germany' column to the column next to the index column
    cols = list(df_with_time_cols.columns)
    cols.remove('time_germany')  # Remove the 'time_germany' column from the list
    cols.insert(1, 'time_germany')  # Insert 'time_germany' as the second column
    df_with_time_cols = df_with_time_cols[cols]

    # Drop the 'Unnamed' column
    df_with_time_cols.drop(columns=['Unnamed: 0'], inplace=True)

    # Save the updated DataFrame back to the CSV file
    df_with_time_cols.to_csv(
        '../../data/clean_data/cleaned_dax_jun2023_timecols.csv',
        date_format='%d/%m/%Y %H:%M', index=True)


if __name__ == "__main__":
    main()
