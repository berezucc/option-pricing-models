import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def heatmap_plot(prices, spot_prices, volatilities, option_type):
    # Plot heatmap
    fig, ax = plt.subplots(figsize=(10, 8))

    sns.heatmap(prices, ax=ax, annot=True, fmt=".2f", xticklabels=np.round(spot_prices, 2), yticklabels=np.round(volatilities, 2), cmap="RdYlGn")
    ax.set_title(f'{option_type} Price Heatmap')
    ax.set_xlabel('Spot Price')
    ax.set_ylabel('Volatility')

    plt.tight_layout()
    plt.show()

    return fig