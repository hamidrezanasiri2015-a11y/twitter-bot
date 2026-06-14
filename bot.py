import os
import time
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

TWITTER_USER = "نام_کاربری_توییتر"  # ← اینجا رو عوض کن
LAST_TWEET_FILE = "last_tweet.txt"

def get_latest_tweet():
    try:
        url = f"https://nitter.net/{TWITTER_USER}"
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        tweet = soup.find("div", class_="tweet-content")
        if tweet:
            return tweet.text.strip()
    except:
        return None
    return None

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def get_last_tweet():
    if os.path.exists(LAST_TWEET_FILE):
        with open(LAST_TWEET_FILE, "r") as f:
            return f.read().strip()
    return ""

def save_last_tweet(text):
    with open(LAST_TWEET_FILE, "w") as f:
        f.write(text)

while True:
    tweet = get_latest_tweet()
    if tweet and tweet != get_last_tweet():
        send_message(f"🆕 توییت جدید از @{TWITTER_USER}:\n\n{tweet}")
        save_last_tweet(tweet)
    time.sleep(60)
