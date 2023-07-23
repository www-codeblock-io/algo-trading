# add_sigtime.py
from datamanager import DataManager


def main():
    csv_path = '../../data/clean_data/cleaned_btc_jan2023_with_timecols.csv'
    date_col = 'timestamp'
    output_csv = '../../data/clean_data/btc_jan2023_sigtimes.csv'

    dmgt = DataManager(csv_path, date_col)

    # Update sigtime, check_both=False just checks 'time_london' column.
    dmgt.update_sigtime_column(output_csv, check_both=True)


if __name__ == "__main__":
    main()
