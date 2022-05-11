import tweepy
from configs.api_keys import TwitterKeys, MongoKeys
from data_collection.twitter_collector import TwitterCollector
from data_collection.mongo_connector import MongoTwitterCluster
from data_collection.markov_text_generation import TweetCreator


def main():
    desired_user = input("Please Input Desired Twitter User's Handle:\n>")
    client = tweepy.Client(bearer_token=TwitterKeys.get_BEARER_TOKEN(
    ), consumer_key=TwitterKeys.get_API_KEY(), consumer_secret=TwitterKeys.get_API_KEY_SECRET(),
        access_token=TwitterKeys.get_ACCESS_TOKEN(),
        access_token_secret=TwitterKeys.get_ACCESS_TOKEN_SECRET())

    mongo = MongoTwitterCluster(
        cluster_password=MongoKeys.get_cluster_password())

    user_info = mongo.twitter_api.get_user_account_info(
        user_handle=desired_user)
    user_id = str(user_info['id'])

    mongo.insert_user(user_info['username'])
    user_json = [item for item in mongo.get_user(desired_user)]

    sentence_generator = TweetCreator(user_json[0]['username'])
    tweet_sentence = sentence_generator.generate_tweet_text()
    print(tweet_sentence)

    client.create_tweet(text=tweet_sentence)


if __name__ == '__main__':
    main()
