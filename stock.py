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

    df_gspc = yf.download("^GSPC", "2022-03-14", "2022-04-15")["Close"]

    filepath = Path('data/gspc_data.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)  

    df_gspc.to_csv(filepath)

    if plot_gspc: 
        set_style()

        fig, axs = plt.subplots(1, figsize=(15, 12))
        axs.plot(df_gspc)
        plt.savefig("image\gspc.png")

if __name__ == "__main__":
    update_gspc()