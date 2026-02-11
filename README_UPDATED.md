# 🤖 Twitter Transfer Haberleri Botu - OMT

Fabrizio Romano ve David Ornstein'ın tweetlerini otomatik olarak sadeleştirip, görsellerine OMT logosu ekleyerek paylaşan bot.

## ✨ YENİ ÖZELLİKLER

- ✅ **Logo Ekleme:** Tüm görsellerin sağ üst köşesine otomatik OMT logosu
- ✅ **Hata Düzeltmeleri:** API çağrıları, görsel işleme ve tweet paylaşımı iyileştirildi
- ✅ **Detaylı Loglar:** Her adımda ne olduğunu görebilirsiniz
- ✅ **24/7 Çalıştırma Rehberi:** Railway, Render, VPS seçenekleri

## 🚀 HIZLI BAŞLANGIÇ

### 1. Dosyaları İndir
```bash
# Tüm dosyalar hazır
ls
# twitter_bot_fixed.py  ← Düzeltilmiş bot
# omt_logo.png          ← Logonuz
# KURULUM_REHBERI.md    ← Detaylı adımlar
# setup.sh / setup.bat  ← Otomatik kurulum
```

### 2. Kurulumu Yap

**Linux/Mac:**
```bash
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

### 3. API Anahtarlarını Al

📖 **Detaylı rehber:** `KURULUM_REHBERI.md` dosyasını oku

**Kısa özet:**
1. **Twitter API:** https://developer.twitter.com/
   - App oluştur
   - "Read and Write" yetkisi ver
   - 5 API anahtarı al

2. **Anthropic API:** https://console.anthropic.com/
   - Hesap aç
   - API Key oluştur

### 4. .env Dosyasını Doldur

```bash
nano .env  # veya notepad .env
```

```env
TWITTER_BEARER_TOKEN=AAAAAxxxxxxxx
TWITTER_API_KEY=xxxxxxxx
TWITTER_API_SECRET=xxxxxxxx
TWITTER_ACCESS_TOKEN=xxxxxxxx
TWITTER_ACCESS_TOKEN_SECRET=xxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxx
```

### 5. Botu Çalıştır

```bash
python3 twitter_bot_fixed.py
```

**Göreceksin:**
```
🤖 Twitter Bot başlatıldı!
👀 Takip edilen hesaplar: FabrizioRomano, David_Ornstein
⏰ Kontrol aralığı: 30 dakika
🎨 Logo: ✅ Aktif

🔍 Kontrol ediliyor... [2026-02-11 20:30:00]
  @FabrizioRomano: 2 yeni tweet bulundu
📝 İşleniyor: @FabrizioRomano - 🚨🔴 EXCLUSIVE...
✨ Sadeleştirilmiş: 🔴 Son Dakika: Manchester United...
✅ Logo eklendi
✅ Görsel yüklendi (logo ile)
✅ Tweet paylaşıldı!
```

## ☁️ 24/7 ÇALIŞTIRMA (Bilgisayar Kapalı Olsa Bile)

### En Kolay: Railway.app (ÜCRETSİZ)

1. **Railway'e git:** https://railway.app/
2. "New Project" → "Empty Project"
3. "Variables" → `.env` içeriğini yapıştır
4. "Deploy from GitHub" veya dosyaları yükle
5. Bitir! Bot 24/7 çalışacak

📖 **Detaylı rehber:** `KURULUM_REHBERI.md` → "24/7 Çalıştırma" bölümü

**Diğer seçenekler:**
- Render.com (ücretsiz)
- Fly.io (ücretsiz)
- VPS (DigitalOcean, $5/ay)

## 📊 NEYİ DEĞİŞTİRDİK?

### ✅ Teknik Düzeltmeler:

1. **API Çağrıları:**
   - Doğru model adı: `claude-sonnet-4-20250514`
   - Hata yakalama iyileştirildi
   - Timeout ayarları eklendi

2. **Görsel İşleme:**
   - Logo otomatik ekleme özelliği
   - Görsel boyutlandırma düzeltildi
   - RGBA → RGB dönüşümü eklendi

3. **Tweet İşleme:**
   - Tweet ID string olarak saklanıyor (int overflow fix)
   - Medya yükleme hataları düzeltildi
   - Rate limit koruması eklendi

4. **Loglar:**
   - Her adımda detaylı bilgi
   - Emoji ile daha okunabilir
   - Hata mesajları iyileştirildi

### 🎨 Logo Ekleme:

- Görselin %15'i kadar logo boyutu
- Sağ üst köşe, 10px padding
- RGBA desteği (şeffaf arka plan)
- Orantılı yeniden boyutlandırma

## ⚙️ AYARLAR

Bot dosyasının başındaki `CONFIG` bölümünü düzenle:

```python
CONFIG = {
    "tracked_accounts": ["FabrizioRomano", "David_Ornstein"],  # Takip edilen hesaplar
    "check_interval_minutes": 30,  # Kontrol sıklığı
    "max_tweet_length": 280,       # Tweet uzunluğu
    "logo_path": "omt_logo.png",   # Logo dosyası
    "logo_size_ratio": 0.15,       # Logo boyutu (%15)
}
```

## 💰 MALİYET

- **Railway/Render:** Ücretsiz
- **Anthropic API:** Ayda ~$3-5 (tweet başına $0.003)
- **Twitter API:** Ücretsiz
- **VPS (opsiyonel):** $5/ay

**Toplam:** Ayda ~$3-5 (ücretsiz hosting ile)

## 🐛 SORUN GİDERME

### "Authentication failed"
- `.env` dosyasını kontrol et
- Twitter'da "Read and Write" yetkisi var mı?

### "Logo yüklenemedi"
- `omt_logo.png` dosyası bot ile aynı klasörde mi?

### Tweet atılmıyor
- Twitter API limitlerini aştın mı?
- Access token doğru mu?

### Bot durdu
- Logları kontrol et
- Railway otomatik restart atar

## 📁 DOSYA YAPISI

```
twitter-bot/
├── twitter_bot_fixed.py      # ✅ Düzeltilmiş bot kodu
├── omt_logo.png              # 🎨 Logonuz
├── KURULUM_REHBERI.md        # 📖 Detaylı rehber
├── README_UPDATED.md         # 📄 Bu dosya
├── requirements.txt          # 📦 Python paketleri
├── Dockerfile                # 🐳 Docker config
├── setup.sh                  # 🔧 Linux/Mac kurulum
├── setup.bat                 # 🔧 Windows kurulum
└── .env.example              # ⚙️ API anahtarları template
```

## ⚠️ ÖNEMLİ NOTLAR

1. **Twitter Kuralları:**
   - Profil bio'nuzda "Bot 🤖" yazın
   - Spam yapmayın
   - Rate limitlere uyun

2. **API Güvenliği:**
   - `.env` dosyasını GitHub'a yüklemeyin
   - API anahtarlarını kimseyle paylaşmayın

3. **Telif Hakkı:**
   - Görseller yeniden oluşturulmadı (logo ekleme sadece)
   - Metinler sadeleştirildi
   - Kaynak belirtilmedi (Twitter kurallarına göre)

## 📞 YARDIM

Sorun yaşarsan:
1. `KURULUM_REHBERI.md` dosyasını oku
2. Logları kontrol et (`.env`, API anahtarları, logo dosyası)
3. Railway loglarına bak

---

**Hazırlayan:** Claude AI  
**Son Güncelleme:** 2026-02-11  
**Versiyon:** 2.0 (Logo + Düzeltmeler)
