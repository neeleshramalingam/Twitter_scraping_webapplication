import snscrape.modules.twitter as sntwitter #importing sncrape module
import requests #importing requests to retrive data from url
import streamlit as st #importing webframework
from streamlit_lottie import st_lottie #importing lottie for lottie animation
import pymongo #importing pymango to connect mangodb database
import pandas as pd #importing pandas for data manipulation
#This function loads a lottie animation from a url and returns it in JSON format
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

#This code uses the "load_lottierul" function to load a lottie animation from a URL and saves it in a variable
lottie_coding = load_lottieurl("https://assets2.lottiefiles.com/private_files/lf30_bz1uh69q.json")

#This code sets the configuration for the web page, including the title, icon, layout, and initial state of the sidebar.
st.set_page_config(page_title="My Twitter Scraping App", page_icon="🦾", layout="wide", initial_sidebar_state="collapsed")


# Display Lottie widget on the left side
st_lottie(lottie_coding, speed=1, width=200, height=200, key="animation")


def mongo(df):
    client = pymongo.MongoClient("mongodb://localhost:27017/") #create connection to MongoDB client on localhost
    mydb = client["twitter"] #create a data base named "twitter" within the MongoDB clent
    mycoll = mydb[f"{search}_tweet"] #create a collection within the "twitter" database that named after the varaiable called 'search' and ends with "_tweet"
    df.reset_index(inplace=True) #Reset the index of the DataFrame in place, meaning it modifies the dataframe directly
    data_dict = df.to_dict("records") #converst the data frame to a dictionary where each row is a dictionary in the format of key-values pairs
    mycoll.insert_one({"index": f"{search}", "data": data_dict})
    st.success("Uploaded Successfully!", icon='✅')
    st.balloons()
    collections = mydb.list_collection_names()
    st.write("List of collection that already exists : ")
    # for i in collections:
    st.write(collections)

st.title("Twitter data Data Scraping Web Application")
st.subheader("This application help as to scrape the twitter data by entering the username and limiting the no of tweets and sepcifying the range of tweets")
tweets_list1 = []
with st.form("my_form"):
    default_since = '2020-06-01'
    default_until = '2020-07-31'
    search = st.text_input("Enter Text that you want to search : ")
    since = st.text_input('Enter the start_date :', default_since)
    until = st.text_input('Enter the start_date :', default_until)
    maxTweets = st.slider('Enter the count :', 0, 1000, 100)
    maxTweets = int(maxTweets)
    summit = st.form_submit_button('Submit')
    if summit:
        passing = (f'{search} since:{since} until:{until}')
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(passing).get_items()):
            if i > maxTweets:
                break
            tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.url, tweet.replyCount,
                                 tweet.retweetCount, tweet.lang, tweet.likeCount])

tweets_df1 = pd.DataFrame(tweets_list1, columns=['DateTime', 'Tweet_ID', 'Content', 'User_Name', 'URL', 'Reply_count',
                                                 'Re_Tweet_Count', 'Language', 'Like_Count'])
st.write(tweets_df1)

with st.form("form"):
    st.write("Press Enter to upload dataset into DB : ")
    enter = st.form_submit_button("Enter")
    if enter:
        mongo(tweets_df1)


def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')


csv = convert_df(tweets_df1)

st.download_button(
    "Press to Download the Dataframe to CSV file format",
    csv,
    f"{search}_tweet.csv",
    "text/csv",
    key='download-csv'
)


def convert_json(df):
    return df.to_json().encode('utf-8')


json = convert_json(tweets_df1)
st.download_button(
    "Press to Download the Dataframe to JSON file format",
    json,
    f"{search}_tweet.json",
    "text/json",
    key='download-json'
)




