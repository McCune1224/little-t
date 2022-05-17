import pytest
from twitter_collection import tweet_collector
from mongo_database import MongoConnector, MongoReader, MongoWriter
from mongo_database.data import Tweet, User


API = tweet_collector.TwitterAPIConnector()
READER = MongoReader.MongoReader()


@pytest.mark.parametrize("twitter_id", ["858911602053074944", 858911602053074944, "-1", -1])
def test_get_user_by_twitter_id(twitter_id):
    print(type(twitter_id))
    user_search = READER.get_user_by_twitter_id(twitter_id=twitter_id)
    assert user_search != None


@pytest.mark.parametrize("twitter_id", ["858911602053074944", 858911602053074944, "-1", -1])
def test_get_tweets_by_author_id(twitter_id):
    user_search = READER.get_tweets_by_author_id(twitter_id=twitter_id)
    assert user_search != None
