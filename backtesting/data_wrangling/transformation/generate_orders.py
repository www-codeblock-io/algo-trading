# generate_orders.py
from datamanager import DataManager


def generate_sigbar_orders(csv_path, date_col, output_csv):
    # Create an instance of the DataManager class and load the data from the CSV
    dmgt = DataManager(csv_path, date_col)

    # Generate orders using the specified lookback period for sigtime in min.
    lookback = 60
    buffer = 2
    dmgt.generate_orders(lookback, buffer, output_csv)






















