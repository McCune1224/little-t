# Overview
This Project aims to fetch any given user's spotify playlists and export the details to JSON format, and then utilize Youtube-DL to fetch mp3/mp4 files of the specified songs within their playlists. 

# How It Works
### 1. Call to [Twitter's Web API](https://developer.twitter.com/en/docs/twitter-api) with a given twitter handle (@username) to collect the following peices of information:
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



  


# Video Visual of the process:
![Little_T_Example](https://user-images.githubusercontent.com/19767251/182556066-8c56d41a-0013-42a6-8de4-c0402db992c4.gif)


# TODO/Future Goals
As of right now, I would really like to have this service being utlized as a twitter bot, which an account has already been made for at https://twitter.com/little_t_bot

There would be two things needed for this however:
1. Some sort of serverless function to handle calling the functions required for the process listed above (AWS Lambda would work)
- This part I have actually already set up a Lambda Function for and worked great..._the issue is with the other requirment_

2. A webhook integration of Twitter's API so that the bot can trigger said serverless function when someone interacts with the bot in some special way (for example a direct message to the bot along the lines of "Copy @username" or by directly tweeting "@little_t_bot Copy @username")

**The problem with setting up a webhook is that you need access to Twitter's Account Activity API...which is for enterprises only... so for right now this project is on hold, but possibly down the line if this APi is made public or doesn't require enterprise level access to obtain, I can return to this project. For right now we are at a roadblock however.**
