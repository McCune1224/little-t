from json.encoder import JSONEncoder
import pymongo
from data_collection.data.Tweets import Tweet
from data_collection.data.User import TwitterUser
from data_collection.twitter_collector import TwitterCollector
from configs.api_keys import *


class MongoTwitterCluster():

    def __init__(self, cluster_password) -> None:
        self.cluster_password = cluster_password
        self.client = pymongo.MongoClient(
            f"mongodb+srv://little_t:{self.cluster_password}@clustertwitter.vd6bg.mongodb.net/ClusterTwitter?retryWrites=true&w=majority")
        self.db = self.client['tweetDB']
        self.user_collection = self.db['UserAccounts']
        self.tweet_collection = self.db['TweetDumps']
        self.twitter_api = TwitterCollector(TwitterKeys.get_BEARER_TOKEN())

    def insert_user(self, twitter_handle: str):
        try:
            user_data = self.twitter_api.get_user_account_info(twitter_handle)

            twitter_user = TwitterUser()
            twitter_user.twitter_id = str(user_data['id'])
            twitter_user.username = user_data['username'].lower()
            twitter_user.last_updated = user_data['last_updated']

            self.user_collection.insert_one(twitter_user.to_mongo())
        except Exception as e:
            print(e)
    def get_user(self, twitter_handle: str):
        return self.user_collection.find({'username': twitter_handle})

    def insert_tweets(self, twitter_user: TwitterUser):
        tweets = self.twitter_api.get_timeline_tweets(
            twitter_user['twitter_id'])

        for _, tweet_response in enumerate(tweets):
            try:
                tweet = Tweet()
                tweet.author_id = twitter_user['twitter_id']
                tweet.tweet_id = tweet_response['id']
                tweet.text = tweet_response['text']
                self.tweet_collection.insert_one(tweet.to_mongo())
            except Exception as e:
                continue

    def get_tweets(self, twitter_handle: str):
        user = self.twitter_api.get_user_account_info(twitter_handle)
        tweet_list = [tweet for tweet in self.tweet_collection.find(
            {'author_id': str(user["id"])})]
        return tweet_list


if __name__ == '__main__':
    print("foo")
