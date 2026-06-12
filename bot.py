import feedparser
import time
import os
import requests
import threading
from flask import Flask
from supabase import create_client

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
RSS_URL = "https://rss.app/feeds/ufSAESC67kjoyb0A.xml"

# Supabase bağlantısını başlat
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

@app.route('/')
def home():
    return "Bot Supabase ile aktif v2.", 200

# Şu satırı ekle (UptimeRobot'un sevdiği bir endpoint)
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
            
            # Eğer boşsa (yani yoksa), gönder ve kaydet
            if not response.data:
                msg = f"📢 **Yeni Tweet**\n\n{entry.link}"
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                                    data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
                
                if res.status_code == 200:
                    supabase.table("tweet_history").insert({"tweet_id": tweet_id}).execute()
                    print(f"Başarıyla gönderildi ve kaydedildi: {tweet_id}")
    except Exception as e:
        print(f"Hata: {e}")

def worker():
    while True:
        check_rss()
        time.sleep(120)

if __name__ == "__main__":
    threading.Thread(target=worker, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

