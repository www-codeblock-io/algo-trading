# run.py
from data_loader import DataLoader
import visualisations

# Create an instance of DataLoader
# replace with your actual file path
loader = DataLoader('data/results/NewYork/BTCopen_backtest_results.xlsx')

# Load the data
#df = loader.load_csv()  # Uncomment if loading via csv
df = loader.load_excel()

# Call the visualisation functions
visualisations.cum_returns_per_month(df)
visualisations.cum_returns_per_trade(df)
visualisations.monthly_win_loss_bar(df)
visualisations.win_loss_ratio(df)
visualisations.drawdown_lengths(df)
visualisations.win_loss_pie_chart(df)
visualisations.win_loss_heatmap(df)
visualisations.density_plots(df)
#visualisations.cumulative_wins_3d(df)

#visualisations.box_plots_by_month(df)
#visualisations.win_loss_scatter_plot(df)

# Call the animated functions
visualisations.win_loss_ratio_animation(df)
visualisations.cum_returns_per_trade_animation(df)
#visualisations.win_loss_scatter_plot_animation(df)
