#!/usr/bin/env python3
"""
Otomatik Twitter Bot - Transfer Haberleri
Fabrizio Romano ve David Ornstein tweetlerini izler, sadeleştirir ve yeni görsellerle paylaşır
Logo ekleme özelliği dahil
"""

import os
import time
import json
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import tweepy
from anthropic import Anthropic
import requests
from io import BytesIO
from PIL import Image, ImageDraw
import base64
from pathlib import Path

# Konfigürasyon
CONFIG = {
    "tracked_accounts": ["FabrizioRomano", "David_Ornstein"],
    "check_interval_minutes": 30,
    "tweet_history_file": "tweet_history.json",
    "max_tweet_length": 280,
    "logo_path": "omt_logo.png",  # Logo dosyası
    "logo_size_ratio": 0.15,  # Görselin %15'i kadar logo boyutu
}

class TwitterBot:
    def __init__(self):
        # Twitter API v2 credentials
        self.twitter_client = tweepy.Client(
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        )
        
        # Twitter API v1.1 for media upload
        auth = tweepy.OAuth1UserHandler(
            os.getenv("TWITTER_API_KEY"),
            os.getenv("TWITTER_API_SECRET"),
            os.getenv("TWITTER_ACCESS_TOKEN"),
            os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        )
        self.api_v1 = tweepy.API(auth)
        
        # Anthropic API for text simplification
        self.anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # Logo yükle
        self.logo = None
        if os.path.exists(CONFIG["logo_path"]):
            self.logo = Image.open(CONFIG["logo_path"]).convert("RGBA")
            print(f"✅ Logo yüklendi: {CONFIG['logo_path']}")
        else:
            print(f"⚠️ Logo bulunamadı: {CONFIG['logo_path']}")
        
        # Tweet history tracking
        self.history = self.load_history()
    
    def load_history(self) -> Dict:
        """Daha önce işlenmiş tweetleri yükle"""
        try:
            with open(CONFIG["tweet_history_file"], "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"processed_tweets": []}
    
    def save_history(self):
        """Tweet geçmişini kaydet"""
        with open(CONFIG["tweet_history_file"], "w") as f:
            json.dump(self.history, f, indent=2)
    
    def get_user_id(self, username: str) -> Optional[str]:
        """Kullanıcı adından user ID al"""
        try:
            user = self.twitter_client.get_user(username=username)
            return user.data.id
        except Exception as e:
            print(f"❌ Kullanıcı bulunamadı {username}: {e}")
            return None
    
    def fetch_recent_tweets(self, username: str, since_minutes: int = 30) -> List[Dict]:
        """Son X dakikadaki tweetleri çek"""
        user_id = self.get_user_id(username)
        if not user_id:
            return []
        
        try:
            # Son X dakikadaki tweetleri al
            start_time = datetime.utcnow() - timedelta(minutes=since_minutes)
            
            tweets = self.twitter_client.get_users_tweets(
                id=user_id,
                max_results=10,
                tweet_fields=["created_at", "attachments", "entities"],
                expansions=["attachments.media_keys"],
                media_fields=["url", "preview_image_url", "type"],
                start_time=start_time.isoformat() + "Z"
            )
            
            if not tweets.data:
                return []
            
            result = []
            media_dict = {}
            
            # Media bilgilerini dictionary'e çevir
            if tweets.includes and "media" in tweets.includes:
                for media in tweets.includes["media"]:
                    media_dict[media.media_key] = media
            
            for tweet in tweets.data:
                # Daha önce işlenmiş mi kontrol et
                if str(tweet.id) in self.history["processed_tweets"]:
                    continue
                
                tweet_data = {
                    "id": str(tweet.id),
                    "text": tweet.text,
                    "created_at": str(tweet.created_at),
                    "username": username,
                    "media": []
                }
                
                # Medya varsa ekle
                if hasattr(tweet, 'attachments') and tweet.attachments and "media_keys" in tweet.attachments:
                    for media_key in tweet.attachments["media_keys"]:
                        if media_key in media_dict:
                            media = media_dict[media_key]
                            if media.type == "photo":
                                tweet_data["media"].append({
                                    "type": "photo",
                                    "url": media.url
                                })
                
                result.append(tweet_data)
            
            return result
            
        except Exception as e:
            print(f"❌ Tweet çekme hatası {username}: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def simplify_tweet_text(self, original_text: str, username: str) -> str:
        """Tweet metnini Claude ile sadeleştir"""
        try:
            prompt = f"""Aşağıdaki {username} tweetini Türkçe olarak sadeleştir. 

Orijinal tweet: {original_text}

Kurallar:
- Aynı bilgiyi ver ama daha sade Türkçe ile
- Emoji varsa koru veya uygun emoji ekle
- Maksimum 280 karakter
- "Here we go!" gibi ikonik ifadeleri Türkçe eşdeğerleriyle değiştir
- Transfer haberi tonunu koru
- Sadece sadeleştirilmiş tweeti döndür, başka açıklama yapma"""

            message = self.anthropic.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            simplified = message.content[0].text.strip()
            
            # Maksimum uzunluk kontrolü
            if len(simplified) > CONFIG["max_tweet_length"]:
                simplified = simplified[:CONFIG["max_tweet_length"]-3] + "..."
            
            return simplified
            
        except Exception as e:
            print(f"❌ Metin sadeleştirme hatası: {e}")
            # Hata durumunda orijinal metni kısalt
            return original_text[:280]
    
    def add_logo_to_image(self, image_bytes: bytes) -> bytes:
        """Görselin sağ üst köşesine logo ekle"""
        try:
            # Görseli aç
            image = Image.open(BytesIO(image_bytes)).convert("RGBA")
            img_width, img_height = image.size
            
            if self.logo is None:
                print("⚠️ Logo yok, görsele logo eklenemedi")
                return image_bytes
            
            # Logo boyutunu hesapla (görselin %15'i)
            logo_height = int(img_height * CONFIG["logo_size_ratio"])
            aspect_ratio = self.logo.width / self.logo.height
            logo_width = int(logo_height * aspect_ratio)
            
            # Logoyu yeniden boyutlandır
            logo_resized = self.logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
            
            # Sağ üst köşe pozisyonu (10px padding)
            padding = 10
            position = (img_width - logo_width - padding, padding)
            
            # Logo'yu yapıştır (alpha channel korunarak)
            image.paste(logo_resized, position, logo_resized)
            
            # RGB'ye çevir ve kaydet
            image = image.convert("RGB")
            output = BytesIO()
            image.save(output, format="JPEG", quality=95)
            
            print("✅ Logo eklendi")
            return output.getvalue()
            
        except Exception as e:
            print(f"❌ Logo ekleme hatası: {e}")
            import traceback
            traceback.print_exc()
            # Hata durumunda orijinal görseli döndür
            return image_bytes
    
    def download_and_process_image(self, image_url: str) -> Optional[bytes]:
        """Görseli indir ve logo ekle"""
        try:
            response = requests.get(image_url, timeout=10)
            if response.status_code == 200:
                # Logo ekle
                processed_image = self.add_logo_to_image(response.content)
                return processed_image
            else:
                print(f"❌ Görsel indirilemedi: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Görsel işleme hatası: {e}")
            return None
    
    def post_tweet(self, text: str, media_ids: List[str] = None) -> bool:
        """Yeni tweet paylaş"""
        try:
            if media_ids:
                self.twitter_client.create_tweet(text=text, media_ids=media_ids)
            else:
                self.twitter_client.create_tweet(text=text)
            
            print(f"✅ Tweet paylaşıldı: {text[:50]}...")
            return True
            
        except Exception as e:
            print(f"❌ Tweet paylaşma hatası: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def upload_media(self, image_bytes: bytes) -> Optional[str]:
        """Görseli Twitter'a yükle"""
        try:
            media = self.api_v1.media_upload(filename="image.jpg", file=BytesIO(image_bytes))
            return media.media_id_string
        except Exception as e:
            print(f"❌ Medya yükleme hatası: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def process_tweet(self, tweet_data: Dict):
        """Bir tweeti işle ve paylaş"""
        print(f"\n📝 İşleniyor: @{tweet_data['username']} - {tweet_data['text'][:50]}...")
        
        # Metni sadeleştir
        simplified_text = self.simplify_tweet_text(tweet_data['text'], tweet_data['username'])
        print(f"✨ Sadeleştirilmiş: {simplified_text[:70]}...")
        
        media_ids = []
        
        # Görselleri işle
        if tweet_data['media']:
            for media in tweet_data['media']:
                if media['type'] == 'photo':
                    # Görseli indir ve logo ekle
                    processed_image = self.download_and_process_image(media['url'])
                    
                    if processed_image:
                        media_id = self.upload_media(processed_image)
                        if media_id:
                            media_ids.append(media_id)
                            print(f"✅ Görsel yüklendi (logo ile)")
                    else:
                        print("⚠️ Görsel işlenemedi")
        
        # Tweeti paylaş
        if self.post_tweet(simplified_text, media_ids if media_ids else None):
            # İşlenmiş tweet olarak kaydet
            self.history["processed_tweets"].append(tweet_data['id'])
            self.save_history()
            print(f"✅ Tweet işlendi ve paylaşıldı!")
        else:
            print(f"❌ Tweet paylaşılamadı!")
    
    async def run(self):
        """Ana döngü - sürekli çalış"""
        print("🤖 Twitter Bot başlatıldı!")
        print(f"👀 Takip edilen hesaplar: {', '.join(CONFIG['tracked_accounts'])}")
        print(f"⏰ Kontrol aralığı: {CONFIG['check_interval_minutes']} dakika")
        print(f"🎨 Logo: {'✅ Aktif' if self.logo else '❌ Yok'}\n")
        
        while True:
            try:
                print(f"\n🔍 Kontrol ediliyor... [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
                
                for username in CONFIG["tracked_accounts"]:
                    tweets = self.fetch_recent_tweets(username, CONFIG["check_interval_minutes"])
                    
                    print(f"  @{username}: {len(tweets)} yeni tweet bulundu")
                    
                    for tweet in tweets:
                        await self.process_tweet(tweet)
                        # Rate limit için bekleme
                        await asyncio.sleep(10)
                
                print(f"\n💤 {CONFIG['check_interval_minutes']} dakika bekleniyor...")
                await asyncio.sleep(CONFIG["check_interval_minutes"] * 60)
                
            except KeyboardInterrupt:
                print("\n👋 Bot durduruldu!")
                break
            except Exception as e:
                print(f"❌ Hata oluştu: {e}")
                import traceback
                traceback.print_exc()
                print("⏳ 60 saniye sonra tekrar denenecek...")
                await asyncio.sleep(60)

if __name__ == "__main__":
    # Environment variables kontrolü
    required_vars = [
        "TWITTER_BEARER_TOKEN",
        "TWITTER_API_KEY",
        "TWITTER_API_SECRET",
        "TWITTER_ACCESS_TOKEN",
        "TWITTER_ACCESS_TOKEN_SECRET",
        "ANTHROPIC_API_KEY"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Eksik environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n.env dosyasını kontrol edin!")
        exit(1)
    
    bot = TwitterBot()
    asyncio.run(bot.run())

import threading
import health

threading.Thread(target=health.run, daemon=True).start()
