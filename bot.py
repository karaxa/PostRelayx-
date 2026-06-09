import os
from flask import Flask
from threading import Thread

# Render'ın beklediği portu aç
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot aktif!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# Sunucuyu ayrı bir kanalda (thread) başlat
t = Thread(target=run)
t.start()

# --- BURADAN SONRA SENİN KENDİ BOT KODLARIN BAŞLASIN ---
import requests
import time

# --- AYARLAR ---
# Buraya TweeterID.com sitesinden aldığın sayısal ID'yi yaz (Tırnakları silme!)
USER_ID = "1406148344897052674" 
X_BEARER_TOKEN = "BURAYA_RENDERDAKI_TOKENI_YAZ" # Render'daki ile aynı olmalı
TELEGRAM_BOT_TOKEN = "BURAYA_BOT_TOKENINI_YAZ"
TELEGRAM_CHAT_ID = "-100..." # Başına - işaretini koymayı unutma

def get_latest_tweets():
    # Artık kullanıcı adını sorgulamıyoruz, doğrudan ID ile tweetleri çekiyoruz
    url = f"https://api.twitter.com/2/users/{USER_ID}/tweets"
    headers = {"Authorization": f"Bearer {X_BEARER_TOKEN}"}
    
    # 402 hatasını aşmak için parametre ekliyoruz
    params = {"max_results": 5}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Hata! Durum Kodu: {response.status_code}")
        print(f"Mesaj: {response.text}")
        return []

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=payload)

# --- ANA DÖNGÜ ---
while True:
    print("Tweetler kontrol ediliyor...")
    tweets = get_latest_tweets()
    
    for tweet in tweets:
        send_to_telegram(tweet['text'])
        
    time.sleep(300) # 5 dakika bekle
