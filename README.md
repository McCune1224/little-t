# Overview 📋
Little_t is designed to copy a user's writing style by collecting a user's previous tweets and then responding to the requested user a sentence similar to that of the target. This process is explained below. 
- Unfortunately with recent [Twitter Premium API Deprecation changes](https://twittercommunity.com/t/deprecating-the-premium-v1-1-api/191092) made in April of 2023 this project no longer has a sustainable way to be continued due to the 100$ fee to continue to utlize the Account Activity API which this project relied upon. Perhaps this change will be reverted in the future or another alternative solution can be found, but until then this is the last version of the project. 


### 🐣 Check out his old tweets: https://twitter.com/little_t_bot 🐣
# How It Works ❔

### 1. Webook Subscription to [Twitter's Web API](https://developer.twitter.com/en/docs/twitter-api/enterprise/account-activity-api/quick-start/enterprise-account-activity-api) via AWS Lambda Deploy of a HTTP Flask API. 
- Setup callback and webhook urls for Twitter to send real time tweet activity 
- Subscribe to Little_t_bot's account to get real time POST request information from Twitter (Tweets, Direct Messages, Mentions, Likes, etc...)
- Parse payload information to know when a user requests for little_t to copy someone.

### 2. Call to [Twitter's Web API](https://developer.twitter.com/en/docs/twitter-api) with a given twitter handle (@username) to collect the following peices of information:
  - Twitter ID
  - Current User Name
  - User's Previous [Timeline Tweets](https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/overview) (up to 3200 recent tweets excluding retweets and comments) 

### 2. Use a MongoDB Cluster to organize the the searched data into two collections:
  - One Collection called UserAccounts to store the user's Twitter ID, username, and a UTC timestamp of when that user was last requested. 
  - The other Collection called TweetDumps to dump the Twitter ID of the poster, Tweet ID, and text content of the post. There is a single call to the timeline endpoint to check to see if any new tweets of the Twitter ID have been posted to avoid making upwards of 3200 redundant endpoint calls.
  
### 3. Parse and clean tweets to make a sensible and usable Text Corpus 
- lowercase all text
- remove punctiation
- remove non-words (\n, \t, emjoi's...etc)
- tokenization of text

### 4. Plug the newly made Text Corpus into a [Markov Chains](https://en.wikipedia.org/wiki/Markov_chain) algorithm to generate a NLP Model for generating new sentences. 
