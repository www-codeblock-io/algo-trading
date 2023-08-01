# backtest_visuals.py
import pandas as pd
import plots
import animations
from matplotlib.backends.backend_pdf import PdfPages


def main():
    file_path = '../data/results/VW141/VW141_backtest_results.csv'
    df = pd.read_csv(file_path, parse_dates=['timestamp'], dayfirst=True)

    # Ignore rows with returns of 0
    df = df[df['returns'] != 0]

    df['timestamp'] = pd.to_datetime(df['timestamp'])

    with PdfPages('../data/results/VW141/vw141_total_period_plots') as pdf_pages:
        plot_functions = [plots.cumulative_returns_per_trade,
                          plots.monthly_cumulative_returns,
                          plots.win_loss_pie_chart,
                          plots.win_loss_ratio,
                          plots.drawdown_lengths,
                          plots.win_loss_heatmap,
                          # plots.cumulative_wins_3d,
                          # plots.monthly_win_loss_bar,
                          # plots.box_plots_by_month,
                          # plots.win_loss_scatter_plot,
                          plots.density_plots]

        for plot_function in plot_functions:
            plot_function(df, pdf_pages)

    animate_functions = [animations.win_loss_ratio_animation,
                         #animations.win_loss_scatter_plot_animation,
                         animations.cum_returns_per_trade_animation]

    for animate_function in animate_functions:
        animate_function(df)


if __name__ == '__main__':
    main()
