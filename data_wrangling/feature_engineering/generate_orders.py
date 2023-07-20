# generate_orders.py

# Import the DataManager class from the feature_creation module
from feature_creation import DataManager

# Define the path to starting data
csv_path = "../../backtesting/data/clean_data/btc_jan2023.csv"

# Specify the name of the column containing timestamps
date_col = 'timestamp'
output_filename = \
    "../../backtesting/data/clean_data/btc_jan2023_with_sigbar_orders.csv"

# Create an instance of the DataManager class and load the data from the CSV
dmgt = DataManager(csv_path, date_col)

dmgt.set_sigtime(8, 0)  # Set the signal time to 8:00 AM (08:00 hours)
lookback = 60  # Set size for sigbar (in minutes)

# Generate orders using the specified lookback period
dmgt.generate_orders(lookback, output_filename)






















