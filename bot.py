def check_rss():
    global sent_links
    try:
        # RSS beslemesini çek
        feed = feedparser.parse(https://rss.app/feeds/ufSAESC67kjoyb0A.xml)
        
        # En son tweeti al
        if feed.entries:
            entry = feed.entries[0]
            
            # Linkin sonundaki ID'yi al (Örn: .../status/123456789 -> 123456789)
            tweet_id = entry.link.split('/')[-1]
            
            # Eğer bu ID daha önce gönderilenler listesinde yoksa gönder
            if tweet_id not in sent_links:
                # Mesajı hazırla
                msg = f"📢 **Yeni Tweet Geldi!**\n\n{entry.link}"
                
                # Telegram'a gönder
                res = requests.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                    data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
                )
                
                # Gönderim başarılıysa listeye ekle
                if res.status_code == 200:
                    sent_links.append(tweet_id)
                    # Sadece son 10'u tut
                    if len(sent_links) > 10:
                        sent_links.pop(0)
                    print(f"Gönderildi: {tweet_id}")
                else:
                    print(f"Telegram hatası: {res.text}")
            else:
                # Zaten gönderildi ise buraya düşer
                print(f"Zaten gönderilmiş, atlandı: {tweet_id}")
        else:
            print("RSS boş görünüyor.")
            
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        
