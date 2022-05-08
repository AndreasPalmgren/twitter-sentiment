import pandas as pd
from datetime import date, timedelta
from twitter_access import access_twitter

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


def get_tweets(client, stocks, date):
    """
    Get tweets for all stocks during given date.
    """
    df = pd.DataFrame(columns=["symbol", "id", "text"])
    for stock in stocks:
        query = f"#{stock} -is:retweet -is:reply lang:en"
        
        tweets = client.search_recent_tweets(query=query, 
                                     start_time=f"{date}T00:00:00Z", 
                                     end_time=f"{date}T23:59:00Z",
                                     max_results=100)
        
        df = pd.concat([df, get_table(tweets, stock, date)], ignore_index=True)
    return df

if __name__ == "__main__":
    client = access_twitter()
    
    stock_list = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]["Symbol"]

    yesterday = date.today() - timedelta(days=1)

    get_tweets(client, stock_list, date=yesterday).to_csv('data/twitter_dataset.csv', index=False)