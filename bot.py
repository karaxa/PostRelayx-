import os
import time
import requests

# Ortam değişkenlerinden bilgileri alıyoruz
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")

USERNAME = "Adememrem1"   # İzlemek istediğin kullanıcı adı
SEEN_FILE = "seen.txt"

def get_user_id(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {X_BEARER_TOKEN}"}
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    return r.json()["data"]["id"]

def get_latest_tweets(user_id, since_id=None):
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    params = {
        "max_results": 5,
        "tweet.fields": "created_at",
        "exclude": "retweets,replies",
    }
    if since_id:
        params["since_id"] = since_id

    headers = {"Authorization": f"Bearer {X_BEARER_TOKEN}"}
    r = requests.get(url, headers=headers, params=params, timeout=20)
    r.raise_for_status()
    return r.json().get("data", [])

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=payload, timeout=20)

def load_last_id():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            return f.read().strip() or None
    return None

def save_last_id(tweet_id):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        f.write(tweet_id)

def main():
    print("Bot başlatılıyor...")
    user_id = get_user_id(USERNAME)
    last_id = load_last_id()

    while True:
        try:
            tweets = get_latest_tweets(user_id, since_id=last_id)
            if tweets:
                tweets = list(reversed(tweets))
                for t in tweets:
                    link = f"https://x.com/{USERNAME}/status/{t['id']}"
                    message = f"Yeni tweet:\n{t['text']}\n\n{link}"
                    send_to_telegram(message)
                    last_id = t["id"]
                    save_last_id(last_id)
        except Exception as e:
            print(f"Hata oluştu: {e}")
        
        time.sleep(300) # 5 dakikada bir kontrol eder

if __name__ == "__main__":
    main()

