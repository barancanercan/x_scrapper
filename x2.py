#!/usr/bin/env python3
"""
Gelişmiş X Scraper - Tam Özellikli Versiyon
- View sayıları (düzeltildi)
- Tweet tarihleri
- Following/For You seçenekleri
- Profil bazlı scraping
- Zaman filtreleme
- Hashtag arama
"""

import time
import csv
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import gradio as gr


class AdvancedXScraper:
    def __init__(self):
        self.driver = None
        self.is_logged_in = False
        self.tweets_data = []

    def setup_driver(self):
        """Chrome driver otomatik kurulum"""
        try:
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            # View sayıları için images gerekli olabilir, kaldırdık
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

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

            self.driver.get("https://x.com/i/flow/login")
            time.sleep(5)

            # Kullanıcı adı girişi
            username_selectors = [
                'input[autocomplete="username"]',
                'input[name="text"]',
                'input[data-testid="ocfEnterTextTextInput"]'
            ]

            username_found = False
            username_input = None
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

            # İleri butonu
            try:
                next_btn = self.driver.find_element(By.XPATH, '//span[text()="Next"]/parent::*')
                next_btn.click()
            except:
                username_input.send_keys(Keys.ENTER)

            time.sleep(3)

            # Şifre girişi
            try:
                password_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
                )
                password_input.clear()
                password_input.send_keys(password)
            except:
                return "❌ Şifre alanı bulunamadı"

            time.sleep(2)

            # Giriş butonu
            try:
                login_btn = self.driver.find_element(By.XPATH, '//span[text()="Log in"]/parent::*')
                login_btn.click()
            except:
                password_input.send_keys(Keys.ENTER)

            time.sleep(8)

            # Giriş kontrolü
            current_url = self.driver.current_url
            if "home" in current_url or "x.com" in current_url:
                self.is_logged_in = True
                return f"✅ X'e başarıyla giriş yapıldı!\n🔗 URL: {current_url}"
            else:
                return f"❌ Giriş doğrulanamadı.\n🔗 Mevcut URL: {current_url}"

        except Exception as e:
            return f"❌ Giriş hatası: {e}"

    def scrape_tweets(self, max_tweets=20, source_type="home", profile_username="", hashtag="", days_filter=0):
        """Gelişmiş tweet toplama"""
        if not self.is_logged_in:
            return "❌ Önce X'e giriş yapın", [], {}

        try:
            print(f"📱 {max_tweets} tweet toplanıyor...")

            # URL belirleme
            url = self._get_scraping_url(source_type, profile_username, hashtag)
            print(f"🔗 Gidilen URL: {url}")

            self.driver.get(url)
            time.sleep(5)

            tweets = []
            scroll_count = 0
            max_scrolls = 20
            cutoff_date = None

            if days_filter > 0:
                cutoff_date = datetime.now() - timedelta(days=days_filter)
                print(f"📅 Zaman filtresi: {cutoff_date.strftime('%Y-%m-%d')} sonrası")

            while len(tweets) < max_tweets and scroll_count < max_scrolls:
                # Tweet elementlerini bul
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
                            continue

                        if not tweet_text or len(tweet_text) < 3:
                            continue

                        # Yazar bilgisi - Geliştirildi
                        author_info = self._get_author_info(tweet_elem)

                        # Tweet tarihi - YENİ
                        tweet_date = self._get_tweet_date(tweet_elem)

                        # Zaman filtresi kontrolü
                        if cutoff_date and tweet_date:
                            if tweet_date < cutoff_date:
                                continue

                        # Etkileşim sayıları - Geliştirildi
                        interactions = self._get_all_interactions(tweet_elem)

                        # Tweet URL'si
                        tweet_url = self._get_tweet_url(tweet_elem)

                        # Tweet verisi
                        tweet_data = {
                            'zaman_toplama': datetime.now().strftime('%Y-%m-%d %H:%M'),
                            'tweet_tarihi': tweet_date.strftime('%Y-%m-%d %H:%M') if tweet_date else 'Bilinmiyor',
                            'tweet': tweet_text[:500] + ('...' if len(tweet_text) > 500 else ''),
                            'yazar': author_info['name'],
                            'yazar_handle': author_info['handle'],
                            'beğeni': interactions['likes'],
                            'retweet': interactions['retweets'],
                            'yanıt': interactions['replies'],
                            'görüntülenme': interactions['views'],
                            'url': tweet_url
                        }

                        # Duplicate kontrolü
                        if not any(t.get('url') == tweet_url for t in tweets):
                            tweets.append(tweet_data)
                            print(
                                f"✅ Tweet eklendi: @{author_info['handle']} - {interactions['likes']} ♥️, {interactions['views']} 👁️")

                    except Exception as e:
                        print(f"⚠️ Tweet işleme hatası: {e}")
                        continue

                # Scroll
                if len(tweets) < max_tweets:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(4)  # Daha uzun bekleme
                    scroll_count += 1
                    print(f"📜 Scroll {scroll_count}/{max_scrolls} - Toplam tweet: {len(tweets)}")

            self.tweets_data = tweets

            # İstatistikler
            stats = self._calculate_stats(tweets, source_type, profile_username, hashtag)

            # Tablo verisi
            table_data = [[
                t['tweet_tarihi'],
                t['tweet'][:60] + '...' if len(t['tweet']) > 60 else t['tweet'],
                f"@{t['yazar_handle']}",
                t['beğeni'],
                t['retweet'],
                t['yanıt'],
                t['görüntülenme']
            ] for t in tweets]

            result_msg = self._create_result_message(tweets, stats)

            return result_msg, table_data, stats

        except Exception as e:
            return f"❌ Scraping hatası: {e}", [], {}

    def _get_scraping_url(self, source_type, profile_username, hashtag):
        """Scraping URL'sini belirle"""
        base_url = "https://x.com"

        if hashtag:
            # Hashtag arama
            hashtag_clean = hashtag.replace('#', '').strip()
            return f"{base_url}/search?q=%23{hashtag_clean}&src=typed_query&f=live"

        if profile_username:
            # Profil scraping
            username_clean = profile_username.replace('@', '').strip()
            return f"{base_url}/{username_clean}"

        # Timeline scraping
        if source_type == "following":
            return f"{base_url}/home"  # Following tab'ı manuel seçilecek
        elif source_type == "foryou":
            return f"{base_url}/home"  # For You tab'ı manuel seçilecek
        else:
            return f"{base_url}/home"

    def _get_author_info(self, tweet_elem):
        """Yazar bilgilerini al"""
        try:
            # Yazar ismi ve handle
            author_elem = tweet_elem.find_element(By.CSS_SELECTOR, '[data-testid="User-Name"]')
            author_text = author_elem.text.strip()

            lines = author_text.split('\n')
            name = lines[0] if lines else 'Bilinmiyor'
            handle = lines[1].replace('@', '') if len(lines) > 1 and '@' in lines[1] else 'bilinmiyor'

            return {'name': name, 'handle': handle}
        except:
            return {'name': 'Bilinmiyor', 'handle': 'bilinmiyor'}

    def _get_tweet_date(self, tweet_elem):
        """Tweet tarihini al - Timezone hatası düzeltildi"""
        try:
            # Time elementi
            time_elem = tweet_elem.find_element(By.CSS_SELECTOR, 'time')
            datetime_attr = time_elem.get_attribute('datetime')

            if datetime_attr:
                # ISO format: 2025-07-29T14:30:00.000Z
                tweet_date = datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
                # Timezone bilgisini kaldır (naive hale getir)
                return tweet_date.replace(tzinfo=None)

            # Alternatif: title attribute
            title_attr = time_elem.get_attribute('title')
            if title_attr:
                # Farklı formatları dene
                formats = [
                    '%I:%M %p · %b %d, %Y',  # 2:30 PM · Jul 29, 2025
                    '%H:%M · %d %b %Y',  # 14:30 · 29 Jul 2025
                ]

                for fmt in formats:
                    try:
                        return datetime.strptime(title_attr, fmt)
                    except:
                        continue

            return None
        except Exception as e:
            print(f"⚠️ Tarih alma hatası: {e}")
            return None

    def _get_all_interactions(self, tweet_elem):
        """Tüm etkileşim sayılarını al - Düzeltildi"""
        interactions = {
            'likes': 0,
            'retweets': 0,
            'replies': 0,
            'views': 0
        }

        try:
            # Tweet footer'ındaki tüm butonları/linkleri bul - Daha spesifik selector
            action_elements = tweet_elem.find_elements(By.CSS_SELECTOR,
                                                       'div[role="group"] div[role="button"], div[role="group"] a[role="link"]')

            for elem in action_elements:
                try:
                    # Aria-label ve text'i kontrol et
                    aria_label = elem.get_attribute('aria-label') or ''
                    elem_text = elem.text.strip()

                    print(f"🔍 Element: aria-label='{aria_label}', text='{elem_text}'")

                    # Reply/Yanıt - En solda
                    if any(keyword in aria_label.lower() for keyword in ['reply', 'yanıt', 'cevap']):
                        reply_count = self._extract_number(aria_label)
                        if reply_count == 0:
                            reply_count = self._extract_number(elem_text)
                        interactions['replies'] = reply_count
                        print(f"✅ Reply bulundu: {reply_count}")

                    # Retweet - İkinci
                    elif any(keyword in aria_label.lower() for keyword in ['retweet', 'repost', 'yeniden paylaş']):
                        rt_count = self._extract_number(aria_label)
                        if rt_count == 0:
                            rt_count = self._extract_number(elem_text)
                        interactions['retweets'] = rt_count
                        print(f"✅ Retweet bulundu: {rt_count}")

                    # Like/Beğeni - Üçüncü
                    elif any(keyword in aria_label.lower() for keyword in
                             ['like', 'beğen']) and 'unlike' not in aria_label.lower():
                        like_count = self._extract_number(aria_label)
                        if like_count == 0:
                            like_count = self._extract_number(elem_text)
                        interactions['likes'] = like_count
                        print(f"✅ Like bulundu: {like_count}")

                    # View/Görüntülenme - Son veya analytics linki
                    elif self._is_view_element(elem, aria_label, elem_text):
                        view_count = self._extract_number(aria_label)
                        if view_count == 0:
                            view_count = self._extract_number(elem_text)
                        interactions['views'] = view_count
                        print(f"✅ View bulundu: {view_count}")

                except Exception as e:
                    print(f"⚠️ Element işleme hatası: {e}")
                    continue

            # Alternatif yöntem: Specific test-id'ler ile
            if all(v == 0 for v in [interactions['likes'], interactions['retweets'], interactions['replies']]):
                print("🔄 Alternatif yöntem deneniyor...")
                interactions.update(self._get_interactions_alternative(tweet_elem))

            # View sayısı için alternatif yöntem
            if interactions['views'] == 0:
                interactions['views'] = self._get_view_count_alternative(tweet_elem)

            print(f"📊 Final interactions: {interactions}")
            return interactions

        except Exception as e:
            print(f"⚠️ Etkileşim sayıları alınamadı: {e}")
            return interactions

    def _get_interactions_alternative(self, tweet_elem):
        """Alternatif etkileşim alma yöntemi"""
        alt_interactions = {'likes': 0, 'retweets': 0, 'replies': 0}

        try:
            # Data-testid'ler ile dene
            testid_selectors = {
                'replies': ['reply', 'Reply'],
                'retweets': ['retweet', 'Retweet'],
                'likes': ['like', 'Like']
            }

            for interaction_type, testids in testid_selectors.items():
                for testid in testids:
                    try:
                        elem = tweet_elem.find_element(By.CSS_SELECTOR, f'[data-testid="{testid}"]')
                        aria_label = elem.get_attribute('aria-label') or ''
                        count = self._extract_number(aria_label)
                        if count > 0:
                            alt_interactions[interaction_type] = count
                            print(f"✅ Alt yöntem {interaction_type}: {count}")
                            break
                    except:
                        continue

            # Span elementlerini kontrol et
            spans = tweet_elem.find_elements(By.CSS_SELECTOR, 'div[role="group"] span')
            numbers_found = []

            for span in spans:
                text = span.text.strip()
                if text and self._extract_number(text) > 0:
                    numbers_found.append(self._extract_number(text))

            print(f"🔍 Bulunan sayılar: {numbers_found}")

            # Sayıları sıraya göre ata (genellikle: reply, retweet, like sırası)
            if len(numbers_found) >= 3:
                alt_interactions['replies'] = numbers_found[0] if alt_interactions['replies'] == 0 else \
                alt_interactions['replies']
                alt_interactions['retweets'] = numbers_found[1] if alt_interactions['retweets'] == 0 else \
                alt_interactions['retweets']
                alt_interactions['likes'] = numbers_found[2] if alt_interactions['likes'] == 0 else alt_interactions[
                    'likes']

            return alt_interactions

        except Exception as e:
            print(f"⚠️ Alternatif yöntem hatası: {e}")
            return alt_interactions

    def _is_view_element(self, elem, aria_label, elem_text):
        """Element'in view sayısı olup olmadığını kontrol et"""
        # View için anahtar kelimeler
        view_keywords = ['view', 'görüntülenme', 'görüntüleme', 'görünüm']

        # Aria-label kontrolü
        if any(keyword in aria_label.lower() for keyword in view_keywords):
            return True

        # Analytics linki kontrolü
        try:
            analytics_link = elem.find_element(By.CSS_SELECTOR, 'a[href*="analytics"]')
            return True
        except:
            pass

        # Sadece rakam içeren büyük sayılar (muhtemelen view)
        if elem_text and self._extract_number(elem_text) > 1000:
            # Diğer etkileşimlerin rakamlarından farklı mı?
            return True

        return False

    def _get_view_count_alternative(self, tweet_elem):
        """Alternatif view sayısı alma yöntemi"""
        try:
            # Analytics linklerini ara
            analytics_links = tweet_elem.find_elements(By.CSS_SELECTOR, 'a[aria-label*="View"], a[href*="analytics"]')

            for link in analytics_links:
                aria_label = link.get_attribute('aria-label') or ''
                link_text = link.text.strip()

                if 'view' in aria_label.lower() or 'görüntülenme' in aria_label.lower():
                    return self._extract_number(aria_label) or self._extract_number(link_text)

            # Son çare: En büyük sayıyı view olarak kabul et
            all_numbers = []
            elements = tweet_elem.find_elements(By.CSS_SELECTOR, 'div[role="group"] *')

            for elem in elements:
                text = elem.text.strip()
                if text:
                    num = self._extract_number(text)
                    if num > 0:
                        all_numbers.append(num)

            if all_numbers:
                # En büyük sayı muhtemelen view count
                return max(all_numbers)

            return 0

        except:
            return 0

    def _extract_number(self, text):
        """Sayıları çıkar (1.2K -> 1200) - Geliştirildi"""
        if not text:
            return 0

        import re
        # Türkçe ve İngilizce sayı formatları için pattern
        patterns = [
            r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*[KkBbMm]?',  # 1,234 veya 1.2K formatı
            r'(\d+(?:\.\d+)?)\s*[KkBbMm]',  # 1.2K formatı
            r'(\d+(?:,\d{3})*)',  # 1,234 formatı
            r'(\d+)'  # Basit sayı
        ]

        text_clean = str(text).replace(',', '').upper()

        for pattern in patterns:
            numbers = re.findall(pattern, text_clean)
            if numbers:
                try:
                    num_str = numbers[0].replace(',', '').upper()

                    if 'K' in text_clean:
                        return int(float(num_str) * 1000)
                    elif 'M' in text_clean:
                        return int(float(num_str) * 1000000)
                    elif 'B' in text_clean:
                        return int(float(num_str) * 1000000000)
                    else:
                        return int(float(num_str))
                except ValueError:
                    continue

        return 0

    def _get_tweet_url(self, tweet_elem):
        """Tweet URL'sini al"""
        try:
            link_elem = tweet_elem.find_element(By.CSS_SELECTOR, 'a[href*="/status/"]')
            return link_elem.get_attribute('href')
        except:
            return f"https://x.com/status/{int(time.time())}"

    def _calculate_stats(self, tweets, source_type, profile_username, hashtag):
        """İstatistikleri hesapla"""
        if not tweets:
            return {"toplanan_tweet": 0, "durum": "Veri yok"}

        total_likes = sum(t['beğeni'] for t in tweets)
        total_retweets = sum(t['retweet'] for t in tweets)
        total_views = sum(t['görüntülenme'] for t in tweets)
        total_replies = sum(t['yanıt'] for t in tweets)

        # Kaynak bilgisi
        source_info = "Ana Sayfa"
        if hashtag:
            source_info = f"#{hashtag.replace('#', '')}"
        elif profile_username:
            source_info = f"@{profile_username.replace('@', '')}"
        elif source_type == "following":
            source_info = "Following"
        elif source_type == "foryou":
            source_info = "For You"

        return {
            "kaynak": source_info,
            "toplanan_tweet": len(tweets),
            "toplam_beğeni": total_likes,
            "toplam_retweet": total_retweets,
            "toplam_yanıt": total_replies,
            "toplam_görüntülenme": total_views,
            "ortalama_beğeni": total_likes // len(tweets) if tweets else 0,
            "ortalama_görüntülenme": total_views // len(tweets) if tweets else 0,
            "en_popüler_tweet": max(tweets, key=lambda x: x['beğeni'])['tweet'][:100] + '...' if tweets else '',
            "son_güncelleme": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def _create_result_message(self, tweets, stats):
        """Sonuç mesajını oluştur"""
        return f"""🎉 Tweet toplama başarıyla tamamlandı!

📊 **Özet Rapor:**
• Kaynak: {stats['kaynak']}
• Toplanan Tweet: {len(tweets)}
• Toplam Beğeni: {stats['toplam_beğeni']:,}
• Toplam Retweet: {stats['toplam_retweet']:,}
• Toplam Görüntülenme: {stats['toplam_görüntülenme']:,}
• Ortalama Beğeni: {stats['ortalama_beğeni']:,}
• Ortalama Görüntülenme: {stats['ortalama_görüntülenme']:,}

🏆 **En Popüler:** {stats['en_popüler_tweet']}

💾 CSV kaydetmeye hazır!"""

    def save_csv(self):
        """CSV'ye kaydet - Gradio indirme desteği"""
        if not self.tweets_data:
            return "❌ Kaydedilecek veri yok", None

        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            csv_filename = f"x_tweets_advanced_{timestamp}.csv"
            csv_file = Path(csv_filename)

            fieldnames = [
                'zaman_toplama', 'tweet_tarihi', 'tweet', 'yazar', 'yazar_handle',
                'beğeni', 'retweet', 'yanıt', 'görüntülenme', 'url'
            ]

            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.tweets_data)

            message = f"✅ Gelişmiş CSV hazırlandı: {csv_filename}\n📊 {len(self.tweets_data)} tweet, 10 kolon veri\n💾 Aşağıdaki butondan indirebilirsiniz!"

            return message, str(csv_file)

        except Exception as e:
            return f"❌ CSV kaydetme hatası: {e}", None

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
scraper = AdvancedXScraper()


