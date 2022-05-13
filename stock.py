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
        "axes.edgecolor" : "grey",
        "axes.linewidth" : 2, 
        "xtick.bottom" : True,
        "xtick.labelbottom" : True,
        "ytick.labelleft" : True,
        "ytick.left" : True,
        "figure.subplot.hspace" : 0.7,
        "figure.titleweight" : "bold",
        "axes.titleweight" : "bold"
    }

    plt.rcParams.update(rc)

def update_gspc(start_value, end_date):

    df_gspc = yf.download("^GSPC", "2022-05-02", end_date)["Close"]
    df_gspc = (1+df_gspc.pct_change()).cumprod() * start_value
    df_gspc[0] = start_value

    df2 = pd.DataFrame(df_gspc).T
    return df2.to_numpy()[0]

    # Save portfolio value
    #filepath = Path('data/gspc_data.csv')
    #filepath.parent.mkdir(parents=True, exist_ok=True)

    #df_gspc.to_csv(filepath)




def update_sentiment(start_value, end_date):
    """
    Return valuation at end of day.
    """
    stock_list = pd.read_csv('data/stock_list.csv')["symbol"]
    df_weights = pd.read_csv('data/weights.csv')

    stock_df = yf.download(stock_list.tolist(), "2022-05-03", end_date)['Close']
    stock_df = 1+stock_df.pct_change()

    valuation = pd.DataFrame({'2022-05-02': [start_value]})

    for i, date in enumerate(df_weights.columns[1:]):
        X =  stock_df.iloc[i+1].to_numpy() * df_weights.iloc[:,i+1]  * start_value

        valuation[str(stock_df.index[i+1]).split(" ")[0]] = X.sum()
        start_value = X.sum()
        
    return valuation

def update_portfolios(start_value, end_date, plot=True):

    df_gspc = update_gspc(start_value, end_date)
    df_sent = update_sentiment(start_value, end_date)

    #df.loc[len(df.index)] = df_gspc
    df = pd.DataFrame(data=np.array([df_sent.to_numpy()[0], df_gspc]).T, 
                        columns=["Sentiment", "S&P 500"], index=df_sent.columns)


    # 0: Sentiment     1: GSPC
    df.to_csv('data/portfolio_values.csv', index_label="date")

    # Plot
    if plot: 
        set_style()

        fig, axs = plt.subplots(1, figsize=(8, 8))

        fig.patch.set_facecolor('#ffffff')
        axs.set_facecolor('#ffffff')

        axs.plot(df.iloc[:,0], label='Sentiment portfolio')
        axs.plot(df.iloc[:,1], label='S&P 500')
        axs.legend()

        plt.savefig("docs\images\portfolios.jpg")


if __name__ == "__main__":

    start_value = 10000

    end_date = "2022-05-13"
    update_portfolios(start_value, end_date)
