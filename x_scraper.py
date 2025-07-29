#!/usr/bin/env python3
"""
Çalışan X Scraper - Otomatik Driver Yönetimi
"""

import time
import csv
import json
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import gradio as gr

class WorkingXScraper:
    def __init__(self):
        self.driver = None
        self.is_logged_in = False
        self.tweets_data = []
        
    def setup_driver(self):
        """Chrome driver otomatik kurulum"""
        try:
            # Chrome seçenekleri
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-images")  # Hız için
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Otomatik driver yönetimi
            service = Service(ChromeDriverManager().install())
            
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return "✅ Chrome driver otomatik olarak kuruldu ve hazır!"
            
        except Exception as e:
            return f"❌ Driver hatası: {e}\n💡 Çözüm: Chrome tarayıcınızı güncelleyin"
    
    def login_x(self, username, password):
        """X'e giriş yap"""
        if not self.driver:
            return "❌ Önce tarayıcıyı hazırlayın"
        
        try:
            print("🔐 X'e giriş yapılıyor...")
            
            # X giriş sayfası
            self.driver.get("https://x.com/i/flow/login")
            time.sleep(5)
            
            # Kullanıcı adı girişi - farklı selector'lar dene
            username_selectors = [
                'input[autocomplete="username"]',
                'input[name="text"]',
                'input[placeholder*="kullanıcı"]',
                'input[placeholder*="username"]'
            ]
            
            username_found = False
            for selector in username_selectors:
                try:
                    username_input = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    username_input.clear()
                    username_input.send_keys(username)
                    username_found = True
                    break
                except:
                    continue
            
            if not username_found:
                return "❌ Kullanıcı adı alanı bulunamadı"
            
            time.sleep(2)
            
            # İleri butonu - farklı yöntemler dene
            next_methods = [
                lambda: self.driver.find_element(By.XPATH, '//span[text()="Next"]/..').click(),
                lambda: self.driver.find_element(By.XPATH, '//span[text()="İleri"]/..').click(),
                lambda: self.driver.find_element(By.CSS_SELECTOR, '[role="button"]').click(),
                lambda: self.driver.find_element(By.XPATH, '//div[@role="button"]').click()
            ]
            
            next_clicked = False
            for method in next_methods:
                try:
                    method()
                    next_clicked = True
                    break
                except:
                    continue
            
            if not next_clicked:
                # Enter tuşu dene
                username_input.send_keys('\n')
            
            time.sleep(3)
            
            # Şifre girişi
            password_selectors = [
                'input[type="password"]',
                'input[name="password"]',
                'input[autocomplete="current-password"]'
            ]
            
            password_found = False
            for selector in password_selectors:
                try:
                    password_input = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    password_input.clear()
                    password_input.send_keys(password)
                    password_found = True
                    break
                except:
                    continue
            
            if not password_found:
                return "❌ Şifre alanı bulunamadı"
            
            time.sleep(2)
            
            # Giriş butonu
            login_methods = [
                lambda: self.driver.find_element(By.XPATH, '//span[text()="Log in"]/..').click(),
                lambda: self.driver.find_element(By.XPATH, '//span[text()="Giriş yap"]/..').click(),
                lambda: self.driver.find_element(By.CSS_SELECTOR, '[data-testid="LoginForm_Login_Button"]').click(),
                lambda: password_input.send_keys('\n')
            ]
            
            login_clicked = False
            for method in login_methods:
                try:
                    method()
                    login_clicked = True
                    break
                except:
                    continue
            
            # Giriş kontrolü için bekle
            time.sleep(8)
            
            # Giriş başarı kontrolü
            current_url = self.driver.current_url
            page_source = self.driver.page_source.lower()
            
            success_checks = [
                "home" in current_url,
                "timeline" in page_source,
                "tweet" in page_source,
                "compose" in page_source
            ]
            
            if any(success_checks):
                self.is_logged_in = True
                return f"✅ X'e başarıyla giriş yapıldı!\n🔗 URL: {current_url}"
            else:
                return f"❌ Giriş doğrulanamadı.\n🔗 Mevcut URL: {current_url}\n💡 Manuel kontrol gerekebilir"
                
        except Exception as e:
            return f"❌ Giriş hatası: {e}"
    
    def scrape_tweets(self, max_tweets=20):
        """Tweet'leri topla"""
        if not self.is_logged_in:
            return "❌ Önce X'e giriş yapın", [], {}
        
        try:
            print(f"📱 {max_tweets} tweet toplanıyor...")
            
            # Ana sayfaya git
            self.driver.get("https://x.com/home")
            time.sleep(5)
            
            tweets = []
            scroll_count = 0
            max_scrolls = 15
            
            while len(tweets) < max_tweets and scroll_count < max_scrolls:
                # Tweet'leri bul
                tweet_elements = self.driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
                print(f"🔍 {len(tweet_elements)} tweet elementi bulundu")
                
                for tweet_elem in tweet_elements:
                    if len(tweets) >= max_tweets:
                        break
                    
                    try:
                        # Tweet metni
                        try:
                            text_elem = tweet_elem.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
                            tweet_text = text_elem.text.strip()
                        except:
                            continue  # Metin yoksa atla
                        
                        if not tweet_text or len(tweet_text) < 3:
                            continue
                        
                        # Yazar bilgisi
                        try:
                            author_elem = tweet_elem.find_element(By.CSS_SELECTOR, '[data-testid="User-Name"]')
                            author_text = author_elem.text
                            author = author_text.split('\n')[0] if author_text else 'Bilinmeyen'
                        except:
                            author = 'Bilinmeyen'
                        
                        # Etkileşim sayıları
                        def get_interaction_count(testid):
                            try:
                                elem = tweet_elem.find_element(By.CSS_SELECTOR, f'[data-testid="{testid}"]')
                                aria_label = elem.get_attribute('aria-label') or '0'
                                return self._extract_number(aria_label)
                            except:
                                return 0
                        
                        likes = get_interaction_count('like')
                        retweets = get_interaction_count('retweet')
                        replies = get_interaction_count('reply')
                        
                        # Tweet URL'si
                        try:
                            link_elem = tweet_elem.find_element(By.CSS_SELECTOR, 'a[href*="/status/"]')
                            tweet_url = link_elem.get_attribute('href')
                        except:
                            tweet_url = f"https://x.com/status/{int(time.time())}"
                        
                        # Tweet verisi
                        tweet_data = {
                            'zaman': datetime.now().strftime('%Y-%m-%d %H:%M'),
                            'tweet': tweet_text[:300] + ('...' if len(tweet_text) > 300 else ''),
                            'yazar': author,
                            'beğeni': likes,
                            'retweet': retweets,
                            'yanıt': replies,
                            'url': tweet_url
                        }
                        
                        # Duplicate kontrolü
                        if not any(t.get('url') == tweet_url for t in tweets):
                            tweets.append(tweet_data)
                            print(f"✅ Tweet eklendi: {author} - {likes} beğeni")
                    
                    except Exception as e:
                        continue
                
                # Scroll ve bekle
                if len(tweets) < max_tweets:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)
                    scroll_count += 1
                    print(f"📜 Scroll {scroll_count}/{max_scrolls} - Toplam tweet: {len(tweets)}")
            
            self.tweets_data = tweets
            
            # İstatistikler
            total_likes = sum(t['beğeni'] for t in tweets)
            total_retweets = sum(t['retweet'] for t in tweets)
            avg_likes = total_likes // len(tweets) if tweets else 0
            
            stats = {
                "toplanan_tweet": len(tweets),
                "toplam_beğeni": total_likes,
                "toplam_retweet": total_retweets,
                "ortalama_beğeni": avg_likes,
                "son_güncelleme": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Tablo verisi
            table_data = [[
                t['zaman'], 
                t['tweet'][:80] + '...' if len(t['tweet']) > 80 else t['tweet'],
                t['yazar'], 
                t['beğeni'], 
                t['retweet'], 
                t['yanıt']
            ] for t in tweets]
            
            result_msg = f"""🎉 Tweet toplama tamamlandı!

📊 Özet:
- Toplanan Tweet: {len(tweets)}
- Toplam Beğeni: {total_likes:,}
- Toplam Retweet: {total_retweets:,}
- Ortalama Beğeni: {avg_likes}

📁 CSV kaydetmeye hazır!"""
            
            return result_msg, table_data, stats
            
        except Exception as e:
            return f"❌ Scraping hatası: {e}", [], {}
    
    def _extract_number(self, text):
        """Sayıları çıkar (1.2K -> 1200)"""
        import re
        if not text:
            return 0
        
        # Sayıları bul
        numbers = re.findall(r'[\d,]+\.?\d*[KMB]?', str(text))
        if not numbers:
            return 0
        
        num_str = numbers[0].replace(',', '').upper()
        
        if 'K' in num_str:
            return int(float(num_str.replace('K', '')) * 1000)
        elif 'M' in num_str:
            return int(float(num_str.replace('M', '')) * 1000000)
        elif 'B' in num_str:
            return int(float(num_str.replace('B', '')) * 1000000000)
        else:
            try:
                return int(float(num_str))
            except:
                return 0
    
    def save_csv(self):
        """CSV'ye kaydet"""
        if not self.tweets_data:
            return "❌ Kaydedilecek veri yok"
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            csv_file = Path(f"x_tweets_{timestamp}.csv")
            
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['zaman', 'tweet', 'yazar', 'beğeni', 'retweet', 'yanıt', 'url'])
                writer.writeheader()
                writer.writerows(self.tweets_data)
            
            return f"✅ CSV kaydedildi: {csv_file}\n📊 {len(self.tweets_data)} tweet kaydedildi"
            
        except Exception as e:
            return f"❌ CSV kaydetme hatası: {e}"
    
    def close(self):
        """Driver'ı kapat"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                return "✅ Tarayıcı kapatıldı"
            return "ℹ️ Tarayıcı zaten kapalı"
        except:
            return "⚠️ Tarayıcı kapatma hatası"

# Global scraper instance
scraper = WorkingXScraper()

# Gradio fonksiyonları
def setup_browser():
    return scraper.setup_driver()

def login(username, password):
    if not username or not password:
        return "❌ Kullanıcı adı ve şifre gerekli!"
    
    # @ işaretini kaldır
    clean_username = username.replace('@', '')
    return scraper.login_x(clean_username, password)

def scrape_tweets_handler(tweet_count):
    return scraper.scrape_tweets(int(tweet_count))

def save_data():
    return scraper.save_csv()

def close_browser():
    return scraper.close()

# Gradio UI
with gr.Blocks(title="🐦 X Scraper - Çalışan Versiyon", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🐦 X (Twitter) Scraper - Gerçek Çalışan Versiyon")
    gr.Markdown("⚡ **Otomatik driver yönetimi** ile ChromeDriver sorunları çözüldü!")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🔧 1. Kurulum")
            setup_btn = gr.Button("🚀 Tarayıcı Hazırla", variant="primary", size="lg")
            setup_output = gr.Textbox(label="Kurulum Durumu", lines=3)
            
            gr.Markdown("### 🔐 2. X Giriş")
            username = gr.Textbox(
                label="👤 X Kullanıcı Adı", 
                placeholder="kullanici_adi (@ olmadan)",
                info="@ işareti olmadan yazın"
            )
            password = gr.Textbox(
                label="🔒 X Şifre", 
                type="password",
                info="X hesap şifreniz"
            )
            login_btn = gr.Button("🔐 X'e Giriş Yap", variant="primary", size="lg")
            login_output = gr.Textbox(label="Giriş Durumu", lines=4)
            
            gr.Markdown("### 📊 3. Tweet Toplama")
            tweet_count = gr.Number(
                label="Tweet Sayısı", 
                value=20, 
                minimum=5, 
                maximum=100,
                info="5-100 arası tweet toplanabilir"
            )
            scrape_btn = gr.Button("🚀 Tweet Topla", variant="primary", size="lg")
            
            gr.Markdown("### 💾 4. Kaydet & Kapat")
            with gr.Row():
                save_btn = gr.Button("💾 CSV Kaydet", variant="secondary")
                close_btn = gr.Button("❌ Kapat", variant="secondary")
        
        with gr.Column(scale=2):
            scrape_output = gr.Textbox(
                label="📤 İşlem Sonuçları", 
                lines=12,
                show_copy_button=True
            )
            
            stats = gr.JSON(
                label="📊 İstatistikler", 
                value={"toplanan_tweet": 0, "durum": "Henüz veri yok"}
            )
    
    gr.Markdown("### 📋 Toplanan Tweet'ler")
    tweet_table = gr.Dataframe(
        label="🐦 Tweet Listesi",
        headers=["Zaman", "Tweet", "Yazar", "Beğeni", "RT", "Yanıt"],
        wrap=True
    )
    
    # Event handlers
    setup_btn.click(setup_browser, outputs=[setup_output])
    login_btn.click(login, inputs=[username, password], outputs=[login_output])
    scrape_btn.click(scrape_tweets_handler, inputs=[tweet_count], outputs=[scrape_output, tweet_table, stats])
    save_btn.click(save_data, outputs=[scrape_output])
    close_btn.click(close_browser, outputs=[scrape_output])

if __name__ == "__main__":
    print("🚀 X Scraper başlatılıyor...")
    print("📱 Otomatik ChromeDriver yönetimi aktif")
    app.launch(server_name="127.0.0.1", server_port=7864, inbrowser=True)
