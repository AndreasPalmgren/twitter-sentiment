import tweepy as tw
import requests

def access_twitter():
    access_token = r"WT90c6EeFymch8alktIS6Czjo"
    access_token_secret = r"rapSxOMSspBkqyUSkQ7QsCqoBSl00eJn0lqM44MypligPrSLI3 "
    bearer_token = r"AAAAAAAAAAAAAAAAAAAAAPQdbAEAAAAAip4dX3hfODMZcwy%2F4D9NGsqQlQY%3DhlWENfRydVk69RbpqLE4vNXku5nzgoVeSfYMekfHfDm6pM0LtN "

    client = tw.Client( bearer_token=bearer_token,
                            access_token=access_token, 
                            access_token_secret=access_token_secret, 
                            return_type = requests.Response,
                            wait_on_rate_limit=True)

    return client