# Imports
import snscrape.modules.twitter as sntwitter
import pandas as pd

# Query by username
# Setting variables to be used below
maxTweets = 100

# Creating list to append tweet data to
tweets_list1 = []

# Using TwitterSearchScraper to scrape data 
user_id = input('Enter the user id : ')
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{user_id}').get_items()):
    if i>maxTweets:
        break
    tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username])
print("Tweets of user successfully fetched !! ")


# Creating a dataframe from the tweets list above

tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
tweets_df1.to_csv('user-tweets.csv', sep=',', index=False)
