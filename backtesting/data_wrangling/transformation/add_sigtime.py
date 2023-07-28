# add_sigtime.py
from datamanager import DataManager


def main():
    csv_path = '../../data/clean_data/cleaned_dax_jan2023_timecols.csv'
    date_col = 'timestamp'
    output_csv = \
        '../../data/results/ASRS141/sigtime_dax_jan2023.csv'

    dmgt = DataManager(csv_path, date_col)

    # Update sigtime, check_both=False just checks 'time_london' column.
    dmgt.update_sigtime_column(output_csv, check_both=False)


if __name__ == "__main__":
    main()
