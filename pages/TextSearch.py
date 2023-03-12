import streamlit as st
import datetime
import tensorflow as tf
import pickle
import plotly.express as px
import matplotlib.pyplot as plt
from keras.models import load_model
import re    # RegEx for removing non-letter characters
import nltk  #natural language processing
#nltk.download("stopwords")
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
import snscrape.modules.twitter as sntwitter
import pandas as pd
from keras_preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center; color:rgb(0,200,234);background-color:black'>MoodAmigo 😃😡😐😔</h1>", unsafe_allow_html=True)

query = st.text_input(
        "Enter some keywords or #hashtags 👇"
    )

tweet_count = st.slider('How many tweets do you want to fetch?', 0, 100)

date_since = st.date_input(
    "Fetch tweets from ",
    datetime.date(2019, 7, 6)     ##default date for the input field.
)

date_till = st.date_input(
    "Fetch tweets till ",
    datetime.date(2022, 7, 6)     ##default date for the input field.
)

#loading
with open('models/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
# Load model
model = tf.keras.models.load_model('models/best_model.h5')

max_words = 5000
max_len=50

def predict_class(text):
    '''Function to predict sentiment class of the passed text'''
    
    sentiment_classes = ['Negative', 'Neutral', 'Positive']
    max_len=50
    
    xt = tokenizer.texts_to_sequences(text)
    xt = pad_sequences(xt, padding='post', maxlen=max_len)
    yt = model.predict(xt).argmax(axis=1)
    #print('The predicted sentiment is', sentiment_classes[yt[0]])
    return sentiment_classes[yt[0]]

# Setting variables to be used below

# create an empty list to store the tweet data
tweets_data = []
tweets_df = pd.DataFrame()
if st.button('Submit'):
    # Using TwitterSearchScraper to scrape data and append tweets to list
    query = query
    tweet_count=tweet_count
    date_since = date_since
    date_till = date_till
    # loop through the tweets
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{query} since:{date_since} until:{date_till}').get_items()):
        if i > tweet_count:
            break
        # predict sentiment for the tweet
        sentiment = predict_class([tweet.content])
        # create a dictionary with tweet content and sentiment
        tweet_data = {
            'date/time':tweet.date,
            'text': tweet.content,
            'sentiment': sentiment
        }
        # append the tweet data to the list
        tweets_data.append(tweet_data)
        # print the tweet content and sentiment
        #print(tweet.content)
        #print("")

    # create a DataFrame from the tweets data
    tweets_df = pd.DataFrame(tweets_data)
    tweets_df['date/time'] = pd.to_datetime(tweets_df['date/time'])
    tweets_df['Date'] = tweets_df['date/time'].dt.date
    tweets_df['Time'] = tweets_df['date/time'].dt.time
    tweets_df['len'] = tweets_df['text'].str.split().str.len()
    
    tweets_df.to_csv('data.csv',index=False)

    combined_tweets = " ".join([tweet for tweet in tweets_df.text])
                          
    # Initialize wordcloud object
    # Initialize wordcloud object
    wc = WordCloud(background_color='black', 
                    max_words=50, 
                    stopwords=STOPWORDS)
    # Generate the wordcloud from the combined tweets
    wc.generate(combined_tweets)

    st.image(wc.to_image(), caption='Wordcloud', use_column_width=True)
    
    col1,col2 = st.columns(2)
    
    with col1:
        val = tweets_df['sentiment'].value_counts().values.tolist()
        names = tweets_df['sentiment'].value_counts().index.tolist()
        fig = px.pie(values=val, names=names)
        fig.update_layout(width=350,height=400)
        st.plotly_chart(fig,width=350,height=400)
    
    with col2:
        fig = px.box(tweets_df, y = "len", x="sentiment")
        fig.update_layout(width=400,height=400)
        st.plotly_chart(fig,width=400,height=400)

    fig = px.histogram(tweets_df, x='len', color='sentiment')
    st.plotly_chart(fig)

    col1, col2, col3=  st.columns(3)
    
    with col1:
       fig = px.histogram(tweets_df, x="sentiment")
       fig.update_layout(width=300,height=300)

       st.plotly_chart(fig,use_container_width=True,width=300,height=300)

    with col2:
       fig = px.histogram(tweets_df, x="sentiment")
       fig.update_layout(width=300,height=300)

       st.plotly_chart(fig,use_container_width=True,width=300,height=300)
    
    with col3:
       fig = px.histogram(tweets_df, x="sentiment")
       fig.update_layout(width=300,height=300)

       st.plotly_chart(fig,use_container_width=True,width=300,height=300)
    