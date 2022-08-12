import tweepy
from api_keys import TwitterKeys as TC
import text_generation


@static
class LittleTAccount():
    def __init__(self) -> None:
        self.account = tweepy.Client(
                bearer_token= TC.get_BEARER_TOKEN(),
                consumer_key=TC.get_API_KEY(),
                consumer_secret=TC.get_API_KEY_SECRET(),
                access_token=TC.get_ACCESS_TOKEN(),
                access_token_secret=TC.get_ACCESS_TOKEN_SECRET(),
                wait_on_rate_limit=True
                )
        self.id = 1511450491976241152
        self.username = "little_t_bot"
    


