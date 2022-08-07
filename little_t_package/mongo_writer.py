from typing import List
from mongo_connector import MongoConnector
from data.User import TwitterUser
from data.Tweet import Tweet
import tweet_collector
import pymongo.errors


class MongoWriter(MongoConnector):
    """
    Writes to the Mongo Cluster new Twitter User's and their tweets
    """

    def __init__(self) -> None:
        super().__init__()
        return

    def insert_twitter_user(self, user: TwitterUser) -> None:
        """
        Attempt to insert a unique twitter user,
        if they already exist (duplicate key) do nothing
        """
        try:
            self.user_collection.insert_one(user.to_mongo())
        except pymongo.errors.DuplicateKeyError:
            return

    def insert_new_tweets(self, tweets: List[Tweet]) -> int:
        try:
            # ordered = false lets us insert many without duplicates :)
            self.tweet_collection.insert_many(
                [tweet.to_mongo() for tweet in tweets], ordered=False
            )
        # With ordered = False this will fail to write already exsiting tweet_collection entries
        # with the same data (which is a good thing).

        # basically to get the tally of how much was actually inserted into the collection,
        # just compare the # of errors to the length of the orig list

        # ie 150 write attempts and 50 errors = 100 successful new entries
        except pymongo.errors.BulkWriteError as bulk_errors:
            return len(tweets) - len(bulk_errors.details["writeErrors"])

        except Exception as bare_except:
            print(bare_except)
            return 0
        return len(tweets)


if __name__ == "__main__":
    target = input("Give Username: ")

    print("opening connection to db")
    writer = MongoWriter()

    print("API Auth for twitter")
    collector = tweet_collector.TwitterAPIConnector()

    print("getting twitter user details")
    user = collector.get_user(username=target)
    print(user.twitter_id)

    print("getting tweets")
    tweets = collector.get_tweets(user, repeat=True)
    writer.insert_twitter_user(user)
    written = writer.insert_new_tweets(tweets)
    print(f"Wrote a total of {len(tweets)} entries for {user.username}")
