import os
import requests
import sys
from flask import Flask
from threading import Thread

# Logları anlık akıt
sys.stdout.reconfigure(line_buffering=True)

# Basit Web Sunucusu
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

def test_twitter_access():
    username = "Adememrem1"
    url = f"https://nitter.poast.org/{username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"--- BAĞLANTI TESTİ ---")
        print(f"Status Code: {response.status_code}")
        # Sayfanın ilk 500 karakterini loglarda görelim
        print(f"Sayfa Başlangıcı: {response.text[:500]}")
    except Exception as e:
        print(f"HATA: {e}")

# Botu başlat ve testi çalıştır
if __name__ == "__main__":
    print("Test başlıyor...")
    test_twitter_access()
    # Testten sonra döngüye girmesin, sadece logu görelim yeterli
