import snscrape.modules.twitter as sntwitter
import streamlit as st
import streamlit.components.v1 as components
import requests
from email.message import EmailMessage
from streamlit_lottie import st_lottie

st.set_page_config(layout="wide")

col1, col2 = st.columns(2)
with col1:
    st.subheader("How engaging are your posts?")
    st.markdown("You can monitor the performance of your posts over time by analyzing their engagements, impressions, and the percentage of engagement per impression.")
    st.markdown("By clicking on any data point, you will be redirected to the link of the corresponding post.")
with col2:
    def load_lottieurl(url:str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    lottie_animation = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_cdu97cbh.json")
    st_lottie(lottie_animation, key="animation", height=200, width=200)
    
# Get the Twitter username input from the user
username = st.text_input("Enter the Twitter username: ")

user_data = {}
for tweet in sntwitter.TwitterSearchScraper(f'from:{username}').get_items():
    if tweet.user.username == username:
        user_data['followers'] = tweet.user.followersCount
        user_data['friends'] = tweet.user.friendsCount
        user_data['total_tweets'] = tweet.user.statusesCount
        user_data['total_likes'] = tweet.user.favouritesCount

# Print the user's Twitter data
col1,col2,col3,col4,col5,col6 = st.columns(6)
with col1:
    st.info("Followers: ")
    st.info(f"{user_data['followers']}")
with col2:
    st.info("Following: ") 
    st.info(f"{user_data['friends']}")
with col3:
    st.info("Total Tweets: ")
    st.info(f"{user_data['total_tweets']}")
with col4:  
    st.info("Total Likes: ")
    st.info(f"{user_data['total_likes']}")


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
top_replied_tweet = max(replied_tweets, key=lambda x: x['replies'])
if quoted_tweets:
    top_quoted_tweet = max(quoted_tweets, key=lambda x: x['replies'])
else:
    top_quoted_tweet = None

most_liked_tweet = max(liked_tweets, key=lambda x: x['likes'])
if retweeted_tweets:
    most_retweeted_tweet = max(retweeted_tweets, key=lambda x: x['retweets'])
else:
    most_retweeted_tweet = None


def theTweet(tweet_url):
    api = "https://publish.twitter.com/oembed?url={}".format(tweet_url)
    response = requests.get(api)
    res = response.json()["html"]
    return res

top_replied = top_replied_tweet['url']
most_liked = most_liked_tweet['url']

st.text("")

col1,col2 = st.columns(2)
with col1:
    if top_replied:
        st.write("Top Replied Tweet")
        reply = theTweet(top_replied)
        components.html(reply,height= 700)
    else:
        st.write("User doesn't have any replied tweets.")
with col2:  
    if most_liked:
        st.write("Most Liked Tweet")
        like = theTweet(most_liked)
        components.html(like,height= 700)
    else:
        st.write("No liked tweets found for this user")

col3,col4 = st.columns(2)
with col3:
    if top_quoted_tweet:
        st.write("Top Quoted Tweet")
        quote = theTweet(top_quoted_tweet['url'])
        components.html(quote,height= 700)
    else:
        st.write("User doesn't have any quoted tweets.")
with col4:  
    if most_retweeted_tweet:
        st.write("Most Retweeted Tweet")
        retweet = theTweet(most_retweeted_tweet['url'])
        components.html(retweet,height= 700)
    else:
        st.write("No retweeted tweets found for this user")