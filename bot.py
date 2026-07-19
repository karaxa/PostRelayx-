import feedparser
import time
import os
import requests
import threading
import gc
from flask import Flask
from supabase import create_client

app = Flask(__name__)

# Çevre Değişkenleri
TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
RSS_URL = "https://rss.app/feeds/FkVRd8Xn6Om0GDtK.xml"
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

@app.route('/')
def home():
    return "Bot Supabase ile aktif.", 200

@app.route('/health')
def health():
    return "OK", 200

def check_rss():
    try:
        feed = feedparser.parse(RSS_URL)
        if feed.entries:
            entry = feed.entries[0]
            tweet_id = entry.link.split('/')[-1]
            
            # Veritabanında var mı?
            response = supabase.table("tweet_history").select("tweet_id").eq("tweet_id", tweet_id).execute()
            
            if not response.data:
                msg = f"📢 **Yeni Tweet**\n\n{entry.link}"
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                                    data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
                
                if res.status_code == 200:
                    supabase.table("tweet_history").insert({"tweet_id": tweet_id}).execute()
                    print(f"Başarıyla gönderildi: {tweet_id}")
        
        # Bellek temizliği (RAM limitini aşmamak için)
        gc.collect()
        
    except Exception as e:
        print(f"Hata oluştu: {e}")

def worker():
    while True:
        check_rss()
        # 5 dakikalık bekleme süresi, sunucu yorgunluğunu azaltır
        time.sleep(300)

if __name__ == "__main__":
    threading.Thread(target=worker, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
    
