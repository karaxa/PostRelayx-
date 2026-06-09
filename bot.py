import os
import requests
import time
import sys

# Logların anlık akması için gerekli ayar
sys.stdout.reconfigure(line_buffering=True)
print("--- BOT BAŞLATILDI ---")

# Render Environment Variables üzerinden bilgileri çekiyoruz
USER_ID = os.environ.get("USER_ID")
X_BEARER_TOKEN = os.environ.get("X_BEARER_TOKEN")
TELEGRAM_BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("CHAT_ID")

def get_latest_tweets():
    url = f"https://api.twitter.com/2/users/{USER_ID}/tweets"
    headers = {"Authorization": f"Bearer {X_BEARER_TOKEN}"}
    params = {"max_results": 5}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception as e:
        print(f"TWITTER HATASI: {e}")
        return []

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print("Telegram'a mesaj gönderildi.")
    except Exception as e:
        print(f"TELEGRAM HATASI: {e}")

# --- ANA DÖNGÜ ---
print("Döngü başladı, tweetler kontrol ediliyor...")
while True:
    tweets = get_latest_tweets()
    
    if tweets:
        for tweet in tweets:
            send_to_telegram(tweet['text'])
    else:
        print("Yeni tweet bulunamadı veya bir hata oluştu.")
        
    time.sleep(300) # 5 dakika bekle