# Gradio fonksiyonları
def setup_browser():
    return scraper.setup_driver()


def login(username, password):
    if not username or not password:
        return "❌ Kullanıcı adı ve şifre gerekli!"

    clean_username = username.replace('@', '')
    return scraper.login_x(clean_username, password)


def scrape_tweets_handler(tweet_count, source_type, profile_username, hashtag, days_filter):
    return scraper.scrape_tweets(
        max_tweets=int(tweet_count),
        source_type=source_type,
        profile_username=profile_username,
        hashtag=hashtag,
        days_filter=int(days_filter) if days_filter else 0
    )


def save_data():
    message, file_path = scraper.save_csv()
    return message, file_path


def close_browser():
    return scraper.close()


# Gelişmiş Gradio UI
with gr.Blocks(title="🚀 X Scraper - Gelişmiş Versiyon", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🚀 X (Twitter) Scraper - Gelişmiş Tam Özellikli Versiyon")
    gr.Markdown(
        "✨ **Tüm özellikler:** Tweet tarihleri, Profil scraping, Hashtag arama, Zaman filtreleme, Gelişmiş view tracking")

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

            gr.Markdown("### 📊 3. Scraping Ayarları")

            with gr.Row():
                tweet_count = gr.Number(
                    label="Tweet Sayısı",
                    value=20,
                    minimum=5,
                    maximum=200,
                    info="5-200 arası"
                )
                days_filter = gr.Number(
                    label="Zaman Filtresi (Gün)",
                    value=0,
                    minimum=0,
                    maximum=365,
                    info="0=Tümü, 7=Son hafta"
                )

            source_type = gr.Radio(
                label="📍 Kaynak Seçimi",
                choices=["home", "following", "foryou"],
                value="home",
                info="Ana sayfa sekmesi seçin"
            )

            profile_username = gr.Textbox(
                label="👤 Profil Username (Opsiyonel)",
                placeholder="elonmusk",
                info="Belirli bir kullanıcının tweetleri için"
            )

            hashtag = gr.Textbox(
                label="🏷️ Hashtag Arama (Opsiyonel)",
                placeholder="#python veya python",
                info="Hashtag ile arama yapmak için"
            )

            scrape_btn = gr.Button("🚀 Tweet Topla", variant="primary", size="lg")

            gr.Markdown("### 💾 4. Kaydet & Kapat")
            with gr.Row():
                save_btn = gr.Button("💾 CSV Hazırla", variant="secondary")
                close_btn = gr.Button("❌ Kapat", variant="secondary")

            # CSV İndirme Bölümü - YENİ
            download_file = gr.File(
                label="📥 CSV İndirme",
                visible=False,
                interactive=False
            )

        with gr.Column(scale=2):
            scrape_output = gr.Textbox(
                label="📤 İşlem Sonuçları",
                lines=15,
                show_copy_button=True
            )

            stats = gr.JSON(
                label="📊 Detaylı İstatistikler",
                value={"toplanan_tweet": 0, "durum": "Henüz veri yok"}
            )

    gr.Markdown("### 📋 Toplanan Tweet'ler (Tam Veri)")
    tweet_table = gr.Dataframe(
        label="🐦 Tweet Listesi - Gelişmiş",
        headers=["Tweet Tarihi", "Tweet", "Yazar", "Beğeni", "RT", "Yanıt", "Görüntülenme"],
        wrap=True,
        max_height=400
    )

    # Event handlers
    setup_btn.click(setup_browser, outputs=[setup_output])
    login_btn.click(login, inputs=[username, password], outputs=[login_output])
    scrape_btn.click(
        scrape_tweets_handler,
        inputs=[tweet_count, source_type, profile_username, hashtag, days_filter],
        outputs=[scrape_output, tweet_table, stats]
    )


    # CSV kaydetme ve indirme - Güncellenmiş
    def handle_save_and_download(file_obj, message):
        if file_obj:
            return message, gr.File(value=file_obj, visible=True)
        else:
            return message, gr.File(visible=False)


    save_btn.click(
        save_data,
        outputs=[scrape_output, download_file]
    ).then(
        lambda file_path: gr.File(value=file_path, visible=True) if file_path else gr.File(visible=False),
        inputs=[download_file],
        outputs=[download_file]
    )

    close_btn.click(close_browser, outputs=[scrape_output])

    # Kullanım örnekleri
    with gr.Accordion("📖 Kullanım Örnekleri", open=False):
        gr.Markdown("""
        ### 🎯 Örnek Kullanımlar:

        **1. Ana Sayfa Timeline:**
        - Kaynak: `home` 
        - Profil/Hashtag: Boş bırak

        **2. Belirli Kullanıcı:**
        - Kaynak: `home`
        - Profil: `elonmusk` (@ olmadan)

        **3. Hashtag Arama:**
        - Kaynak: `home`
        - Hashtag: `#python` veya `python`

        **4. Zaman Filtresi:**
        - Son 7 gün: `7`
        - Son ay: `30`
        - Tümü: `0`

        **5. Following Timeline:**
        - Kaynak: `following` 
        - Manuel olarak Following tab'ına geçin

        **6. Kombine Örnek:**
        - Tweet Sayısı: `50`
        - Zaman Filtresi: `7` (son hafta)
        - Profil: `openai`
        - Sonuç: OpenAI'ın son 7 gündeki 50 tweeti
        """)

if __name__ == "__main__":
    print("🚀 Gelişmiş X Scraper başlatılıyor...")
    print("✨ Özellikler: Tweet tarihleri, Profil scraping, Hashtag arama, Zaman filtreleme")
    print("📱 Otomatik ChromeDriver yönetimi aktif")
    print("👁️ Gelişmiş görüntülenme sayısı tracking")
    app.launch(server_name="127.0.0.1", server_port=7864, inbrowser=True)