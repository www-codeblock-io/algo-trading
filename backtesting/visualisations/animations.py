# animations.py
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation as animation

# Set Seaborn style and context
sns.set_style('darkgrid')
sns.set_context("talk")


# Helper function to handle common configurations
def animate_common_config(frame, x, y, title, xlabel, ylabel, color='blue'):
    plt.gca().clear()
    plt.plot(x[:frame+1], y[:frame+1], color=color.lower(), marker='o')
    plt.title(title, fontsize=12)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(True)


def win_loss_ratio_animation(df):
    df = df[df['returns'] != 0].copy()  # Filter rows with a return of 0 and create a copy
    df['Trade Number'] = range(1, len(df) + 1)  # Add trade number for x-axis
    df['Win'] = (df['returns'] > 0).astype(int)
    df['Cumulative Wins'] = df['Win'].cumsum()
    df['Win/Loss Ratio'] = df['Cumulative Wins'] / df['Trade Number']

    fig, ax = plt.subplots(figsize=(10, 6))

    def update(frame):
        animate_common_config(frame, df['Trade Number'], df['Win/Loss Ratio'],
                              f"Win/Loss Ratio Animation (Total Trades: {frame+1})",
                              'Trade Number', 'Win/Loss Ratio', 'blue')

    ani = animation.FuncAnimation(fig, update, frames=len(df), interval=200, repeat=False)
    plt.tight_layout()  # Prevent x-axis label from being cropped
    plt.subplots_adjust(bottom=0.15)
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    plt.show()


def cum_returns_per_trade_animation(df):
    df = df[df['returns'] != 0]
    df['Trade Number'] = range(1, len(df) + 1)  # Add trade number for x-axis
    df['Cumulative Returns'] = df['returns'].cumsum()

    fig, ax = plt.subplots(figsize=(12, 6))

    def update(frame):
        animate_common_config(frame, df['Trade Number'], df['Cumulative Returns'],
                              f"Cumulative Returns per Trade (Total Trades: {frame+1})",
                              'Trade Number', 'Cumulative Returns')

    ani = animation.FuncAnimation(fig, update, frames=len(df), interval=200, repeat=False)
    plt.tight_layout()  # Prevent x-axis label from being cropped
    plt.subplots_adjust(bottom=0.15)
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    plt.show()


def win_loss_scatter_plot_animation(df):
    df = df[df['returns'] != 0]
    df['Trade Number'] = range(1, len(df) + 1)  # Add trade number for x-axis

    fig, ax = plt.subplots(figsize=(12, 6))
    sc = plt.scatter([], [], c=[], cmap='bwr', alpha=0.5)

    def animate(i):
        sc.set_offsets(df[['Trade Number', 'returns']].values[:i+1])
        sc.set_array(df['returns'].iloc[:i+1])
        plt.title(f'Win/Loss Scatter Plot (Total Trades: {i+1})')
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

