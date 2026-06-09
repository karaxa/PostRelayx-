import os
import requests
import time
import sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(line_buffering=True)
print("--- RSS BOT BAŞLATILDI ---")

# Telegram Bilgileri (Render'dan çekilecek)
TELEGRAM_BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("CHAT_ID")
TWITTER_USERNAME = "Adememrem1" # Takip ettiğin kişi

def get_latest_tweets_rss():
    # Ücretsiz bir RSS dönüştürücü servisi
    rss_url = f"https://rsshub.app/twitter/user/{TWITTER_USERNAME}"
    try:
        response = requests.get(rss_url, timeout=10)
        root = ET.fromstring(response.content)
        items = root.findall('.//item')
        
        # Son tweetin içeriğini al
        if items:
            return items[0].find('title').text
        return None
    except Exception as e:
        print(f"RSS HATASI: {e}")
        return None

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=payload)

# --- ANA DÖNGÜ ---
last_tweet = ""
while True:
    print("Tweetler kontrol ediliyor...")
    tweet_text = get_latest_tweets_rss()
    
    if tweet_text and tweet_text != last_tweet:
        send_to_telegram(tweet_text)
        last_tweet = tweet_text
        print("Yeni tweet bulundu ve gönderildi!")
    
    time.sleep(300) # 5 dakika bekle
