import os
import requests
import time
import sys

sys.stdout.reconfigure(line_buffering=True)
print("--- YENİ YÖNTEM İLE BOT BAŞLATILDI ---")

TELEGRAM_BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("CHAT_ID")
TWITTER_USERNAME = "Adememrem1"

def get_latest_tweets_json():
    # Twitter'ın kendi gizli Syndication API'si
    url = f"https://syndication.twitter.com/srv/timeline-profile?screen_name={TWITTER_USERNAME}"
    try:
        response = requests.get(url, timeout=10)
        # Burası bazen HTML döndürür, JSON gelip gelmediğini kontrol edelim
        if response.status_code == 200:
            # Buradan tweet metnini ayıklayacağız
            # Not: Syndication API yapısı biraz karışıktır, 
            # en basit yol ile son tweeti çekelim:
            tweets = response.json().get("timeline", [])
            if tweets:
                return tweets[0].get("text")
        return None
    except Exception as e:
        print(f"SYNDICATION HATASI: {e}")
        return None

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=payload)

last_tweet = ""
while True:
    print("Tweetler kontrol ediliyor...")
    tweet_text = get_latest_tweets_json()
    
    if tweet_text and tweet_text != last_tweet:
        send_to_telegram(tweet_text)
        last_tweet = tweet_text
        print("Yeni tweet yakalandı ve gönderildi!")
    
    time.sleep(300)
    
