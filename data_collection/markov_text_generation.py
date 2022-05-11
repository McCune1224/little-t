import markovify
import re
import os
import emoji
from configs.api_keys import TwitterKeys, MongoKeys
from data_collection.mongo_connector import MongoTwitterCluster
from data_collection.twitter_collector import TwitterCollector


class TweetCreator():
    def __init__(self, user_handle: str) -> None:
        self.twitter_handle = user_handle
        mongo = MongoTwitterCluster(MongoKeys.get_cluster_password())
        self.tweet_list = mongo.get_tweets(self.twitter_handle)

    def _text_preperation(self):
        text_blob = ""
        sentence_finishers = ['.', '?', '!']
        for tweet in self.tweet_list:
            text = tweet['text']
            # replace http and emoijs
            text = re.sub(r"https?", "", text)
            text = re.sub(r"@", "", text)
            text = emoji.replace_emoji(text, '')

            # add punctuation
            if text[-1] not in sentence_finishers:
                text += '.'
            text_blob += text + " "
        return text_blob

    def generate_tweet_text(self):
        try:
            Markov_Model = markovify.Text(self._text_preperation())
            new_sentence = Markov_Model.make_short_sentence(250)
        except KeyError:
            print("not enough text:\n", self._text_preperation())
            return
        twitter_api = TwitterCollector(TwitterKeys.get_BEARER_TOKEN())
        user = twitter_api.get_user_account_info(self.twitter_handle)
        return f"'{new_sentence}' - {user['username']}"


if __name__ == '__main__':
    sample = []
    test = TweetCreator("@elonmusk")
    print(test.generate_tweet_text())
