import pandas as pd
import numpy as np


class DataLoader:
    """
    Original CSV file needs to just have two columns, 'timestamp' and 'win/lose'
    the timestamp column can be a datetime and the win/lose values are int 1 for
    a win and int -1 for a lossing trade.


    """
    def __init__(self, filepath):
        self.filepath = filepath

    def load_excel(self, sheet_name=None):
        xls = pd.ExcelFile(self.filepath)
        dfs = [xls.parse(sheet_name) for sheet_name in xls.sheet_names]

        reshaped_dfs = [self._clean_and_reshape(df) for df in dfs]

        all_data = pd.concat(reshaped_dfs)
        return all_data

    def _clean_and_reshape(self, df):
        reshaped_data = []
        for i in range(0, df.shape[1], 2):
            month = df.iloc[:, i]
            win_loss = df.iloc[:, i+1]
            is_valid = ~np.isnan(win_loss)
            month = month[is_valid]
            win_loss = win_loss[is_valid]
            if len(month) == 0 or len(win_loss) == 0:
                continue
            temp_df = pd.concat([month, win_loss], axis=1)
            temp_df.columns = ['Date', 'Win/Loss']
            reshaped_data.append(temp_df)
        reshaped_df = pd.concat(reshaped_data)
        reshaped_df = reshaped_df.sort_values('Date').reset_index(drop=True)
        return reshaped_df
