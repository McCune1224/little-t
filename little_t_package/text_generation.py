from typing import List
import markovify
import re
import emoji
from data.Tweet import Tweet
from tweet_collector import TwitterAPIConnector
from mongo_reader import MongoReader
from mongo_writer import MongoWriter


class MarkovTweetGeneration:
    def __init__(self, tweets: List[Tweet], username: str) -> None:
        self.username = username
        self.tweets = tweets
        self.buildable = False
        if len(self.tweets) > 50:
            self.buildable = True

    def _text_preperation(self):
        text_blob = ""
        sentence_finishers = [".", "?", "!"]
        print(f"Building from a list of {len(self.tweets)} tweets...")
        for tweet in tweets:
            # have to wrap as string class because the ClassString from MongoDB throws errors :(
            text = str(tweet.text)

            # replace http(s)
            if re.search(r"http?s://t.co/\w{4,10}", text):
                text = re.sub(r"http?s://t.co/\w{4,10}", "", text)
                text = text[: len(text) - 1]

            # BEGONE EMOJIS
            text = emoji.replace_emoji(text, "")
            text = re.sub(r"@", "", text)

            # add punctuation
            if len(text) == 1 or len(text) == 0:
                continue

            # occasional sentence will start with a blank, so add a '.' to close
            if text[-1] not in sentence_finishers:
                text += "."
            text = text.capitalize()
            text_blob += text + " "
        return text_blob

    def generate_tweet_text(self):
        if self.buildable == False:
            return f"50 Tweets needed for suitable text generation, have {len(self.tweets)} from {self.username}"
        text_corpus = self._text_preperation()
        markov_model = markovify.Text(input_text=text_corpus, well_formed=False)
        try:
            new_sentence = markov_model.make_short_sentence(
                min_chars=70, max_chars=280, tries=100
            ).capitalize()
        # TooSmall
        except KeyError:
            return
        if new_sentence[0:2] == ". ":
            new_sentence = new_sentence[2:]
        return f"'{new_sentence}' - {self.username}"


if __name__ == "__main__":
    tweets = []
    requested_user = input("Twitter Handle: ")
    twitter_collector = TwitterAPIConnector()
    account_details = twitter_collector.get_user(username=requested_user)

    reader = MongoReader()
    # Case where user doesn't exist yet
    try:
        tw = reader.get_user_by_twitter_id(account_details.twitter_id)

    except ValueError:
        print("New user! Pulling tweets and account details from Twitter...")
        writer = MongoWriter()
        writer.insert_twitter_user(account_details)
        tweets = twitter_collector.get_tweets(account_details, repeat=True)
        writer.insert_new_tweets(tweets)

    # We don't have a new user, so just pull tweets from the db
    if len(tweets) == 0:
        tweets = reader.get_tweets_by_author_id(account_details.twitter_id)
    print(f"Building Model for {requested_user}\n")
    test_model = MarkovTweetGeneration(tweets, account_details.username)
    print(test_model.generate_tweet_text())
