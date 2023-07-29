# visualisations.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime
import matplotlib.animation as animation
import matplotlib.dates as mdates
import matplotlib.colors as mcolors

# Set Seaborn style and context
sns.set_style('darkgrid')
sns.set_context("talk")


def cum_returns_per_month(df):
    df['YearMonth'] = df['Date'].dt.to_period('M')
    monthly_returns = df.groupby(['YearMonth'])['Win/Loss'].sum()

    # Calculate cumulative return for each month
    cumulative_returns = monthly_returns.cumsum()

    plt.figure(figsize=(12, 6))

    # Convert PeriodIndex to string representation for plotting
    x_labels = cumulative_returns.index.strftime('%b%y')

    # Plot cumulative returns
    plt.plot(x_labels, cumulative_returns, label='Cumulative Return', color='blue', marker='o')

    plt.xlabel('Month', fontsize=10)
    plt.ylabel('Cumulative Return', fontsize=10)
    plt.title(f'Monthly Cumulative Return (Total Trades: {len(df)})', fontsize=10)

    plt.legend()  # Show legend for the cumulative return line
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
    plt.grid(True)
    plt.tight_layout()  # Prevent x-axis label from being cropped
    plt.show()


def cum_returns_per_trade(df):
    df['Cumulative Returns'] = df['Win/Loss'].cumsum()

    plt.figure(figsize=(12, 6))

    # Plot cumulative returns per trade
    plt.plot(df.index, df['Cumulative Returns'], label='Cumulative Returns per Trade', color='blue', marker='o')

    plt.xlabel('Trade Number', fontsize=10)
    plt.ylabel('Cumulative Returns', fontsize=10)
    plt.title(f'Cumulative Returns per Trade (Total Trades: {len(df)})', fontsize=10)

    plt.legend()  # Show legend for the cumulative returns line
    plt.grid(True)
    plt.tight_layout()  # Prevent x-axis label from being cropped
    plt.show()


def monthly_win_loss_bar(df):
    df['YearMonth'] = df['Date'].dt.to_period('M')
    monthly_counts = df.groupby(['YearMonth', 'Win/Loss']).size().unstack(
        fill_value=0)
    monthly_counts = monthly_counts[[1, -1]]

    # Convert the index to string
    monthly_counts.index = monthly_counts.index.astype(str)

    monthly_counts.plot(kind='bar', stacked=True, figsize=(12, 6),
                        color=['lightblue', 'salmon'])
    plt.xlabel('Month', fontsize=10)
    plt.ylabel('Number of Trades', fontsize=10)
    plt.title(f'Monthly Win/Loss Counts (Total Trades: {len(df)})', fontsize=10)
    plt.gcf().autofmt_xdate()
    plt.subplots_adjust(bottom=0.15)
    plt.grid(True)
    plt.tight_layout()  # Prevent x-axis label from being cropped
    plt.show()


def win_loss_ratio(df):
    df['Win'] = (df['Win/Loss'] == 1).astype(int)
    df['Cumulative Wins'] = df['Win'].cumsum()
    df['Cumulative Trades'] = df.index + 1
    df['Win/Loss Ratio'] = df['Cumulative Wins'] / df['Cumulative Trades']

    # Convert the 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['Date'], df['Win/Loss Ratio'], color=mcolors.to_rgba('blue', alpha=0.8), linewidth=2)
    ax.set_xlabel('Date', fontsize=10)
    ax.set_ylabel('Win/Loss Ratio', fontsize=10)
    ax.set_title('Win/Loss Ratio Over Time', fontsize=10)
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))

    # Set the date format for the x-axis to "Jan23"
    date_format = mdates.DateFormatter('%b%y')
    ax.xaxis.set_major_formatter(date_format)

    # Adjust font size for x-axis labels
    for tick in ax.get_xticklabels():
        tick.set_fontsize(10)

    # Adjust font size for y-axis labels
    for tick in ax.get_yticklabels():
        tick.set_fontsize(10)

    ax.grid(True)
    plt.tight_layout()  # Prevent x-axis label from being cropped
    plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility

    plt.show()


