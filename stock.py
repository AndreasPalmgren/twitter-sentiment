import yfinance as yf
import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


#sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]

#dt = yf.download(sp500["Symbol"].to_list(), "2021-03-01", "2022-03-30")

def set_style():
    rc = {
        "axes.spines.left" : True,
        "axes.spines.right" : False,
        "axes.spines.bottom" : True,
        "axes.spines.top" : False,
        "axes.edgecolor" : "#512f5c",
        "axes.linewidth" : 6, 
        "xtick.bottom" : True,
        "xtick.labelbottom" : True,
        "ytick.labelleft" : True,
        "ytick.left" : True,
        "figure.subplot.hspace" : 0.7,
        "figure.titleweight" : "bold",
        "axes.titleweight" : "bold"
    }

    plt.rcParams.update(rc)

def update_gspc(start_value=10000, plot_gspc=True):

    df_gspc = yf.download("^GSPC", "2021-03-14", "2022-04-15")["Close"]
    df_gspc = (1+df_gspc.pct_change()).cumprod() * start_value
    df_gspc[0] = start_value

    # Save portfolio value
    filepath = Path('data/gspc_data.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)

    df_gspc.to_csv(filepath)

    # Plot
    if plot_gspc: 
        set_style()

        fig, axs = plt.subplots(1, figsize=(8, 8))

        fig.patch.set_facecolor('#13011a')
        axs.set_facecolor('#13011a')
        axs.tick_params(axis='x', colors='#b760d1')
        axs.tick_params(axis='y', colors='#b760d1')

        axs.plot(df_gspc)
        plt.savefig("docs\images\gspc.png")

if __name__ == "__main__":
    update_gspc()