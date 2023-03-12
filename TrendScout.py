import streamlit as st
st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center; color:rgb(0,200,234);background-color:black'>TrendScout : Twitter Data Analytics 🔎 WebApp</h1>", unsafe_allow_html=True)

st.write("""Welcome to trendScout, A tool for insightful visualisations and data analytics for understanding 
         Twitter's impact at a glance to facilitate the following functions""")
st.write('1. Measure brand perception 💻')
st.write('2. Identify trends 📈')
st.write('3. Product/Tweet sentiment 🐦')
st.write('4. Measure brand hashtag performance #️⃣')
st.write('5. Competitor analysis 📊')
         
st.write('This app scrapes (and never keeps or stores) 🙈 the tweets you want to analyze.')

st.write("""To begin with, please select the type of search you want to conduct. 
You can either search a twitter handle (e.g. @elonmusk) which will analyse the recent tweets of that user or search
a trending hashtag (e.g #WomensPremierLeague) to classify sentiments of the tweets regarding it""")