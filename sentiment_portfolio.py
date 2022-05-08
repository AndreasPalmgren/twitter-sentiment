import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from textblob import TextBlob
from datetime import date, timedelta

def get_analysis(score):
    if score < 0:
        return "Negative"
    elif score == 0:
        return "Neutral"
    else:
        return "Positive"
    

def get_polarity(text):
    return TextBlob(text).sentiment.polarity

def clean_text(text):
    """
    Clean tweets.
    """

    text = text.lower()
    text = re.sub(r"@[A-Za-z0-9]+", "", text) #Remove @mention
    text = re.sub(r"#", "", text)   #Remove the '#' symbol
    text = re.sub(r"RT[\s]+", "", text)   # Remove retweet
    text = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", text)   # Remove hyperlink
    text = re.sub(r"\n"," ", text)

    return text

def get_weights(df):
    
    total = df[["symbol", "Analysis"]].groupby(by=["symbol"]).agg(['count']).reset_index()
    total.columns = total.columns.get_level_values(0)

    positives = df[["symbol", "Analysis"]][df["Analysis"]=="Positive"].groupby(by=["symbol"]).agg(['count']).reset_index()
    positives.columns = positives.columns.get_level_values(0)

    df = pd.merge(total, positives, on="symbol", how="left")
    
    # Get all symbols even if no tweets
    sp500 = pd.read_csv('data/stock_list.csv')
    df = pd.merge(sp500, df, on="symbol", how="left")

    df["score"] = df["Analysis_y"].div(df["Analysis_x"])
    df["weight"] = df["score"]/df["score"].sum()

    return df.fillna(0)



def portfolio_weights():

    df = pd.read_csv("data/twitter_dataset.csv")

    df["text_clean"] = df["text"].apply(clean_text)

    # Basic sentiment
    df["Polarity"] = df["text_clean"].apply(get_polarity)
    df["Analysis"] = df["Polarity"].apply(get_analysis)

    df = get_weights(df)
    
    return df["weight"]
    


if __name__ == "__main__":

    new_weights = portfolio_weights()

    #yesterday = date.today() - timedelta(days=1)
    yesterday = "2022-05-06"

    df_weights = pd.read_csv('data/weights.csv')
    df_weights[yesterday] = new_weights
    df_weights.to_csv('data/weights.csv', index=False)

