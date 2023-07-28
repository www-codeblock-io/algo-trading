# generate_orders.py
from datamanager import DataManager


def generate_sigbar_orders(csv_path, date_col, output_csv):
    """
    Generate orders based on the signal time.

    :param csv_path: Path to the CSV file containing the data.
    :param date_col: Name of the column containing the timestamp in the CSV file.
    :param output_csv: Path to the output CSV file to save the generated orders.
    """
    # Create an instance of the DataManager class and load the data from the CSV
    dmgt = DataManager(csv_path, date_col)

    # Generate orders using the specified lookback period for sigtime in min.
    lookback = 120
    buffer = 2
    dmgt.generate_orders(lookback, buffer, output_csv)


if __name__ == "__main__":
    # Input file paths
    csv_path = "../../data/results/ASRS141/sigtime_dax_2022.csv"
    date_col = "timestamp"
    output_csv = "../../data/results/ASRS141/orders_dax_2022.csv"

    generate_sigbar_orders(csv_path, date_col, output_csv)
