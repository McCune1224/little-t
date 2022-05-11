from mongoengine import *
class TwitterUser(Document):
    twitter_id = StringField(required=True)
    username = StringField(required=True)
    last_updated = DateTimeField(required=True)