def win_loss_heatmap(df):
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.strftime('%b')  # Format month as 'Jan'
    heatmap_data = df.groupby(['Year', 'Month'])['Win/Loss'].sum().unstack()

    plt.figure(figsize=(12, 6))
    sns.heatmap(heatmap_data, cmap='coolwarm', center=0)
    plt.title('Win/Loss Heatmap by Month', fontsize=10)
    plt.tight_layout()  # Prevent x-axis label from being cropped
    plt.show()


def box_plots_by_month(df):
    df['Month'] = df['Date'].dt.month
    df.boxplot(column='Win/Loss', by='Month', grid=False, figsize=(12, 6), color=dict(boxes='skyblue', whiskers='black', medians='red', caps='black'))
    plt.title('Box Plots of Win/Loss by Month', fontsize=10)
    plt.suptitle('', fontsize=10)  # remove auto-generated title
    plt.tight_layout()  # Prevent x-axis label from being cropped
    plt.show()


def density_plots(df):
    df['Drawdown'] = (df['Win/Loss'] == -1).astype(int)
    drawdowns = []
    streaks = []
    length = 0
    for i in df['Drawdown']:
        if i == 1:
            length += 1
        elif length > 0:
            drawdowns.append(length)
            length = 0
        streaks.append(length)

    plt.figure(figsize=(12, 6))
    sns.kdeplot(drawdowns, fill=True, color='salmon')
    plt.xlabel('Streak Length', fontsize=10)
    plt.title('Density Plot of Losing Streak Lengths', fontsize=10)
    plt.tight_layout()  # Prevent x-axis label from being cropped
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.kdeplot(streaks, fill=True, color='skyblue')
    plt.xlabel('Streak Length', fontsize=10)
    plt.title('Density Plot of Winning Streak Lengths', fontsize=10)
    plt.tight_layout()  # Prevent x-axis label from being cropped
    plt.show()


def cumulative_wins_3d(df):
    df['Win'] = (df['Win/Loss'] == 1).astype(int)
    df['Cumulative Wins'] = df['Win'].cumsum()
    df['TradeNumber'] = range(1, len(df) + 1)
    df['DateNumerical'] = df['Date'].apply(lambda date: date.toordinal())

    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(df['TradeNumber'], df['DateNumerical'], df['Cumulative Wins'], color='skyblue', linewidth=2)
    ax.set_xlabel('Trade Number', fontsize=10)
    date_ticks = ax.get_yticks()
    ax.set_yticklabels([datetime.fromordinal(int(date_tick)).date() for date_tick in date_ticks])
    ax.set_ylabel('Date', fontsize=10)
    ax.set_zlabel('Cumulative Wins', fontsize=10)
    plt.title('3D Plot of Cumulative Wins Over Time', fontsize=10)
    plt.tight_layout()  # Prevent x-axis label from being cropped
    plt.show()


def drawdown_lengths(df):
    df['Drawdown'] = (df['Win/Loss'] == -1).astype(int)
    drawdowns = []
    length = 0
    for i in df['Drawdown']:
        if i == 1:
            length += 1
        elif length > 0:
            drawdowns.append(length)
            length = 0

    # Add the last drawdown if it hasn't ended
    if length > 0:
        drawdowns.append(length)

    total_trades = len(df)

    if not drawdowns:
        print("No drawdowns in the data.")
    else:
        plt.hist(drawdowns, bins=range(1, max(drawdowns) + 2), align='left', rwidth=0.8)
        plt.xlabel('Drawdown Length', fontsize=10)
        plt.ylabel('Frequency', fontsize=10)
        plt.title(f'Histogram of Drawdown Lengths (Total Trades: {total_trades})', fontsize=10)
        plt.grid(True)
        plt.tight_layout()  # Prevent x-axis label from being cropped
        plt.show()


def win_loss_pie_chart(df):
    win_loss_counts = df['Win/Loss'].value_counts()
    win_loss_counts.index = ['Win' if i == 1 else 'Loss' for i in win_loss_counts.index]

    win_loss_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, figsize=(6, 6))
    plt.ylabel('', fontsize=10)  # This is to remove the 'None' ylabel.
    plt.title('Win/Loss Proportions', fontsize=10)
    plt.tight_layout()  # Prevent x-axis label from being cropped
    plt.show()


