import json
import tweepy
from src.configs.api_keys import TwitterKeys as tc

twitter_authenticator = tweepy.AppAuthHandler(
    tc.get_API_KEY(), tc.get_API_KEY_SECRET())


def hello(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def twitter_callback(event, context):
    body = {
        "message": "Callback",
        "input": event,
    }
    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

