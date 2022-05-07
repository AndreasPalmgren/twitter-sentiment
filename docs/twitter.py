import pandas as pd
from datetime import date
from twitter_access import *

def get_table(tweets, symbol, date):
    # Save data as dictionary
    tweets_dict = tweets.json() 
    
    try:
        # Extract "data" value from dictionary
        tweets_data = tweets_dict['data'] 

        # Transform to pandas Dataframe
        df = pd.json_normalize(tweets_data)
        
        df["symbol"] = symbol
        df["date"] = date
        
        return df
    except:
        pass


def get_tweets(stocks, date=date.today()):
    """
    Get tweets for all stocks during given date.
    """
    for stock in stocks:
        query = f"#{stock} -is:retweet -is:reply lang:en"
        
        tweets = client.search_recent_tweets(query=query, 
                                     start_time=f"{date}T00:00:00Z", 
                                     end_time=f"{date}T23:59:00Z",
                                     max_results=10)
        
        df = pd.concat([df, get_table(tweets, stock, date)], ignore_index=True)
    return df

if __name__ == "__main__":
    client = access_twitter()
    
    sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]

    print(get_tweets("AAPL"))