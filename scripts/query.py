# Imports
import snscrape.modules.twitter as sntwitter
import pandas as pd

# Query by text search
# Setting variables to be used below
maxTweets = 500

# Creating list to append tweet data to
tweets_list2 = []

# Using TwitterSearchScraper to scrape data and append tweets to list
query = input('Enter the query : ')
since = input("Enter a starting date (format: YYYY-MM-DD): ")
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{query} since:2020-06-01 until:2020-07-31').get_items()):
    if i>maxTweets:
        break
    tweets_list2.append([tweet.date, tweet.id, tweet.content, tweet.user.username])
print("Tweets of query successfully fetched !!")

# Creating a dataframe from the tweets list above
tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

# Display first 5 entries from dataframe
tweets_df2.head()

# Export dataframe into a CSV
tweets_df2.to_csv('text-query-tweets.csv', sep=',', index=False)