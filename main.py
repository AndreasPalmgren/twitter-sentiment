import pandas as pd
import numpy as np
from sentiment_portfolio import portfolio_weights
from twitter import get_tweets
from datetime import date, timedelta
from twitter_access import access_twitter

#sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]["Symbol"]
#pd.DataFrame({'symbol':sp500}).to_csv('data/weights.csv', index=False)


df_weights = pd.read_csv('data/weights.csv')
#df_twitter = pd.read_csv('data/twitter_dataset.csv')
stock_list = pd.read_csv('data/stock_list.csv')

# Date
#yesterday = date.today() - timedelta(days=1)
yesterday = '2022-05-11'

if yesterday in df_weights.columns:
    print("Date already in weights.")
else:

    # Twitter
    client = access_twitter()
    get_tweets(client, stock_list["symbol"], date=yesterday).to_csv('data/twitter_dataset.csv', index=False)


    # Sentiment portfolio
    new_weights = portfolio_weights()
    df_weights[yesterday] = new_weights
    df_weights.to_csv('data/weights.csv', index=False)

    print("Successful update.")
