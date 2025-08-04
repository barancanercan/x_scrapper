#!/usr/bin/env python3
"""
X Scraper - Streamlit Versiyonu
- Excel ve CSV export
- Modern UI
- Streamlit deployment ready
"""

import time
import csv
import json
import re
import io
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import streamlit as st


class AdvancedXScraper:
    def __init__(self):
        self.driver = None
        self.is_logged_in = False
        self.tweets_data = []

    def setup_driver(self):
        """Chrome driver kurulum - Streamlit Cloud için optimize edilmiş"""
        try:
            options = Options()

            # Streamlit Cloud için gerekli options
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-web-security")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--remote-debugging-port=9222")
            options.add_argument(
                "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option("detach", True)

            # Streamlit Cloud için ChromeDriver path detection
            import shutil
            import os

            # ChromeDriver'ı farklı yollardan bul
            chrome_driver_paths = [
                "/usr/bin/chromedriver",
                "/usr/local/bin/chromedriver",
                "/opt/chrome/chromedriver",
                shutil.which("chromedriver")
            ]

            chrome_driver_path = None
            for path in chrome_driver_paths:
                if path and os.path.exists(path):
                    chrome_driver_path = path
                    break

            if chrome_driver_path:
                # Manuel service path
                service = Service(chrome_driver_path)
                st.info(f"✅ ChromeDriver bulundu: {chrome_driver_path}")
            else:
                # WebDriverManager fallback
                try:
                    service = Service(ChromeDriverManager().install())
                    st.info("✅ ChromeDriver WebDriverManager ile yüklendi")
                except:
                    return False, "❌ ChromeDriver kurulamadı. Lütfen sistem yöneticisiyle iletişime geçin."

            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            # Test connection
            self.driver.get("https://httpbin.org/user-agent")

            return True, "✅ Chrome driver başarıyla kuruldu ve test edildi!"

        except Exception as e:
            return False, f"❌ Driver hatası: {e}\n💡 Çözüm: Streamlit uygulamasını yeniden başlatın"

    def login_x(self, username, password):
        """X'e giriş yap"""
        if not self.driver:
            return False, "❌ Önce tarayıcıyı hazırlayın"

        try:
            with st.spinner("🔐 X'e giriş yapılıyor..."):
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
                    return False, "❌ Kullanıcı adı alanı bulunamadı"

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
                    return False, "❌ Şifre alanı bulunamadı"

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
                    return True, f"✅ X'e başarıyla giriş yapıldı!"
                else:
                    return False, f"❌ Giriş doğrulanamadı."

        except Exception as e:
            return False, f"❌ Giriş hatası: {e}"

    def scrape_tweets(self, max_tweets=20, source_type="home", profile_username="", hashtag="", days_filter=0):
        """Gelişmiş tweet toplama"""
        if not self.is_logged_in:
            return False, "❌ Önce X'e giriş yapın", [], {}

        try:
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.text(f"📱 {max_tweets} tweet toplanıyor...")

            # URL belirleme
            url = self._get_scraping_url(source_type, profile_username, hashtag)
            self.driver.get(url)
            time.sleep(5)

            tweets = []
            scroll_count = 0
            max_scrolls = 15
            cutoff_date = None

            if days_filter > 0:
                cutoff_date = datetime.now() - timedelta(days=days_filter)

            while len(tweets) < max_tweets and scroll_count < max_scrolls:
                # Progress güncelle
                progress = min((len(tweets) / max_tweets) * 0.8 + (scroll_count / max_scrolls) * 0.2, 0.95)
                progress_bar.progress(progress)
                status_text.text(f"📜 Scroll {scroll_count + 1}/{max_scrolls} - {len(tweets)} tweet toplandı")

                # Tweet elementlerini bul
                tweet_elements = self.driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')

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

                        # Yazar bilgisi
                        author_info = self._get_author_info(tweet_elem)

                        # Tweet tarihi
                        tweet_date = self._get_tweet_date(tweet_elem)

                        # Zaman filtresi kontrolü
                        if cutoff_date and tweet_date:
                            if tweet_date < cutoff_date:
                                continue

                        # Etkileşim sayıları
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

                    except Exception as e:
                        continue

                # Scroll
                if len(tweets) < max_tweets:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(4)
                    scroll_count += 1

            # Progress tamamla
            progress_bar.progress(1.0)
            status_text.text("✅ Tweet toplama tamamlandı!")

            self.tweets_data = tweets

            # İstatistikler
            stats = self._calculate_stats(tweets, source_type, profile_username, hashtag)

            return True, f"✅ {len(tweets)} tweet başarıyla toplandı!", tweets, stats

        except Exception as e:
            return False, f"❌ Scraping hatası: {e}", [], {}

    def _get_scraping_url(self, source_type, profile_username, hashtag):
        """Scraping URL'sini belirle"""
        base_url = "https://x.com"

        if hashtag:
            hashtag_clean = hashtag.replace('#', '').strip()
            return f"{base_url}/search?q=%23{hashtag_clean}&src=typed_query&f=live"

        if profile_username:
            username_clean = profile_username.replace('@', '').strip()
            return f"{base_url}/{username_clean}"

        return f"{base_url}/home"

    def _get_author_info(self, tweet_elem):
        """Yazar bilgilerini al"""
        try:
            author_elem = tweet_elem.find_element(By.CSS_SELECTOR, '[data-testid="User-Name"]')
            author_text = author_elem.text.strip()

            lines = author_text.split('\n')
            name = lines[0] if lines else 'Bilinmiyor'
            handle = lines[1].replace('@', '') if len(lines) > 1 and '@' in lines[1] else 'bilinmiyor'

            return {'name': name, 'handle': handle}
        except:
            return {'name': 'Bilinmiyor', 'handle': 'bilinmiyor'}

    def _get_tweet_date(self, tweet_elem):
        """Tweet tarihini al"""
        try:
            time_elem = tweet_elem.find_element(By.CSS_SELECTOR, 'time')
            datetime_attr = time_elem.get_attribute('datetime')

            if datetime_attr:
                tweet_date = datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
                return tweet_date.replace(tzinfo=None)

            return None
        except:
            return None

    def _get_all_interactions(self, tweet_elem):
        """Tüm etkileşim sayılarını al"""
        interactions = {
            'likes': 0,
            'retweets': 0,
            'replies': 0,
            'views': 0
        }

        try:
            action_elements = tweet_elem.find_elements(By.CSS_SELECTOR,
                                                       'div[role="group"] div[role="button"], div[role="group"] a[role="link"]')

            for elem in action_elements:
                try:
                    aria_label = elem.get_attribute('aria-label') or ''
                    elem_text = elem.text.strip()

                    if any(keyword in aria_label.lower() for keyword in ['reply', 'yanıt', 'cevap']):
                        interactions['replies'] = self._extract_number(aria_label) or self._extract_number(elem_text)

                    elif any(keyword in aria_label.lower() for keyword in ['retweet', 'repost', 'yeniden paylaş']):
                        interactions['retweets'] = self._extract_number(aria_label) or self._extract_number(elem_text)

                    elif any(keyword in aria_label.lower() for keyword in
                             ['like', 'beğen']) and 'unlike' not in aria_label.lower():
                        interactions['likes'] = self._extract_number(aria_label) or self._extract_number(elem_text)

                    elif self._is_view_element(elem, aria_label, elem_text):
                        interactions['views'] = self._extract_number(aria_label) or self._extract_number(elem_text)

                except:
                    continue

            return interactions

        except:
            return interactions

    def _is_view_element(self, elem, aria_label, elem_text):
        """Element'in view sayısı olup olmadığını kontrol et"""
        view_keywords = ['view', 'görüntülenme', 'görüntüleme', 'görünüm']

        if any(keyword in aria_label.lower() for keyword in view_keywords):
            return True

        try:
            analytics_link = elem.find_element(By.CSS_SELECTOR, 'a[href*="analytics"]')
            return True
        except:
            pass

        if elem_text and self._extract_number(elem_text) > 1000:
            return True

        return False

    def _extract_number(self, text):
        """Sayıları çıkar (1.2K -> 1200)"""
        if not text:
            return 0

        import re
        text_clean = str(text).replace(',', '').upper()

        patterns = [
            r'(\d+(?:\.\d+)?)\s*[KkBbMm]',
            r'(\d+(?:,\d{3})*)',
            r'(\d+)'
        ]

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

    def save_to_csv(self):
        """CSV olarak kaydet"""
        if not self.tweets_data:
            return None, "❌ Kaydedilecek veri yok"

        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            # DataFrame oluştur
            df = pd.DataFrame(self.tweets_data)

            # CSV buffer
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, encoding='utf-8')

            return csv_buffer.getvalue(), f"x_tweets_{timestamp}.csv"

        except Exception as e:
            return None, f"❌ CSV oluşturma hatası: {e}"

    def save_to_excel(self):
        """Excel olarak kaydet"""
        if not self.tweets_data:
            return None, "❌ Kaydedilecek veri yok"

        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            # DataFrame oluştur
            df = pd.DataFrame(self.tweets_data)

            # Excel buffer
            excel_buffer = io.BytesIO()

            # Excel writer ile gelişmiş formatting
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Tweets', index=False)

                # Worksheet al
                worksheet = writer.sheets['Tweets']

                # Kolon genişliklerini ayarla
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter

                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass

                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width

                # Header stil
                for cell in worksheet[1]:
                    cell.font = cell.font.copy(bold=True)

            excel_buffer.seek(0)
            return excel_buffer.getvalue(), f"x_tweets_{timestamp}.xlsx"

        except Exception as e:
            return None, f"❌ Excel oluşturma hatası: {e}"

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


