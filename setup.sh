#!/bin/bash
# Twitter Bot Hızlı Kurulum Scripti

echo "🤖 Twitter Bot Kurulum Başlıyor..."
echo ""

# Python versiyonunu kontrol et
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 bulunamadı! Lütfen Python 3.8+ kurun."
    exit 1
fi

echo "✅ Python versiyon: $(python3 --version)"

# Pip versiyonunu kontrol et
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 bulunamadı!"
    exit 1
fi

echo "✅ pip versiyon: $(pip3 --version)"
echo ""

# Paketleri kur
echo "📦 Python paketleri kuruluyor..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Paket kurulumu başarısız!"
    exit 1
fi

echo "✅ Paketler kuruldu!"
echo ""

# .env dosyası kontrolü
if [ ! -f ".env" ]; then
    echo "📝 .env dosyası oluşturuluyor..."
    cp .env.example .env
    echo "⚠️  .env dosyasını düzenleyip API anahtarlarını ekleyin!"
    echo ""
    echo "Gerekli API Anahtarları:"
    echo "  1. Twitter API Keys (5 adet)"
    echo "  2. Anthropic API Key (1 adet)"
    echo ""
    echo "Detaylı rehber için: KURULUM_REHBERI.md dosyasını okuyun"
    echo ""
fi

# Logo kontrolü
if [ ! -f "omt_logo.png" ]; then
    echo "⚠️  Logo dosyası (omt_logo.png) bulunamadı!"
    echo "   Logo olmadan da çalışır ama görsellere logo eklenmez."
    echo ""
fi

echo "✅ Kurulum tamamlandı!"
echo ""
echo "Sonraki adımlar:"
echo "  1. nano .env    (API anahtarlarını ekle)"
echo "  2. python3 twitter_bot_fixed.py    (Botu çalıştır)"
echo ""
echo "24/7 çalıştırma için: KURULUM_REHBERI.md dosyasına bakın"
