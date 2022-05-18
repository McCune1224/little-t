import pytest
from twitter_collection import tweet_collector


API = tweet_collector.TwitterAPIConnector()


@pytest.mark.parametrize("id", [858911602053074944, "858911602053074944", -1])
def test_get_twitter_user_by_id(id):
    response = API.get_user(id=id)
    assert response != None
    assert len(response.errors) == 0


@pytest.mark.parametrize("username", ["KusaAlexM", "@KusaAlexM", "INVALID_USERNAME"])
def test_get_twitter_user_by_username(username):
    response = API.get_user(username=username)
    assert response != None
    assert len(response.errors) == 0


@pytest.mark.parametrize("username, amount, repeat", [("@KusaAlexM", 3, False), ("@INVALID_USERNAME", 3, False)])
def test_get_tweets_none_repeated(username, amount, repeat):
    response = API.get_tweets(username=username, amount=amount, repeat=repeat)
    assert response != None
    print(response)
    assert len(response.errors) == 0


@pytest.mark.parametrize("username, amount, repeat", [("@KusaAlexM", 3, False), ("@JoeBiden", 3, False)])
def test_get_tweets_repeated(username, amount, repeat):
    pass
