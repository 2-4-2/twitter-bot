# 🚀 API KURULUM VE 24/7 ÇALIŞTIRMA REHBERİ

## 📋 İÇİNDEKİLER
1. [Twitter API Kurulumu](#twitter-api)
2. [Anthropic API Kurulumu](#anthropic-api)
3. [Bot Kurulumu](#bot-kurulumu)
4. [24/7 Çalıştırma (Cloud)](#247-çalıştırma)

---

## 🐦 TWITTER API KURULUMU {#twitter-api}

### Adım 1: Twitter Developer Hesabı Oluştur

1. **Developer Portal'a Git:**
   - https://developer.twitter.com/ adresine git
   - Twitter hesabınla giriş yap
   - "Sign up for Free Account" butonuna tıkla

2. **Hesap Türü Seç:**
   - "Hobbyist" → "Making a bot" seç
   - Formları doldur (bot ne yapacak, kişisel kullanım vb.)
   - Email doğrulama yap

### Adım 2: App Oluştur

1. **Developer Portal Dashboard:**
   - https://developer.twitter.com/en/portal/dashboard
   - "Projects & Apps" → "+ Create App" tıkla

2. **App İsmi Ver:**
   - Örnek: "OMT_Transfer_Bot"
   - "Next" tıkla

3. **API Keys Kaydet:**
   ```
   API Key (Consumer Key): xxxxxxxxxxxxxxxxxxxxx
   API Key Secret (Consumer Secret): xxxxxxxxxxxxxxxxxxxxx
   Bearer Token: AAAAAAAAAAAAAAAAAAAAAxxxxxxxxxxxx
   ```
   ⚠️ **ÖNEMLİ:** Bu anahtarları güvenli bir yere kaydet! Bir daha gösterilmeyecek!

### Adım 3: Access Token Al

1. **App Settings:**
   - Developer Portal → Your App → "Keys and tokens" sekmesi
   - "Access Token and Secret" bölümünde "Generate" tıkla

2. **Yetkileri Ayarla:**
   - Settings → "User authentication settings" → "Set up"
   - App permissions: **"Read and Write"** seç (ÖNEMLİ!)
   - Type of App: "Web App" seç
   - Callback URL: `https://example.com` (herhangi bir URL)
   - Website URL: Kendi siteniz varsa o, yoksa `https://twitter.com/yourhandle`
   - "Save" tıkla

3. **Access Token Oluştur:**
   - "Access Token and Secret" → "Generate"
   ```
   Access Token: xxxxxxxxxxxxxxxxxxxxx
   Access Token Secret: xxxxxxxxxxxxxxxxxxxxx
   ```

### Twitter API Anahtarlarını Özet:
```
✅ API Key (Consumer Key)
✅ API Key Secret (Consumer Secret) 
✅ Bearer Token
✅ Access Token
✅ Access Token Secret
```

---

## 🤖 ANTHROPIC API KURULUMU {#anthropic-api}

### Adım 1: Anthropic Hesabı Aç

1. **Console'a Git:**
   - https://console.anthropic.com/
   - "Sign Up" ile hesap oluştur
   - Email doğrulama yap

### Adım 2: API Key Al

1. **API Keys Sayfası:**
   - Console → "API Keys" menüsü
   - "+ Create Key" tıkla
   - İsim ver: "Twitter Bot"
   - "Create Key" tıkla

2. **API Key'i Kaydet:**
   ```
   ANTHROPIC_API_KEY: sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxx
   ```
   ⚠️ **ÖNEMLİ:** Bu anahtarı kaydet! Bir daha gösterilmeyecek!

### Adım 3: Kredi Ekle (Opsiyonel)

- Ücretsiz tier: Ayda $5 kredi
- Daha fazla kullanım için: Settings → Billing → Add credit

**Maliyet Tahmini:**
- Her tweet sadeleştirme: ~$0.003
- Ayda 1000 tweet: ~$3

---

## 💻 BOT KURULUMU {#bot-kurulumu}

### Adım 1: Dosyaları Hazırla

1. **Proje Klasörü:**
   ```bash
   cd twitter-bot
   ls
   # twitter_bot_fixed.py
   # omt_logo.png
   # requirements.txt
   # .env.example
   ```

2. **Python Paketlerini Yükle:**
   ```bash
   pip install -r requirements.txt
   ```

### Adım 2: .env Dosyası Oluştur

1. **Example'ı Kopyala:**
   ```bash
   cp .env.example .env
   ```

2. **API Anahtarlarını Ekle:**
   ```bash
   nano .env  # veya notepad .env (Windows)
   ```

   **İçerik (.env dosyası):**
   ```env
   # Twitter API Keys
   TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAxxxxxxxxxxxxxxxx
   TWITTER_API_KEY=xxxxxxxxxxxxxxxxxxxxx
   TWITTER_API_SECRET=xxxxxxxxxxxxxxxxxxxxx
   TWITTER_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxxx
   TWITTER_ACCESS_TOKEN_SECRET=xxxxxxxxxxxxxxxxxxxxx

   # Anthropic API Key
   ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxx
   ```

   ⚠️ Tüm `xxxx` yerlerine kendi API anahtarlarını yapıştır!

### Adım 3: Test Et

1. **Botu Çalıştır:**
   ```bash
   python twitter_bot_fixed.py
   ```

2. **Çıktı Görmeli:**
   ```
   🤖 Twitter Bot başlatıldı!
   👀 Takip edilen hesaplar: FabrizioRomano, David_Ornstein
   ⏰ Kontrol aralığı: 30 dakika
   🎨 Logo: ✅ Aktif

   🔍 Kontrol ediliyor... [2026-02-11 20:30:00]
     @FabrizioRomano: 2 yeni tweet bulundu
   📝 İşleniyor: @FabrizioRomano - 🚨🔴 EXCLUSIVE...
   ```

3. **Hata Varsa:**
   - `.env` dosyasını kontrol et
   - API anahtarlarının doğru olduğundan emin ol
   - Twitter App'in "Read and Write" yetkisi var mı kontrol et

---

## ☁️ 24/7 ÇALIŞTIRMA (Bilgisayar Kapalı Olsa Bile) {#247-çalıştırma}

### SEÇENEK 1: Railway.app (ÖNERİLEN - ÜCRETSİZ)

**Neden Railway:**
- ✅ Tamamen ücretsiz ($5/ay kredi)
- ✅ Kolay kurulum
- ✅ 24/7 çalışır
- ✅ Otomatik restart

**Adım Adım:**

1. **Railway Hesabı Aç:**
   - https://railway.app/ → "Start a New Project"
   - GitHub ile giriş yap

2. **Yeni Proje Oluştur:**
   - "New Project" → "Deploy from GitHub repo"
   - Repo seç (veya "Empty Project")

3. **Dosyaları Yükle:**
   
   **Dockerfile Oluştur:**
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   # Paketleri kur
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   # Bot dosyalarını kopyala
   COPY twitter_bot_fixed.py .
   COPY omt_logo.png .

   # Botu çalıştır
   CMD ["python", "-u", "twitter_bot_fixed.py"]
   ```

4. **Environment Variables Ekle:**
   - Railway Dashboard → Settings → Variables
   - Tüm `.env` içeriğini buraya ekle:
   ```
   TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAxxxxxxxxxxxxxxxx
   TWITTER_API_KEY=xxxxxxxxxxxxxxxxxxxxx
   TWITTER_API_SECRET=xxxxxxxxxxxxxxxxxxxxx
   TWITTER_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxxx
   TWITTER_ACCESS_TOKEN_SECRET=xxxxxxxxxxxxxxxxxxxxx
   ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxx
   ```

5. **Deploy Et:**
   - "Deploy" butonuna bas
   - 2-3 dakika bekle
   - Logs'ta "🤖 Twitter Bot başlatıldı!" göreceksin

6. **Log İzle:**
   - Dashboard → "View Logs"
   - Tweetlerin paylaşıldığını görebilirsin

**Railway Avantajları:**
- Bilgisayarın kapalı olsa bile çalışır
- Hata olsa otomatik restart atar
- Logları web'den izleyebilirsin

---

### SEÇENEK 2: Render.com (ÜCRETSİZ)

1. **Render Hesabı:**
   - https://render.com/ → Sign up
   - GitHub ile bağlan

2. **Web Service Oluştur:**
   - "New" → "Background Worker"
   - GitHub repo'nu bağla

3. **Build Command:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Command:**
   ```bash
   python twitter_bot_fixed.py
   ```

5. **Environment Variables:**
   - Tüm API anahtarlarını ekle

---

### SEÇENEK 3: Fly.io (ÜCRETSİZ)

1. **Fly.io Hesabı:**
   - https://fly.io/ → Sign up
   - Kredi kartı ister ama ücret almaz

2. **Fly CLI Kur:**
   ```bash
   # macOS
   brew install flyctl
   
   # Windows
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   
   # Linux
   curl -L https://fly.io/install.sh | sh
   ```

3. **Login:**
   ```bash
   flyctl auth login
   ```

4. **App Oluştur:**
   ```bash
   cd twitter-bot
   flyctl launch
   ```

5. **Secrets Ekle:**
   ```bash
   flyctl secrets set TWITTER_BEARER_TOKEN="AAAAAxxxxxx"
   flyctl secrets set TWITTER_API_KEY="xxxxxxx"
   flyctl secrets set TWITTER_API_SECRET="xxxxxxx"
   flyctl secrets set TWITTER_ACCESS_TOKEN="xxxxxxx"
   flyctl secrets set TWITTER_ACCESS_TOKEN_SECRET="xxxxxxx"
   flyctl secrets set ANTHROPIC_API_KEY="sk-ant-xxxxx"
   ```

6. **Deploy:**
   ```bash
   flyctl deploy
   ```

---

### SEÇENEK 4: VPS (Ubuntu Server - $5/ay)

**DigitalOcean / Linode / Vultr kullanarak:**

1. **VPS Kirala:**
   - DigitalOcean: https://www.digitalocean.com/
   - En ucuz plan: $4-5/ay

2. **SSH ile Bağlan:**
   ```bash
   ssh root@your-server-ip
   ```

3. **Bot Kur:**
   ```bash
   # Python kur
   apt update
   apt install python3 python3-pip git

   # Projeyi kopyala
   git clone your-repo-url
   cd twitter-bot

   # Paketleri kur
   pip3 install -r requirements.txt

   # .env dosyası oluştur
   nano .env
   # API anahtarlarını yapıştır
   ```

4. **Systemd Service Oluştur:**
   ```bash
   sudo nano /etc/systemd/system/twitter-bot.service
   ```

   **İçerik:**
   ```ini
   [Unit]
   Description=Twitter Transfer Bot
   After=network.target

   [Service]
   Type=simple
   User=root
   WorkingDirectory=/root/twitter-bot
   Environment="PATH=/usr/bin:/usr/local/bin"
   ExecStart=/usr/bin/python3 twitter_bot_fixed.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

5. **Servisi Başlat:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable twitter-bot
   sudo systemctl start twitter-bot
   
   # Status kontrol
   sudo systemctl status twitter-bot
   
   # Logları izle
   sudo journalctl -u twitter-bot -f
   ```

---

## 🎯 EN İYİ SEÇENEK ÖNERİSİ

**Yeni Başlayanlar İçin:**
- ✅ **Railway.app** - En kolay, ücretsiz, güvenilir

**Deneyimliyseniz:**
- ✅ **VPS** - Tam kontrol, ucuz, esnek

**Hızlı Test İçin:**
- ✅ **Render.com** - 5 dakikada hazır

---

## 📊 BOT İZLEME

### Railway Logs:
```
🤖 Twitter Bot başlatıldı!
🔍 Kontrol ediliyor... [2026-02-11 20:30:00]
  @FabrizioRomano: 1 yeni tweet bulundu
📝 İşleniyor: @FabrizioRomano - 🚨🔴 EXCLUSIVE...
✨ Sadeleştirilmiş: 🔴 Son Dakika: Manchester United...
✅ Logo eklendi
✅ Görsel yüklendi (logo ile)
✅ Tweet paylaşıldı: 🔴 Son Dakika: Manchester United...
✅ Tweet işlendi ve paylaşıldı!
💤 30 dakika bekleniyor...
```

---

## ⚠️ ÖNEMLİ NOTLAR

1. **Twitter Rate Limits:**
   - Saatte maks 300 tweet
   - Günde maks 2400 tweet
   - Bot bunları aşmaz (30dk kontrol = günde ~48 tweet max)

2. **Maliyet:**
   - Railway/Render: Ücretsiz
   - Anthropic API: Ayda ~$3-5
   - VPS: Ayda $5

3. **Bot Profili:**
   - Twitter bio'nuzda "Bot 🤖" yazın
   - Kurallar: https://help.twitter.com/en/rules-and-policies/twitter-automation

---

## 🐛 SORUN GİDERME

### "Authentication failed"
```bash
# API anahtarlarını kontrol et
cat .env

# Twitter Developer Portal'da "Read and Write" yetkisi var mı?
```

### "Logo yüklenemedi"
```bash
# Logo dosyası bot ile aynı klasörde mi?
ls -l omt_logo.png
```

### Bot durdu
```bash
# Railway: Otomatik restart atar
# VPS: systemctl restart twitter-bot
```

### Tweet atılmıyor
```bash
# Twitter API yetkilerini kontrol et
# Rate limit'e mi takıldı? (logs kontrol et)
```

---

## 📞 DESTEK

Sorun yaşarsan:
1. Logs'u kontrol et
2. `.env` dosyasını kontrol et
3. Twitter API yetkilerini kontrol et

---

**Hazırladım:** Claude AI  
**Son Güncelleme:** 2026-02-11
