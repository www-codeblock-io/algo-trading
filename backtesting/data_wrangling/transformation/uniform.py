# Module for testing plotting entry price a random uniformed line.
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('ggplot')

data = pd.read_csv('clean_data/cleaned_btc.csv',
                   parse_dates=['timestamp'],
                   index_col ='timestamp')

print(data.tail(50))

data['t_plus'] = data.open.shift(-1)
data.dropna(inplace=True)
print(data.tail(50))

data['diff_'] = data.t_plus - data.close

data['diff_'].plot(figsize=(6,4))

plt.hist(data.diff_)

del data['diff_']


resample_dict = {'volume': 'sum', 'open': 'first',
                 'low': 'min', 'high': 'max',
                 'close': 'last',
                 't_plus': 'last'}


df = data.resample('5min').agg(resample_dict)
print(df.tail(50))

# show example of drawing from uniform
high = 100.5
low = 99.5

for _ in range(10):
    random_val = np.random.uniform(low, high)
    print(f"simulated entry price is {random_val}")

data['t_plus'] = [np.random.uniform(x,y)\
                    for x,y in zip(data.low.values,data.high.values)]

data['t_plus'] = data.t_plus.shift(-1)
print(data.tail(50))