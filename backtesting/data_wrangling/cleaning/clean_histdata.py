import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()
plt.style.use('ggplot')

# Load in data from previous video
# Read the data from the CSV file
csv_path = "../../data/clean_data/dax/DAT_MT_GRXEUR_M1_202304.csv"
df = pd.read_csv(csv_path, header=None)

# Rename the columns
new_column_names = {0: 'date', 1: 'time', 2: 'open', 3: 'high', 4: 'low', 5: 'close', 6: 'volume'}
df.rename(columns=new_column_names, inplace=True)

# Combine 'date' and 'time' columns to create the 'timestamp' column
df['timestamp'] = pd.to_datetime(df['date'] + ' ' + df['time'])
df.drop(columns=['date', 'time'], inplace=True)

# Set 'timestamp' as the DataFrame index
df.set_index('timestamp', inplace=True)

# Drop duplicates based on the 'timestamp' column
df.drop_duplicates(keep='first', inplace=True)

# Reset the DataFrame index to make it a regular column again
df.reset_index(inplace=True)

# View the data
plt.plot(df.timestamp, df.close)
plt.title('DAX Close Prices')
plt.xlabel('Timestamp')
plt.ylabel('Close Price')
plt.show()

# Calculate daily returns
df['returns'] = df.close.pct_change()
df.dropna(inplace=True)

# Inspect returns
df.returns.plot()
plt.title('DAX Daily Returns')
plt.xlabel('Timestamp')
plt.ylabel('Returns')
plt.show()

#
# # Create the animation function
# def animate(i):
#     plt.clf()
#     plt.plot(df.timestamp[33900:34000+i], df.close[33900:34000+i])
#     plt.title('Dax Flash Crash')
#     plt.ylabel('DAX PRICE in USD')
#
#
# # Create the figure and animate it
# fig = plt.figure()
# ani = animation.FuncAnimation(fig, animate, frames=len(df['close'][31300:35000]), interval=1)
# plt.show()
#
# # delete unused columns
# del df['volume']
# del df['returns']
#
# # Save the updated DataFrame back to the CSV file
# df.to_csv(
#     '../../data/clean_data/cleaned_dax_jun2023.csv',
#     date_format='%d/%m/%Y %H:%M', index=True)
