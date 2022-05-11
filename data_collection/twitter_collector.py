import datetime
from typing import Union
import tweepy


class TwitterCollector():
    def __init__(self, bearer_token: str) -> None:
        self.client = tweepy.Client(bearer_token)

    def get_user_account_info(self, user_handle: str) -> dict:
        """
        Fetch Account info of desired username/twitter handle and return
        a response of the info
        """

        # Drop @ and if they included it
        if user_handle[0] == '@':
            user_handle = user_handle[1:]

        response = self.client.get_user(username=user_handle.lower())
        json_dict = {}
        for item in response.data:
            json_dict[item] = response.data[item]
        json_dict['last_updated'] = datetime.datetime.now()
        return json_dict


    def get_timeline_tweets(self, user_id: Union[str, int], limit: int = 100):
        tweet_collection = []
        """Collect Recent Pagation Tweets of a user"""
        tweets = self.client.get_users_tweets(id=user_id,
                                              exclude=["retweets", "replies"],
                                              max_results=limit,
                                              tweet_fields=["in_reply_to_user_id", "author_id"])
        for tweet_data in tweets.data:
            tweet_collection.append(tweet_data)
        try:
            while tweets.meta['next_token']:

                for tweet_data in tweets.data:
                    tweet_collection.append(tweet_data)
                tweets = self.client.get_users_tweets(id=user_id,
                                                      tweet_fields=[
                                                          "in_reply_to_user_id", "author_id"],
                                                      max_results=limit,
                                                      exclude=[
                                                          'retweets', 'replies'],
                                                      pagination_token=tweets.meta['next_token'])
        except KeyError:
            print(
                f"Ran out of Paginations, collected a total of {len(tweet_collection)} tweets.")
        return tweet_collection
