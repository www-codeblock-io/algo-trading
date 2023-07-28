import pandas as pd


def append_csv_files(file1, file2, output_file):
    """
    Append the contents of file2 below file1 and save the result to output_file.

    :param file1: Path to the first CSV file.
    :param file2: Path to the second CSV file.
    :param output_file: Path to the output CSV file to save the combined data.
    """
    # Load data from the CSV files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Append df2 below df1
    combined_df = df1.append(df2, ignore_index=True)

    # Save the combined data to the output CSV file
    combined_df.to_csv(output_file, index=False)


if __name__ == "__main__":
    # Input file paths
    file1 = "../../data/test_data/BTCMC/final/jun-dec_2022.csv"
    file2 = "../../data/test_data/BTCMC/final/jan-jun_2023.csv"
    output_file = 'backtesting/data/test_data/final_test_data.csv'

    append_csv_files(file1, file2, output_file)
