from mongoengine import *

class Tweet(Document):
    author_id = StringField(required=True)
    tweet_id = StringField(required=True)
    text = StringField(required=True) 
    created_at = DateTimeField(required=True)