# Streamlit App
def main():
    st.set_page_config(
        page_title="🚀 X Scraper",
        page_icon="🐦",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # CSS stil
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #1DA1F2, #14171A);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1DA1F2;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .error-box {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="main-header">
        <h1 style="color: white; margin: 0;">🚀 X (Twitter) Scraper - Streamlit Edition</h1>
        <p style="color: #e1e8ed; margin: 0;">Excel & CSV Export | Gelişmiş Tweet Toplama | Zaman Filtreleme</p>
    </div>
    """, unsafe_allow_html=True)

    # Session state
    if 'scraper' not in st.session_state:
        st.session_state.scraper = AdvancedXScraper()
    if 'is_setup' not in st.session_state:
        st.session_state.is_setup = False
    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = False
    if 'tweets_data' not in st.session_state:
        st.session_state.tweets_data = []
    if 'stats' not in st.session_state:
        st.session_state.stats = {}

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Kontrol Paneli")

        # 1. Kurulum
        st.subheader("🔧 1. Kurulum")
        if st.button("🚀 Tarayıcı Hazırla", type="primary", use_container_width=True):
            with st.spinner("Tarayıcı hazırlanıyor..."):
                success, message = st.session_state.scraper.setup_driver()
                if success:
                    st.session_state.is_setup = True
                    st.success(message)
                else:
                    st.error(message)

        # Status indicator
        status_color = "🟢" if st.session_state.is_setup else "🔴"
        st.write(f"{status_color} Tarayıcı Durumu: {'Hazır' if st.session_state.is_setup else 'Kurulum Gerekli'}")

        st.divider()

        # 2. Login
        st.subheader("🔐 2. X Giriş")
        username = st.text_input("👤 X Kullanıcı Adı", placeholder="kullanici_adi (@ olmadan)")
        password = st.text_input("🔒 X Şifre", type="password")

        if st.button("🔐 X'e Giriş Yap", type="primary", use_container_width=True):
            if not st.session_state.is_setup:
                st.error("❌ Önce tarayıcıyı hazırlayın!")
            elif not username or not password:
                st.error("❌ Kullanıcı adı ve şifre gerekli!")
            else:
                clean_username = username.replace('@', '')
                success, message = st.session_state.scraper.login_x(clean_username, password)
                if success:
                    st.session_state.is_logged_in = True
                    st.success(message)
                else:
                    st.error(message)

        # Login status
        login_color = "🟢" if st.session_state.is_logged_in else "🔴"
        st.write(f"{login_color} Giriş Durumu: {'Başarılı' if st.session_state.is_logged_in else 'Giriş Gerekli'}")

        st.divider()

        # 3. Scraping Ayarları
        st.subheader("📊 3. Scraping Ayarları")

        col1, col2 = st.columns(2)
        with col1:
            tweet_count = st.number_input("Tweet Sayısı", min_value=5, max_value=200, value=20, step=5)
        with col2:
            days_filter = st.number_input("Zaman Filtresi (Gün)", min_value=0, max_value=365, value=0, help="0=Tümü")

        source_type = st.selectbox(
            "📍 Kaynak Seçimi",
            ["home", "following", "foryou"],
            help="Ana sayfa sekmesi seçin"
        )

        profile_username = st.text_input(
            "👤 Profil Username (Opsiyonel)",
            placeholder="elonmusk",
            help="Belirli bir kullanıcının tweetleri için"
        )

        hashtag = st.text_input(
            "🏷️ Hashtag Arama (Opsiyonel)",
            placeholder="#python veya python",
            help="Hashtag ile arama yapmak için"
        )

        # Scrape button
        if st.button("🚀 Tweet Topla", type="primary", use_container_width=True):
            if not st.session_state.is_logged_in:
                st.error("❌ Önce X'e giriş yapın!")
            else:
                success, message, tweets, stats = st.session_state.scraper.scrape_tweets(
                    max_tweets=tweet_count,
                    source_type=source_type,
                    profile_username=profile_username,
                    hashtag=hashtag,
                    days_filter=days_filter
                )

                if success:
                    st.session_state.tweets_data = tweets
                    st.session_state.stats = stats
                    st.success(message)
                    st.rerun()  # Sayfayı yenile
                else:
                    st.error(message)

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📊 Toplanan Tweetler")

        if st.session_state.tweets_data:
            # DataFrame göster
            df = pd.DataFrame(st.session_state.tweets_data)

            # Display columns
            display_df = df[
                ['tweet_tarihi', 'tweet', 'yazar_handle', 'beğeni', 'retweet', 'yanıt', 'görüntülenme']].copy()
            display_df.columns = ['Tarih', 'Tweet', 'Yazar', 'Beğeni', 'RT', 'Yanıt', 'Görüntülenme']

            # Tweet column'u kısalt
            display_df['Tweet'] = display_df['Tweet'].apply(lambda x: x[:80] + '...' if len(x) > 80 else x)

            st.dataframe(
                display_df,
                use_container_width=True,
                height=400,
                column_config={
                    "Beğeni": st.column_config.NumberColumn(format="%d"),
                    "RT": st.column_config.NumberColumn(format="%d"),
                    "Yanıt": st.column_config.NumberColumn(format="%d"),
                    "Görüntülenme": st.column_config.NumberColumn(format="%d"),
                }
            )

            # Export butonları
            st.subheader("💾 Export Seçenekleri")
            col_csv, col_excel = st.columns(2)

            with col_csv:
                csv_data, csv_filename = st.session_state.scraper.save_to_csv()
                if csv_data:
                    st.download_button(
                        label="📄 CSV İndir",
                        data=csv_data,
                        file_name=csv_filename,
                        mime="text/csv",
                        type="primary",
                        use_container_width=True
                    )

            with col_excel:
                excel_data, excel_filename = st.session_state.scraper.save_to_excel()
                if excel_data:
                    st.download_button(
                        label="📊 Excel İndir",
                        data=excel_data,
                        file_name=excel_filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        type="primary",
                        use_container_width=True
                    )

        else:
            st.info("🔍 Henüz tweet toplanmamış. Sidebar'dan scraping başlatın.")

    with col2:
        st.subheader("📈 İstatistikler")

        if st.session_state.stats:
            stats = st.session_state.stats

            # Metrics
            st.metric("📱 Toplanan Tweet", stats.get('toplanan_tweet', 0))
            st.metric("❤️ Toplam Beğeni", f"{stats.get('toplam_beğeni', 0):,}")
            st.metric("🔄 Toplam Retweet", f"{stats.get('toplam_retweet', 0):,}")
            st.metric("👁️ Toplam Görüntülenme", f"{stats.get('toplam_görüntülenme', 0):,}")

            st.divider()

            # Ortalamalar
            st.write("**📊 Ortalamalar**")
            st.write(f"• Beğeni: {stats.get('ortalama_beğeni', 0):,}")
            st.write(f"• Görüntülenme: {stats.get('ortalama_görüntülenme', 0):,}")

            st.divider()

            # Kaynak bilgisi
            st.write("**📍 Kaynak**")
            st.write(f"• {stats.get('kaynak', 'Bilinmiyor')}")

            # En popüler tweet
            if stats.get('en_popüler_tweet'):
                st.write("**🏆 En Popüler Tweet**")
                st.write(f"*{stats.get('en_popüler_tweet')}*")

        else:
            st.info("📊 İstatistikler scraping sonrası görüntülenecek.")

        st.divider()

        # Kullanım örnekleri
        with st.expander("📖 Kullanım Örnekleri"):
            st.write("""
            **🎯 Örnek Kullanımlar:**

            **1. Ana Sayfa Timeline:**
            - Kaynak: `home`
            - Profil/Hashtag: Boş bırak

            **2. Belirli Kullanıcı:**
            - Kaynak: `home`
            - Profil: `elonmusk`

            **3. Hashtag Arama:**
            - Hashtag: `#python`

            **4. Zaman Filtresi:**
            - Son 7 gün: `7`
            - Son ay: `30`
            - Tümü: `0`
            """)

    # Footer
    st.divider()

    # Sistem durumu
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**🔧 Sistem Durumu**")
        st.write(f"• Tarayıcı: {'✅' if st.session_state.is_setup else '❌'}")
        st.write(f"• X Giriş: {'✅' if st.session_state.is_logged_in else '❌'}")

    with col2:
        st.write("**📊 Veri Durumu**")
        st.write(f"• Tweet Sayısı: {len(st.session_state.tweets_data)}")
        st.write(f"• Export Hazır: {'✅' if st.session_state.tweets_data else '❌'}")

    with col3:
        if st.button("❌ Tarayıcıyı Kapat", type="secondary"):
            message = st.session_state.scraper.close()
            st.session_state.is_setup = False
            st.session_state.is_logged_in = False
            st.info(message)


if __name__ == "__main__":
    main()