def win_loss_scatter_plot(df):
    df['TradeNumber'] = range(1, len(df) + 1)  # add trade number for x-axis

    plt.figure(figsize=(12, 6))
    plt.scatter(df['TradeNumber'], df['Win/Loss'], c=df['Win/Loss'], cmap='bwr', alpha=0.5)
    plt.plot(df['TradeNumber'], df['Win/Loss'], color='black', linewidth=0.5, alpha=0.5)  # added line plot
    plt.yticks([0, 1], fontsize=10)  # set yticks to just 1 or 0
    plt.xlabel('Trade Number', fontsize=10)
    plt.ylabel('Win/Loss', fontsize=10)
    plt.title('Win/Loss Scatter Plot', fontsize=10)
    plt.grid(True)
    plt.tight_layout()  # Prevent x-axis label from being cropped
    plt.show()


def win_loss_ratio_animation(df):
    df = df.copy()
    df['Win'] = (df['Win/Loss'] == 1).astype(int)
    df['Cumulative Wins'] = df['Win'].cumsum()
    df['Cumulative Trades'] = df.index + 1
    df['Win/Loss Ratio'] = df['Cumulative Wins'] / df['Cumulative Trades']

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title("Win/Loss Ratio Animation", fontsize=16)
    ax.set_xlabel("Trade Count", fontsize=12)
    ax.set_ylabel("Win/Loss Ratio", fontsize=12)

    def update(frame):
        ax.clear()
        ax.plot(df['Cumulative Trades'][:frame], df['Win/Loss Ratio'][:frame], color='b', marker='o')
        ax.set_title("Win/Loss Ratio Animation", fontsize=16)
        ax.set_xlabel("Trade Count", fontsize=12)
        ax.set_ylabel("Win/Loss Ratio", fontsize=12)
        ax.set_xlim(0, df['Cumulative Trades'].max() + 1)

    ani = animation.FuncAnimation(fig, update, frames=len(df), interval=200, repeat=False)
    plt.tight_layout()  # Prevent x-axis label from being cropped
    plt.show()


def cum_returns_per_trade_animation(df):
    df['Cumulative Returns'] = df['Win/Loss'].cumsum()

    fig, ax = plt.subplots(figsize=(12, 6))

    def update(frame):
        ax.clear()
        ax.plot(df.index[:frame], df['Cumulative Returns'][:frame], label='Cumulative Returns per Trade', color='blue', marker='o')
        ax.set_xlabel('Trade Number', fontsize=10)
        ax.set_ylabel('Cumulative Returns', fontsize=10)
        ax.set_title(f'Cumulative Returns per Trade (Total Trades: {len(df)})', fontsize=10)
        ax.legend()  # Show legend for the cumulative returns line
        ax.grid(True)
        ax.set_xticks(df.index[:frame], minor=False)
        ax.set_xticklabels(df.index[:frame], rotation=45, ha='right', minor=False)
        ax.tick_params(axis='x', labelsize=8)
        ax.tick_params(axis='y', labelsize=8)

    ani = animation.FuncAnimation(fig, update, frames=len(df), interval=200, repeat=False)
    plt.tight_layout()  # Prevent x-axis label from being cropped
    plt.show()


def win_loss_scatter_plot_animation(df):
    df['TradeNumber'] = range(1, len(df) + 1)  # add trade number for x-axis

    plt.figure(figsize=(12, 6))
    plt.xlabel('Trade Number', fontsize=10)
    plt.ylabel('Win/Loss', fontsize=10)
    plt.title('Win/Loss Scatter Plot', fontsize=10)
    plt.grid(True)
    plt.tight_layout()  # Prevent x-axis label from being cropped

    sc = plt.scatter([], [], c=[], cmap='bwr', alpha=0.5)

    def animate(i):
        sc.set_offsets(df[['TradeNumber', 'Win/Loss']].iloc[:i])
        sc.set_array(df['Win/Loss'].iloc[:i])
        return sc,

    ani = animation.FuncAnimation(plt.gcf(), animate, frames=len(df), interval=100, blit=True)
    plt.show()

