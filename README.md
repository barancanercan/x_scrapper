# 🐦 X (Twitter) Scraper - Profesyonel Tweet Toplama Aracı

<div align="center">

![X Scraper](https://img.shields.io/badge/X-Scraper-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-FF6B6B?style=for-the-badge&logo=gradio&logoColor=white)

**X (Twitter) hesabınızdaki tweet'leri otomatik olarak toplayıp analiz eden güçlü scraper aracı**

[🚀 Hızlı Başlangıç](#-hızlı-başlangıç) • [📖 Kullanım Kılavuzu](#-kullanım-kılavuzu) • [🔧 Kurulum](#-detaylı-kurulum) • [❓ Sorun Giderme](#-sorun-giderme)

</div>

---

## 📋 İçindekiler

- [🌟 Özellikler](#-özellikler)
- [🚀 Hızlı Başlangıç](#-hızlı-başlangıç)
- [📦 Sistem Gereksinimleri](#-sistem-gereksinimleri)
- [🔧 Detaylı Kurulum](#-detaylı-kurulum)
- [📖 Kullanım Kılavuzu](#-kullanım-kılavuzu)
- [📊 Çıktı Formatları](#-çıktı-formatları)
- [⚙️ Yapılandırma](#️-yapılandırma)
- [🔒 Güvenlik](#-güvenlik)
- [❓ Sorun Giderme](#-sorun-giderme)
- [🤝 Katkıda Bulunma](#-katkıda-bulunma)
- [📄 Lisans](#-lisans)

---

## 🌟 Özellikler

### 🎯 **Temel Özellikler**
- ✅ **Gerçek X Scraping**: Ana sayfa timeline'ından gerçek tweet'leri toplar
- ✅ **Otomatik Giriş**: X hesabınıza güvenli giriş yapar
- ✅ **Etkileşim Verileri**: Beğeni, retweet, yanıt sayılarını toplar
- ✅ **CSV Export**: Google Sheets'e aktarılabilir format
- ✅ **Web Arayüzü**: Kullanıcı dostu Gradio interface
- ✅ **Otomatik Driver**: ChromeDriver otomatik yönetimi

### 🛠️ **Teknik Özellikler**
- 🔄 **Anti-Detection**: Bot algılama karşıtı önlemler
- 📊 **Real-time Stats**: Anlık istatistik takibi
- 🎛️ **Ayarlanabilir**: Tweet sayısı ve hız kontrolü
- 💾 **Veri Yönetimi**: Otomatik dosya isimlendirme
- 🖥️ **Cross-Platform**: Ubuntu/Linux desteği
- 🔒 **Güvenli**: Yerel veri işleme, harici sunucu yok

### 📈 **Toplanan Veriler**
| Veri Türü | Açıklama | Format |
|------------|----------|---------|
| Tweet Metni | Tam tweet içeriği | String (300 karakter) |
| Yazar | Tweet sahibinin adı | String |
| Beğeni Sayısı | Like count | Integer |
| Retweet Sayısı | RT count | Integer |
| Yanıt Sayısı | Reply count | Integer |
| Tweet URL'si | Direkt tweet linki | URL |
| Zaman Damgası | Toplama zamanı | DateTime |

---

## 🚀 Hızlı Başlangıç

### ⚡ 30 Saniyede Başlatma

```bash
# 1. Klasöre git
cd ~/Desktop/x_scrapper

# 2. Kurulum (ilk kez)
./setup_x_scraper.sh

# 3. Başlat
./start_x_scraper.sh
```

### 🌐 Web Arayüzü
Uygulama başladıktan sonra tarayıcınızda otomatik açılacak:
```
http://127.0.0.1:7864
```

---

## 📦 Sistem Gereksinimleri

### 🖥️ **İşletim Sistemi**
- Ubuntu 18.04+ (önerilen: 20.04 veya 22.04)
- Debian 10+
- Linux Mint 19+

### 🐍 **Python**
- Python 3.8 veya üzeri
- pip paket yöneticisi
- venv modülü

### 🌐 **Tarayıcı**
- Google Chrome 90+ veya Chromium
- Otomatik güncellemeler aktif önerilir

### 💾 **Donanım**
| Bileşen | Minimum | Önerilen |
|---------|---------|----------|
| RAM | 2 GB | 4 GB+ |
| Disk | 1 GB boş alan | 5 GB+ |
| İşlemci | 2 çekirdek | 4 çekirdek+ |
| İnternet | 1 Mbps | 5 Mbps+ |

---

## 🔧 Detaylı Kurulum

### 1️⃣ **Sistem Hazırlığı**

```bash
# Sistem güncellemesi
sudo apt update && sudo apt upgrade -y

# Python ve temel araçlar
sudo apt install python3 python3-pip python3-venv curl wget -y

# Chrome/Chromium kurulumu
sudo apt install chromium-browser -y
# VEYA Google Chrome:
# wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
# sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# sudo apt update && sudo apt install google-chrome-stable -y
```

### 2️⃣ **Proje Kurulumu**

```bash
# Proje klasörünü oluştur
mkdir -p ~/Desktop/x_scrapper
cd ~/Desktop/x_scrapper

# Dosyaları indir/kopyala (bu README ile birlikte gelen dosyalar)
# x_scraper.py, setup_x_scraper.sh, start_x_scraper.sh

# Scriptleri çalıştırılabilir yap
chmod +x setup_x_scraper.sh start_x_scraper.sh

# Python sanal ortamı ve bağımlılıkları kur
./setup_x_scraper.sh
```

### 3️⃣ **İlk Çalıştırma**

```bash
# X Scraper'ı başlat
./start_x_scraper.sh
```

### 4️⃣ **Kurulum Doğrulama**

Aşağıdaki adımları takip ederek kurulumun başarılı olduğunu doğrulayın:

1. ✅ Terminal'de "🚀 X Scraper arayüzü açılıyor..." mesajı görünür
2. ✅ Tarayıcıda http://127.0.0.1:7864 adresi açılır  
3. ✅ "🐦 X (Twitter) Scraper" başlığı görünür
4. ✅ "🚀 Tarayıcı Hazırla" butonu çalışır

---

## 📖 Kullanım Kılavuzu

### 🔰 **Temel Kullanım**

#### **Adım 1: Tarayıcı Hazırlığı**
1. Web arayüzünde **"🚀 Tarayıcı Hazırla"** butonuna tıklayın
2. ChromeDriver otomatik olarak indirilip kurulacak
3. **"✅ Chrome driver otomatik olarak kuruldu ve hazır!"** mesajını bekleyin

#### **Adım 2: X Hesabına Giriş**
1. **X Kullanıcı Adı** alanına hesap adınızı girin (@ işareti olmadan)
   ```
   Örnek: barancanercan (❌ @barancanercan değil)
   ```
2. **X Şifre** alanına hesap şifrenizi girin
3. **"🔐 X'e Giriş Yap"** butonuna tıklayın
4. Giriş işlemi 10-15 saniye sürebilir

#### **Adım 3: Tweet Toplama**
1. **Tweet Sayısı** belirleyin (5-100 arası önerilir)
   - İlk kullanım: 10-20 tweet
   - Deneyimli kullanım: 50-100 tweet
2. **"🚀 Tweet Topla"** butonuna tıklayın
3. İşlem süresi: ~30 saniye (20 tweet için)

#### **Adım 4: Veri Kaydetme**
1. Tweet toplama tamamlandığında **"💾 CSV Kaydet"** tıklayın
2. Dosya `x_tweets_YYYYMMDD_HHMMSS.csv` formatında kaydedilir
3. Google Sheets'e import edebilirsiniz

### 🎛️ **Gelişmiş Kullanım**

#### **Tweet Sayısı Optimizasyonu**
| Tweet Sayısı | Süre | Ram Kullanımı | Önerilen Durum |
|---------------|------|---------------|----------------|
| 5-10 | ~15 sn | Düşük | Test/Deneme |
| 20-30 | ~45 sn | Orta | Günlük kullanım |
| 50-70 | ~2 dk | Yüksek | Haftalık analiz |
| 80-100 | ~3 dk | Çok Yüksek | Aylık rapor |

#### **Hız ve Kalite Ayarları**
```python
# Gelişmiş kullanıcılar için x_scraper.py içinde değiştirilebilir:

# Scroll bekleme süresi (saniye)
time.sleep(3)  # Varsayılan: 3sn, Hızlı: 2sn, Güvenli: 5sn

# Maksimum scroll sayısı
max_scrolls = 15  # Varsayılan: 15, Hızlı: 10, Kapsamlı: 25

# Sayfa yükleme beklemesi
time.sleep(5)  # Varsayılan: 5sn, Hızlı: 3sn, Güvenli: 8sn
```

### 🔄 **Otomatik Kullanım Senaryoları**

#### **Günlük Tweet Toplama**
```bash
# Cron job ile günlük otomatik toplama
# crontab -e
0 9 * * * cd ~/Desktop/x_scrapper && ./daily_scrape.sh
```

#### **Toplu Analiz**
```bash
# Birden fazla CSV'yi birleştirme
cat x_tweets_*.csv > combined_tweets.csv
```

---

## 📊 Çıktı Formatları

### 📄 **CSV Formatı**
```csv
zaman,tweet,yazar,beğeni,retweet,yanıt,url
2025-07-29 14:30,Bu harika bir tweet!,Kullanici123,150,25,8,https://x.com/status/123456789
2025-07-29 14:31,Python öğreniyorum 🐍,TechLover,89,12,3,https://x.com/status/123456790
```

### 📈 **JSON Formatı** (İsteğe bağlı)
```json
{
  "tweets": [
    {
      "zaman": "2025-07-29 14:30",
      "tweet": "Bu harika bir tweet!",
      "yazar": "Kullanici123",
      "beğeni": 150,
      "retweet": 25,
      "yanıt": 8,
      "url": "https://x.com/status/123456789"
    }
  ],
  "istatistikler": {
    "toplam_tweet": 20,
    "toplam_beğeni": 2840,
    "ortalama_beğeni": 142
  }
}
```

### 📊 **Google Sheets İmport**
1. **Google Sheets** açın
2. **File → Import → Upload** seçin
3. CSV dosyasını sürükleyin
4. **Separator type: Comma** seçin
5. **Import data** tıklayın

### 📈 **Excel Analizi**
```excel
=AVERAGE(D:D)     // Ortalama beğeni
=SUM(E:E)         // Toplam retweet  
=MAX(F:F)         // En çok yanıt
=COUNTIF(C:C,"*Tech*")  // "Tech" içeren yazarlar
```

---

## ⚙️ Yapılandırma

### 🔧 **Temel Ayarlar**

#### **Port Değiştirme**
```python
# x_scraper.py dosyasının en altında
app.launch(server_name="127.0.0.1", server_port=7864, inbrowser=True)
# 7864 yerine istediğiniz portu yazın (örn: 8080)
```

#### **Tarayıcı Modu**
```python
# Headless mod (arka planda çalıştırma)
options.add_argument("--headless")

# Debug mod (geliştirici araçları)
options.add_argument("--auto-open-devtools-for-tabs")
```

### 🛡️ **Güvenlik Ayarları**

#### **Rate Limiting** (Hız Sınırlama)
```python
# Daha güvenli scraping için bekleme sürelerini artırın
time.sleep(5)  # Sayfa geçişleri arası
time.sleep(3)  # Scroll'lar arası
```

#### **User Agent Değiştirme**
```python
options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36")
```

### 📁 **Dosya Ayarları**

#### **Çıktı Dizini**
```python
# Farklı klasöre kaydetme
csv_file = Path("outputs/tweets/x_tweets_{timestamp}.csv")
```

#### **Dosya Formatı**
```python
# Dosya adı formatını değiştirme
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
csv_file = Path(f"tweets_{username}_{timestamp}.csv")
```

---

## 🔒 Güvenlik

### 🛡️ **Veri Güvenliği**

#### **Yerel Veri İşleme**
- ✅ Tüm veriler yerel bilgisayarınızda kalır
- ✅ Hiçbir veri harici sunucuya gönderilmez
- ✅ İnternet sadece X'e bağlanmak için kullanılır

#### **Hesap Güvenliği**
- ⚠️ **Önemli**: Sadece kendi hesabınızı kullanın
- ⚠️ **2FA**: İki faktörlü kimlik doğrulama etkinse devre dışı bırakın
- ⚠️ **Şifre**: Güçlü şifre kullanın, paylaşmayın

#### **Bot Algılama Önlemleri**
```python
# Mevcut anti-detection özellikleri:
- User-Agent maskeleme
- WebDriver özelliklerini gizleme  
- İnsan benzeri davranış (scroll, beklemeler)
- Rastgele timing değişiklikleri
```

### 🔐 **Gizlilik Önlemleri**

#### **Credential Yönetimi**
```bash
# Şifrelerinizi script'te saklamayın!
# Her seferinde manuel girin veya environment variable kullanın

export X_USERNAME="kullanici_adi"
export X_PASSWORD="sifre"
```

#### **Log Temizleme**
```bash
# Hassas logları temizleme
rm -f ~/.cache/selenium/
rm -f /tmp/chrome*
```

---

## ❓ Sorun Giderme

### 🔧 **Yaygın Sorunlar ve Çözümleri**

#### **1. ChromeDriver Uyumsuzluğu**
```
❌ Hata: "This version of ChromeDriver only supports Chrome version X"
```
**Çözüm:**
```bash
# Chrome'u güncelleyin
sudo apt update && sudo apt upgrade google-chrome-stable

# Veya scraper'ı yeniden başlatın (otomatik günceller)
./start_x_scraper.sh
```

#### **2. X Giriş Başarısız**
```
❌ Hata: "Giriş doğrulanamadı"
```
**Çözümler:**
```bash
# a) Kullanıcı adında @ işareti olmasın
❌ @kullanici_adi
✅ kullanici_adi

# b) 2FA kapalı olmalı
X Ayarlar → Güvenlik → İki faktörlü kimlik doğrulama → Kapat

# c) Şifrede özel karakterler
"Şifre123!" → elle yazın, copy-paste yapmayın

# d) Manuel kontrol
Tarayıcıda x.com'a manuel giriş yapabilir misiniz?
```

#### **3. Tweet Toplanamıyor**
```
❌ Hata: "❌ Önce X'e giriş yapın"
```
**Çözüm:**
```bash
# Giriş durumunu kontrol edin
1. "Giriş Durumu" kutusunda ✅ mesajı var mı?
2. Manuel olarak x.com/home açılıyor mu?
3. Uygulama penceresini minimize etmeyin
```

#### **4. Port Çakışması**
```
❌ Hata: "Address already in use: 7864"
```
**Çözüm:**
```bash
# Başka port kullanın
python x_scraper.py  # Hata verecek
# x_scraper.py'de port 7864 → 7865 değiştirin

# Veya çalışan uygulamayı kapatın
pkill -f "x_scraper.py"
```

#### **5. Boş CSV Dosyası**
```
❌ Sorun: CSV dosyası sadece header içeriyor
```
**Çözüm:**
```bash
# Daha fazla tweet sayısı deneyin
Tweet Sayısı: 5 → 20

# Farklı zamanda deneyin
Ana sayfa timeline'ında tweet var mı kontrol edin

# Debug mode
Terminal çıktısını takip edin: "🔍 X tweet elementi bulundu"
```

### 🐛 **Hata Logları**

#### **Debug Modunu Etkinleştirme**
```python
# x_scraper.py'de logging seviyesini değiştirin
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### **Terminal Çıktısını Kaydetme**
```bash
# Çalıştırırken logları dosyaya kaydet
./start_x_scraper.sh 2>&1 | tee debug.log
```

#### **Yaygın Hata Kodları**
| Hata Kodu | Açıklama | Çözüm |
|-----------|----------|-------|
| `TimeoutException` | Element bulunamadı | Bekleme süresini artırın |
| `NoSuchElementException` | Selector yanlış | X arayüzü değişmiş olabilir |
| `WebDriverException` | Chrome problemi | Chrome'u yeniden başlatın |
| `ConnectionRefusedError` | Port problemi | Portu değiştirin |

### 🚨 **Acil Durum Prosedürleri**

#### **Uygulama Dondu**
```bash
# 1. Ctrl+C ile durdurun
# 2. Tüm Chrome process'lerini kapatın
pkill -f chrome
pkill -f chromium

# 3. Yeniden başlatın
./start_x_scraper.sh
```

#### **Sistem Kaynakları Tükendi**
```bash
# RAM kullanımını kontrol edin
free -h

# Chrome process'lerini kontrol edin
ps aux | grep chrome

# Gerekirse bilgisayarı yeniden başlatın
sudo reboot
```

---

## 🔄 Güncellemeler ve Bakım

### 📅 **Rutin Bakım**

#### **Haftalık Kontroller**
```bash
# Chrome güncellemesi
sudo apt update && sudo apt upgrade google-chrome-stable

# Python paketleri
source venv/bin/activate
pip list --outdated
```

#### **Aylık Temizlik**
```bash
# Eski CSV dosyalarını arşivle
mkdir -p archive/$(date +%Y-%m)
mv x_tweets_*.csv archive/$(date +%Y-%m)/

# Cache temizliği
rm -rf ~/.cache/selenium/
rm -rf /tmp/chrome*
```

### 🔄 **Güncelleme Prosedürü**

#### **Manuel Güncelleme**
```bash
# 1. Mevcut versiyonu yedekle
cp x_scraper.py x_scraper_backup.py

# 2. Yeni kodu indirin
# 3. Ayarlarınızı yeni dosyaya aktarın
# 4. Test edin
```

#### **Otomatik Güncelleme** (İleri seviye)
```bash
# GitHub'dan otomatik güncelleme scripti
cat > update_scraper.sh << 'SCRIPT'
#!/bin/bash
echo "🔄 X Scraper güncelleniyor..."
git pull origin main
pip install -r requirements.txt
echo "✅ Güncelleme tamamlandı"
SCRIPT
```

---

## 📊 Performans Optimizasyonu

### ⚡ **Hız Optimizasyonu**

#### **Tarayıcı Ayarları**
```python
# Daha hızlı loading için x_scraper.py'de:
options.add_argument("--disable-images")
options.add_argument("--disable-plugins")  
options.add_argument("--disable-extensions")
options.add_argument("--no-first-run")
```

#### **Network Optimizasyonu**
```python
# Sadece gerekli kaynakları yükle
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
```

### 📈 **Kaynak Yönetimi**

#### **RAM Kullanımını Azaltma**
```python
# Tweet sayısını sınırla
max_tweets = 50  # 100 yerine

# Scroll sayısını azalt  
max_scrolls = 10  # 15 yerine
```

#### **CPU Kullanımını Azaltma**
```python
# Daha uzun beklemeler
time.sleep(4)  # 3 yerine
```

---

## 📚 API ve Entegrasyon

### 🔌 **Harici Entegrasyonlar**

#### **Google Sheets API**
```python
# Google Sheets'e otomatik upload için:
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Credentials ayarla
scope = ["https://spreadsheets.google.com/feeds"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

# Upload fonksiyonu
def upload_to_sheets(csv_file):
    sheet = client.open("X Tweets Analysis").sheet1
    with open(csv_file, 'r') as f:
        content = f.read()
    client.import_csv(sheet.id, content)
```

#### **Webhook Entegrasyonu**
```python
# Slack/Discord bildirim
import requests

def send_notification(message):
    webhook_url = "https://hooks.slack.com/..."
    requests.post(webhook_url, json={"text": message})

# Scraping tamamlandığında bildir
send_notification(f"✅ {len(tweets)} tweet toplandı!")
```

### 📊 **Veri Analizi Örnekleri**

#### **Pandas ile Analiz**
```python
import pandas as pd

# CSV'yi oku
df = pd.read_csv('x_tweets_20250729_143022.csv')

# Temel istatistikler
print(f"Toplam tweet: {len(df)}")
print(f"Ortalama beğeni: {df['beğeni'].mean():.0f}")
print(f"En popüler tweet: {df.loc[df['beğeni'].idxmax(), 'tweet']}")

# En aktif yazarlar
top_authors = df['yazar'].value_counts().head(10)
print("En aktif yazarlar:")
print(top_authors)
```

#### **Matplotlib ile Grafik**
```python
import matplotlib.pyplot as plt

# Beğeni dağılımı histogramı
plt.figure(figsize=(10, 6))
plt.hist(df['beğeni'], bins=20, alpha=0.7)
plt.title('Tweet Beğeni Dağılımı')
plt.xlabel('Beğeni Sayısı')
plt.ylabel('Tweet Sayısı')
plt.savefig('begeni_dagilimi.png')
plt.show()
```

---

## 🤝 Katkıda Bulunma

### 💡 **Geliştirme Fikirleri**

#### **Özellik Talepleri**
- [ ] **Multi-account support**: Birden fazla hesap
- [ ] **Scheduled scraping**: Zamanlanmış toplama
- [ ] **Real-time monitoring**: Canlı takip
- [ ] **Advanced filters**: Hashtag, mention filtreleri
- [ ] **Export formats**: JSON, Excel, PDF export
- [ ] **Analytics dashboard**: Grafik ve analiz paneli

#### **Teknik İyileştirmeler**
- [ ] **Docker support**: Containerized deployment
- [ ] **REST API**: HTTP API endpoint'leri
- [ ] **Database integration**: PostgreSQL/MySQL desteği
- [ ] **Proxy support**: Proxy sunucu desteği
- [ ] **Captcha solving**: Otomatik captcha çözümü

### 🔧 **Geliştirme Ortamı**

#### **Katkıda Bulunma Adımları**
1. **Fork** edin
2. **Feature branch** oluşturun: `git checkout -b yeni-ozellik`
3. **Commit** edin: `git commit -m "Yeni özellik eklendi"`
4. **Push** edin: `git push origin yeni-ozellik`
5. **Pull Request** oluşturun

#### **Code Style**
```python
# PEP 8 standardını takip edin
# Type hints kullanın
def scrape_tweets(max_tweets: int) -> List[Dict[str, Any]]:
    """Tweet'leri topla."""
    pass

# Docstring ekleyin
def login_x(username: str, password: str) -> bool:
    """
    X hesabına giriş yapar.
    
    Args:
        username: X kullanıcı adı
        password: X şifresi
        
    Returns:
        Giriş başarılıysa True, aksi halde False
    """
```

### 🐛 **Bug Raporu**

#### **Bug Raporu Formatı**
```markdown
**Bug Açıklaması**
Kısa ve net açıklama

**Hatayı Tekrarlama Adımları**
1. Bu adımı izle
2. Bu butona tıkla
3. Bu hatayı gör

**Beklenen Davranış**
Ne olmasını bekliyordunuz

**Ekran Görüntüleri**
Mümkünse screenshot ekleyin

**Sistem Bilgileri**
- OS: Ubuntu 22.04
- Python: 3.10.12
- Chrome: 126.0.6478.126
```

---

## 📄 Lisans

### 📜 **MIT Lisansı**

```
MIT License

Copyright (c) 2025 X Scraper

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### ⚖️ **Yasal Uyarılar**

#### **Kullanım Koşulları**# x_scrapper
