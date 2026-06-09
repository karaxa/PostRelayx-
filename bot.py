import feedparser
import time
import os
import requests
from flask import Flask
from threading import Thread

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
app = Flask(__name__)

@app.route('/')
def home(): return "Bot aktif.", 200

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

def run_bot():
    last_link = ""
    print("--- BOT İZLEMEYE BAŞLADI ---")
    
    while True:
        try:
            rss_url = "https://rss.app/feeds/HXScZ2SZ5dwrKNp4.xml"
            feed = feedparser.parse(rss_url)
            
            if feed.entries:
                entry = feed.entries[0]
                current_link = entry.link
                
                print(f"Kontrol edildi. Son link: {current_link}") # Logda görürsün
                
                if current_link != last_link:
                    print("Yeni tweet bulundu! Telegram'a gönderiliyor...")
                    
                    # Telegram isteği
                    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                    data = {"chat_id": CHAT_ID, "text": f"Yeni tweet: {entry.title}\n{current_link}"}
                    response = requests.post(url, data=data)
                    
                    if response.status_code == 200:
                        print("Başarıyla gönderildi.")
                        last_link = current_link
                    else:
                        print(f"Telegram Hatası: {response.text}") # Hata kodunu loga yazar
                else:
                    print("Yeni tweet yok, bekleniyor.")
            else:
                print("RSS boş görünüyor.")
        
        except Exception as e:
            print(f"Genel Hata: {e}")
        
        time.sleep(120) # 2 dakikada bir kontrol

if __name__ == "__main__":
    Thread(target=run_bot, daemon=True).start()
    run_web()
    
