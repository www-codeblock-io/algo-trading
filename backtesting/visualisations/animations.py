# animations.py
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation as animation

# Set Seaborn style and context
sns.set_style('darkgrid')
sns.set_context("talk")


# Helper function to handle common configurations
def animate_common_config(frame, df, title, xlabel, ylabel, color='blue'):
    plt.gca().clear()
    plt.plot(df.index[:frame], df.iloc[:frame], color=color, marker='o')
    plt.title(title, fontsize=12)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(True)


def win_loss_ratio_animation(df):
    df = df.copy()
    df['Win'] = (df['returns'] == 1).astype(int)
    df['Cumulative Wins'] = df['Win'].cumsum()
    df['Cumulative Trades'] = df.index + 1
    df['Win/Loss Ratio'] = df['Cumulative Wins'] / df['Cumulative Trades']

    fig, ax = plt.subplots(figsize=(10, 6))

    def update(frame):
        animate_common_config(frame, df['Win/Loss Ratio'], "Win/Loss Ratio Animation", "Trade Count", "Win/Loss Ratio")

    ani = animation.FuncAnimation(fig, update, frames=len(df), interval=200, repeat=False)
    plt.tight_layout()  # Prevent x-axis label from being cropped
    plt.subplots_adjust(bottom=0.15)
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    plt.show()


def cum_returns_per_trade_animation(df):
    df['Cumulative Returns'] = df['returns'].cumsum()

    fig, ax = plt.subplots(figsize=(12, 6))

    def update(frame):
        animate_common_config(frame, df['Cumulative Returns'], f'Cumulative Returns per Trade (Total Trades: {len(df)})', 'Trade Count', 'Cumulative Returns')

    ani = animation.FuncAnimation(fig, update, frames=len(df), interval=200, repeat=False)
    plt.tight_layout()  # Prevent x-axis label from being cropped
    plt.subplots_adjust(bottom=0.15)
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    plt.show()


def win_loss_scatter_plot_animation(df):
    df['TradeNumber'] = range(1, len(df) + 1)  # add trade number for x-axis

    fig, ax = plt.subplots(figsize=(12, 6))
    sc = plt.scatter([], [], c=[], cmap='bwr', alpha=0.5)

    def animate(i):
        sc.set_offsets(df[['TradeNumber', 'returns']].iloc[:i])
        sc.set_array(df['returns'].iloc[:i])
        plt.title('Win/Loss Scatter Plot')
        plt.xlabel('Trade Number')
        plt.ylabel('returns')
        plt.grid(True)
        return sc,

    ani = animation.FuncAnimation(fig, animate, frames=len(df), interval=100, blit=True)
    plt.tight_layout()  # Prevent x-axis label from being cropped
    plt.subplots_adjust(bottom=0.25)
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    plt.show()
