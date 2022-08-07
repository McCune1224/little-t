from typing import List, TypeVar
from mongo_connector import MongoConnector
from data.Tweet import Tweet
from data.User import TwitterUser


A = TypeVar("A", str, int)


class MongoReader(MongoConnector):
    def __init__(self) -> None:
        super().__init__()

    def get_user_by_twitter_id(self, twitter_id: A) -> TwitterUser:
        if isinstance(twitter_id, str):
            try:
                twitter_id = int(twitter_id)
            except ValueError as exc:
                raise ValueError from exc

        cursor = self.user_collection.find_one({"twitter_id": twitter_id})
        if cursor is None:
            raise ValueError("No User Found")
        user = TwitterUser()
        user.twitter_id = cursor["twitter_id"]
        user.username = cursor["username"]
        return user

    def get_tweets_by_author_id(self, twitter_id: A) -> List[Tweet]:
        if isinstance(twitter_id, str):
            try:
                twitter_id = int(twitter_id)
            except TypeError as exc:
                raise TypeError from exc
        tweets = []
        for mongo_tweet in self.tweet_collection.find({"author_id": twitter_id}):
            tweet = Tweet()
            tweet.author_id = mongo_tweet["author_id"]
            tweet.tweet_id = mongo_tweet["tweet_id"]
            tweet.text = mongo_tweet["text"]
            tweets.append(tweet)
        return tweets


if __name__ == "__main__":
    foo = MongoReader()
    me = foo.get_user_by_twitter_id("858911602053074944")
    # tweets_int = foo.get_tweets_by_author_id(858911602053074944)
    # tweets_str = foo.get_tweets_by_author_id("858911602053074944")

    print(me.to_json())
    # tally_a = 0
    # for t in tweets_str.find():
    #     tally_a += 1
    #     print(t)
    # tally_b = 0
    # for t in tweets_int.find():
    #     tally_b += 1
    #     print(t)
    # print(tally_a)
    # print(tally_b)
