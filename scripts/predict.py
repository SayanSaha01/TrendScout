import tensorflow as tf
import pickle
from keras.models import load_model
import re    # RegEx for removing non-letter characters
import nltk  #natural language processing
nltk.download("stopwords")
from nltk.corpus import stopwords

#loading
with open('models/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
# Load model
model = tf.keras.models.load_model('models/best_model.h5')

from keras_preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences

max_words = 5000
max_len=50

def predict_class(text):
    '''Function to predict sentiment class of the passed text'''
    
    sentiment_classes = ['Negative', 'Neutral', 'Positive']
    max_len=50
    
    xt = tokenizer.texts_to_sequences(text)
    xt = pad_sequences(xt, padding='post', maxlen=max_len)
    yt = model.predict(xt).argmax(axis=1)
    print('The predicted sentiment is', sentiment_classes[yt[0]])

import snscrape.modules.twitter as sntwitter
import pandas as pd

# Query by text search
# Setting variables to be used below
tweet_count = 10

# Creating list to append tweet data to
tweets_list2 = []

# Using TwitterSearchScraper to scrape data and append tweets to list
query = input('Enter the query : ')
date_since = input("Enter a starting date (format: YYYY-MM-DD): ")
date_till = input("Enter a ending date (format: YYYY-MM-DD): ")
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{query} since:{date_since} until:{date_till}').get_items()):
    if i>tweet_count:
        break
    #tweets_list2.append([tweet.content])
    #for tweet in tweets:
    print(tweet.content)
    predict_class([tweet.content]) #predicting sentiment
    print("")