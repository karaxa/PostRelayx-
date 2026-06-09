import os
import requests
import time
import sys
from flask import Flask
from threading import Thread
from bs4 import BeautifulSoup

# Render için Web Sunucusu
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot aktif."

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

t = Thread(target=run_web)
t.daemon = True
t.start()

# Bot Ayarları
sys.stdout.reconfigure(line_buffering=True)
TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
TWITTER_USERNAME = "Adememrem1"

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Telegram Hatası: {e}")

def get_latest_tweets():
    # Nitter üzerinden veriyi çekiyoruz
    url = f"https://nitter.net/{TWITTER_USERNAME}"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Nitter'daki tweet kartlarını bul
            tweet = soup.find('div', class_='tweet-content')
            if tweet:
                return tweet.get_text()
        else:
            print(f"DEBUG: Nitter bağlantı hatası: {response.status_code}")
        return None
    except Exception as e:
        print(f"HATA: {e}")
        return None

# Ana Döngü
last_tweet = ""
while True:
    print("Tweetler Nitter üzerinden kontrol ediliyor...")
    tweet_text = get_latest_tweets()
    
    if tweet_text and tweet_text != last_tweet:
        send_to_telegram(tweet_text)
        last_tweet = tweet_text
        print("Yeni tweet gönderildi!")
    
    time.sleep(300)
