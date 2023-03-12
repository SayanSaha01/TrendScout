import snscrape.modules.twitter as sntwitter

# Get the Twitter username input from the user
username = input("Enter the Twitter username: ")

# Fetch the top replied and quoted tweets of all time for the user
replied_tweets = []
quoted_tweets = []
for tweet in sntwitter.TwitterSearchScraper(f"to:{username}").get_items():
    if not tweet.inReplyToTweetId is None:
        replied_tweets.append({
            "text": tweet.content,
            "replies": tweet.replyCount,
            "likes": tweet.likeCount,
            "retweets": tweet.retweetCount,
            "url": f"https://twitter.com/{tweet.user.username}/status/{tweet.id}"
        })
    if not tweet.quotedTweet is None:
        quoted_tweets.append({
            "text": tweet.content,
            "replies": tweet.replyCount,
            "likes": tweet.likeCount,
            "retweets": tweet.retweetCount,
            "quoted_tweet": {
                "text": tweet.quotedTweet.content,
                "url": f"https://twitter.com/{tweet.quotedTweet.user.username}/status/{tweet.quotedTweet.id}"
            },
            "url": f"https://twitter.com/{tweet.user.username}/status/{tweet.id}"
        })

# Fetch the top liked and retweeted tweets of all time for the user
liked_tweets = []
retweeted_tweets = []
for tweet in sntwitter.TwitterSearchScraper(f"from:{username}").get_items():
    if tweet.likeCount > 0:
        liked_tweets.append({
            "text": tweet.content,
            "replies": tweet.replyCount,
            "likes": tweet.likeCount,
            "retweets": tweet.retweetCount,
            "url": f"https://twitter.com/{tweet.user.username}/status/{tweet.id}"
        })
    if tweet.retweetCount > 0:
        retweeted_tweets.append({
            "text": tweet.content,
            "replies": tweet.replyCount,
            "likes": tweet.likeCount,
            "retweets": tweet.retweetCount,
            "url": f"https://twitter.com/{tweet.user.username}/status/{tweet.id}"
        })

# Sort the lists by the specified key and get the top 5 tweets for each category
top_replied_tweet = max(replied_tweets, key=lambda x: x['replies']) if replied_tweets else None
top_quoted_tweet = max(quoted_tweets, key=lambda x: x['replies']) if quoted_tweets else None
most_liked_tweet = max(liked_tweets, key=lambda x: x['likes']) if liked_tweets else None
most_retweeted_tweet = max(retweeted_tweets, key=lambda x: x['retweets']) if retweeted_tweets else None

# Print the results
if top_replied_tweet:
    print("Maximum replied tweet:")
    print(top_replied_tweet['text'])
    print("URL:", top_replied_tweet['url'])
    print()
else:
    print("User doesn't have any replied tweets.")
if top_quoted_tweet:
    print("Maximum quoted tweet:")
    print(top_quoted_tweet['text'])
    print("Quoted tweet text:", top_quoted_tweet['quoted_tweet']['text'])
    print("Quoted tweet URL:", top_quoted_tweet['quoted_tweet']['url'])
    print("URL:", top_quoted_tweet['url'])
    print()
else:
    print("User doesn't have any quoted tweets.")
if most_liked_tweet:
    print("Most liked tweet:")
    print(most_liked_tweet['text'])
    print("URL:", most_liked_tweet['url'])
    print()
else:
    print("No liked tweets found for this user")

if most_retweeted_tweet:
    print("Most retweeted tweet:")
    print(most_retweeted_tweet['text'])
    print("URL:", most_retweeted_tweet['url'])
    print()
else:
    print("No retweeted tweets found for this user")