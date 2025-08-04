#!/usr/bin/env python3
"""
Gelişmiş X Scraper - Excel Destekli Tam Özellikli Versiyon
- View sayıları (düzeltildi)
- Tweet tarihleri
- Following/For You seçenekleri
- Profil bazlı scraping
- Zaman filtreleme
- Hashtag arama
- CSV ve Excel export/import desteği
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
import pandas as pd
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows


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

    def load_excel_data(self, excel_file):
        """Excel dosyasından veri yükle"""
        try:
            if excel_file is None:
                return "❌ Excel dosyası seçilmedi", [], {}

            # Excel dosyasını oku
            df = pd.read_excel(excel_file.name)
            print(f"📊 Excel dosyası yüklendi: {len(df)} satır")

            # Gerekli kolonları kontrol et
            required_columns = ['tweet', 'yazar', 'yazar_handle', 'beğeni', 'retweet', 'yanıt', 'görüntülenme']
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                return f"❌ Eksik kolonlar: {missing_columns}\n💡 Gerekli kolonlar: {required_columns}", [], {}

            # Veriyi temizle ve dönüştür
            df = df.fillna('')  # NaN değerleri boş string yap

            # Sayısal kolonları integer'a dönüştür
            numeric_columns = ['beğeni', 'retweet', 'yanıt', 'görüntülenme']
            for col in numeric_columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

            # Tweet verilerini liste formatına dönüştür
            tweets_data = []
            for _, row in df.iterrows():
                tweet_data = {
                    'zaman_toplama': row.get('zaman_toplama', datetime.now().strftime('%Y-%m-%d %H:%M')),
                    'tweet_tarihi': row.get('tweet_tarihi', 'Bilinmiyor'),
                    'tweet': str(row['tweet'])[:500],
                    'yazar': str(row['yazar']),
                    'yazar_handle': str(row['yazar_handle']),
                    'beğeni': int(row['beğeni']),
                    'retweet': int(row['retweet']),
                    'yanıt': int(row['yanıt']),
                    'görüntülenme': int(row['görüntülenme']),
                    'url': row.get('url', '')
                }
                tweets_data.append(tweet_data)

            self.tweets_data = tweets_data

            # Tablo verisi oluştur
            table_data = [[
                t['tweet_tarihi'],
                t['tweet'][:60] + '...' if len(t['tweet']) > 60 else t['tweet'],
                f"@{t['yazar_handle']}",
                t['beğeni'],
                t['retweet'],
                t['yanıt'],
                t['görüntülenme']
            ] for t in tweets_data]

            # İstatistikleri hesapla
            stats = self._calculate_stats_from_data(tweets_data, "Excel Dosyası")

            message = f"""✅ Excel dosyası başarıyla yüklendi!

📊 **Yüklenen Veri:**
• Toplam Tweet: {len(tweets_data)}
• Toplam Beğeni: {stats['toplam_beğeni']:,}
• Toplam Görüntülenme: {stats['toplam_görüntülenme']:,}
• Ortalama Beğeni: {stats['ortalama_beğeni']:,}

💾 Artık CSV ve Excel olarak indirebilirsiniz!"""

            return message, table_data, stats

        except Exception as e:
            return f"❌ Excel yükleme hatası: {e}", [], {}

    def scrape_tweets(self, max_tweets=20, source_type="home", profile_username="", hashtag="", days_filter=0):
        """Gelişmiş tweet toplama"""
        if not self.is_logged_in:
            return "❌ Önce X'e giriş yapın", [], {}

        try:
            print(f"📱 {max_tweets} tweet toplanıyor...")

            # Global sayaçları sıfırla
            self._empty_scroll_count = 0
            self._total_old_tweets = 0

            # URL belirleme
            url = self._get_scraping_url(source_type, profile_username, hashtag)
            print(f"🔗 Gidilen URL: {url}")

            self.driver.get(url)
            time.sleep(5)

            tweets = []
            scroll_count = 0
            max_scrolls = 15
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
                            print(
                                f"✅ Tweet eklendi: @{author_info['handle']} - {interactions['likes']} ♥️, {interactions['views']} 👁️")

                    except Exception as e:
                        print(f"⚠️ Tweet işleme hatası: {e}")
                        continue

                # Scroll
                if len(tweets) < max_tweets:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(4)
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

    def save_csv(self):
        """CSV'ye kaydet"""
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

            message = f"✅ CSV hazırlandı: {csv_filename}\n📊 {len(self.tweets_data)} tweet, 10 kolon veri\n💾 Aşağıdaki butondan indirebilirsiniz!"

            return message, str(csv_file)

        except Exception as e:
            return f"❌ CSV kaydetme hatası: {e}", None

    def save_excel(self):
        """Excel'e kaydet - Gelişmiş formatting ile"""
        if not self.tweets_data:
            return "❌ Kaydedilecek veri yok", None

        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            excel_filename = f"x_tweets_advanced_{timestamp}.xlsx"
            excel_file = Path(excel_filename)

            # DataFrame oluştur
            df = pd.DataFrame(self.tweets_data)

            # Kolon sıralaması
            column_order = [
                'zaman_toplama', 'tweet_tarihi', 'tweet', 'yazar', 'yazar_handle',
                'beğeni', 'retweet', 'yanıt', 'görüntülenme', 'url'
            ]
            df = df[column_order]

            # Excel'e yaz
            with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
                # Ana veri sayfası
                df.to_excel(writer, sheet_name='Tweet_Verileri', index=False)

                # İstatistik sayfası
                stats = self._calculate_stats_from_data(self.tweets_data, "Excel Export")
                stats_df = pd.DataFrame([
                    ['Toplam Tweet', len(self.tweets_data)],
                    ['Toplam Beğeni', stats['toplam_beğeni']],
                    ['Toplam Retweet', stats['toplam_retweet']],
                    ['Toplam Yanıt', stats['toplam_yanıt']],
                    ['Toplam Görüntülenme', stats['toplam_görüntülenme']],
                    ['Ortalama Beğeni', stats['ortalama_beğeni']],
                    ['Ortalama Görüntülenme', stats['ortalama_görüntülenme']],
                    ['Oluşturulma Tarihi', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
                ], columns=['Metrik', 'Değer'])

                stats_df.to_excel(writer, sheet_name='İstatistikler', index=False)

                # Formatting
                workbook = writer.book
                worksheet = writer.sheets['Tweet_Verileri']

                # Header styling
                header_font = Font(bold=True, color="FFFFFF")
                header_fill = PatternFill(start_color="1DA1F2", end_color="1DA1F2", fill_type="solid")

                for cell in worksheet[1]:
                    cell.font = header_font
                    cell.fill = header_fill
                    cell.alignment = Alignment(horizontal="center")

                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter

                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass

                    adjusted_width = min(max_length + 2, 50)  # Max 50 karakter
                    worksheet.column_dimensions[column_letter].width = adjusted_width

                # Tweet kolonunu daha geniş yap
                worksheet.column_dimensions['C'].width = 60  # Tweet kolonu

            message = f"✅ Excel hazırlandı: {excel_filename}\n📊 {len(self.tweets_data)} tweet + İstatistikler\n🎨 Gelişmiş formatting ile\n💾 Aşağıdaki butondan indirebilirsiniz!"

            return message, str(excel_file)

        except Exception as e:
            return f"❌ Excel kaydetme hatası: {e}", None

    def _get_scraping_url(self, source_type, profile_username, hashtag):
        """Scraping URL'sini belirle"""
        base_url = "https://x.com"

        if hashtag:
            hashtag_clean = hashtag.replace('#', '').strip()
            return f"{base_url}/search?q=%23{hashtag_clean}&src=typed_query&f=live"

        if profile_username:
            username_clean = profile_username.replace('@', '').strip()
            return f"{base_url}/{username_clean}"

        if source_type == "following":
            return f"{base_url}/home"
        elif source_type == "foryou":
            return f"{base_url}/home"
        else:
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

            title_attr = time_elem.get_attribute('title')
            if title_attr:
                formats = [
                    '%I:%M %p · %b %d, %Y',
                    '%H:%M · %d %b %Y',
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
                        reply_count = self._extract_number(aria_label)
                        if reply_count == 0:
                            reply_count = self._extract_number(elem_text)
                        interactions['replies'] = reply_count

                    elif any(keyword in aria_label.lower() for keyword in ['retweet', 'repost', 'yeniden paylaş']):
                        rt_count = self._extract_number(aria_label)
                        if rt_count == 0:
                            rt_count = self._extract_number(elem_text)
                        interactions['retweets'] = rt_count

                    elif any(keyword in aria_label.lower() for keyword in
                             ['like', 'beğen']) and 'unlike' not in aria_label.lower():
                        like_count = self._extract_number(aria_label)
                        if like_count == 0:
                            like_count = self._extract_number(elem_text)
                        interactions['likes'] = like_count

                    elif self._is_view_element(elem, aria_label, elem_text):
                        view_count = self._extract_number(aria_label)
                        if view_count == 0:
                            view_count = self._extract_number(elem_text)
                        interactions['views'] = view_count

                except Exception as e:
                    continue

            if all(v == 0 for v in [interactions['likes'], interactions['retweets'], interactions['replies']]):
                interactions.update(self._get_interactions_alternative(tweet_elem))

            if interactions['views'] == 0:
                interactions['views'] = self._get_view_count_alternative(tweet_elem)

            return interactions

        except Exception as e:
            print(f"⚠️ Etkileşim sayıları alınamadı: {e}")
            return interactions

    def _get_interactions_alternative(self, tweet_elem):
        """Alternatif etkileşim alma yöntemi"""
        alt_interactions = {'likes': 0, 'retweets': 0, 'replies': 0}

        try:
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
                            break
                    except:
                        continue

            return alt_interactions

        except Exception as e:
            return alt_interactions

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

    def _get_view_count_alternative(self, tweet_elem):
        """Alternatif view sayısı alma yöntemi"""
        try:
            analytics_links = tweet_elem.find_elements(By.CSS_SELECTOR, 'a[aria-label*="View"], a[href*="analytics"]')

            for link in analytics_links:
                aria_label = link.get_attribute('aria-label') or ''
                link_text = link.text.strip()

                if 'view' in aria_label.lower() or 'görüntülenme' in aria_label.lower():
                    return self._extract_number(aria_label) or self._extract_number(link_text)

            return 0

        except:
            return 0

    def _extract_number(self, text):
        """Sayıları çıkar (1.2K -> 1200)"""
        if not text:
            return 0

        import re
        patterns = [
            r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*[KkBbMm]?',
            r'(\d+(?:\.\d+)?)\s*[KkBbMm]',
            r'(\d+(?:,\d{3})*)',
            r'(\d+)'
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

        return self._calculate_stats_from_data(tweets, self._get_source_info(source_type, profile_username, hashtag))

    def _calculate_stats_from_data(self, tweets, source_info):
        """Veriden istatistik hesapla"""
        if not tweets:
            return {"toplanan_tweet": 0, "durum": "Veri yok"}

        total_likes = sum(t['beğeni'] for t in tweets)
        total_retweets = sum(t['retweet'] for t in tweets)
        total_views = sum(t['görüntülenme'] for t in tweets)
        total_replies = sum(t['yanıt'] for t in tweets)

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

    def _get_source_info(self, source_type, profile_username, hashtag):
        """Kaynak bilgisini al"""
        if hashtag:
            return f"#{hashtag.replace('#', '')}"
        elif profile_username:
            return f"@{profile_username.replace('@', '')}"
        elif source_type == "following":
            return "Following"
        elif source_type == "foryou":
            return "For You"
        else:
            return "Ana Sayfa"

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

💾 CSV ve Excel kaydetmeye hazır!"""

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


def load_excel_handler(excel_file):
    return scraper.load_excel_data(excel_file)


def scrape_tweets_handler(tweet_count, source_type, profile_username, hashtag, days_filter):
    return scraper.scrape_tweets(
        max_tweets=int(tweet_count),
        source_type=source_type,
        profile_username=profile_username,
        hashtag=hashtag,
        days_filter=int(days_filter) if days_filter else 0
    )


def save_csv_data():
    message, file_path = scraper.save_csv()
    return message, file_path


def save_excel_data():
    message, file_path = scraper.save_excel()
    return message, file_path


def close_browser():
    return scraper.close()


# Excel Destekli Gelişmiş Gradio UI
with gr.Blocks(title="🚀 X Scraper - Excel Destekli Versiyon", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🚀 X (Twitter) Scraper - Excel Destekli Gelişmiş Versiyon")
    gr.Markdown("✨ **Yeni Özellikler:** Excel import/export, Gelişmiş formatting, İstatistik sayfası")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🔧 1. Kurulum")
            setup_btn = gr.Button("🚀 Tarayıcı Hazırla", variant="primary", size="lg")
            setup_output = gr.Textbox(label="Kurulum Durumu", lines=3)

            gr.Markdown("### 📊 2. Excel Veri Yükleme (Opsiyonel)")
            excel_upload = gr.File(
                label="📁 Excel Dosyası Yükle",
                file_types=[".xlsx", ".xls"],
                type="filepath"
            )
            load_excel_btn = gr.Button("📊 Excel Verilerini Yükle", variant="secondary", size="lg")

            gr.Markdown("### 🔐 3. X Giriş")
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

            gr.Markdown("### 📊 4. Scraping Ayarları")

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

            gr.Markdown("### 💾 5. Kaydet & Kapat")
            with gr.Row():
                save_csv_btn = gr.Button("💾 CSV Hazırla", variant="secondary")
                save_excel_btn = gr.Button("📊 Excel Hazırla", variant="secondary")

            close_btn = gr.Button("❌ Kapat", variant="secondary")

            # Dosya İndirme Bölümleri
            gr.Markdown("### 📥 Dosya İndirme")
            csv_download_file = gr.File(
                label="📄 CSV İndirme",
                visible=False,
                interactive=False
            )

            excel_download_file = gr.File(
                label="📊 Excel İndirme",
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
        label="🐦 Tweet Listesi - Excel Destekli",
        headers=["Tweet Tarihi", "Tweet", "Yazar", "Beğeni", "RT", "Yanıt", "Görüntülenme"],
        wrap=True,
        max_height=400
    )

    # Event handlers
    setup_btn.click(setup_browser, outputs=[setup_output])

    # Excel yükleme
    load_excel_btn.click(
        load_excel_handler,
        inputs=[excel_upload],
        outputs=[scrape_output, tweet_table, stats]
    )

    login_btn.click(login, inputs=[username, password], outputs=[login_output])

    scrape_btn.click(
        scrape_tweets_handler,
        inputs=[tweet_count, source_type, profile_username, hashtag, days_filter],
        outputs=[scrape_output, tweet_table, stats]
    )

    # CSV kaydetme
    save_csv_btn.click(
        save_csv_data,
        outputs=[scrape_output, csv_download_file]
    ).then(
        lambda file_path: gr.File(value=file_path, visible=True) if file_path else gr.File(visible=False),
        inputs=[csv_download_file],
        outputs=[csv_download_file]
    )

    # Excel kaydetme
    save_excel_btn.click(
        save_excel_data,
        outputs=[scrape_output, excel_download_file]
    ).then(
        lambda file_path: gr.File(value=file_path, visible=True) if file_path else gr.File(visible=False),
        inputs=[excel_download_file],
        outputs=[excel_download_file]
    )

    close_btn.click(close_browser, outputs=[scrape_output])

    # Kullanım örnekleri
    with gr.Accordion("📖 Excel Destekli Kullanım Örnekleri", open=False):
        gr.Markdown("""
        ### 🎯 Yeni Excel Özellikleri:

        **📊 Excel Veri Yükleme:**
        1. Daha önce kaydedilmiş Excel dosyasını yükleyin
        2. Veriler otomatik olarak tabloya yüklenir
        3. İstatistikler hesaplanır
        4. CSV ve Excel olarak tekrar indirebilirsiniz

        **📈 Excel Export Özellikleri:**
        - **2 Sayfa:** Tweet verileri + İstatistikler
        - **Gelişmiş Formatting:** Renkli başlıklar, otomatik kolon genişliği
        - **İstatistik Sayfası:** Toplam değerler, ortalamalar
        - **Professional Layout:** İş sunumları için hazır format

        **💾 Desteklenen Formatlar:**
        - **Import:** .xlsx, .xls dosyaları
        - **Export:** .xlsx (gelişmiş formatting), .csv

        **🔄 Workflow Örnekleri:**
        1. **Tweet Toplama → Excel Export → Analiz**
        2. **Eski Excel → Import → Yeni Verilerle Birleştir**
        3. **Excel → Düzenleme → Tekrar Import**

        **📋 Gerekli Excel Kolonları (Import için):**
        - `tweet`: Tweet metni
        - `yazar`: Yazar adı
        - `yazar_handle`: @username
        - `beğeni`: Beğeni sayısı
        - `retweet`: Retweet sayısı
        - `yanıt`: Yanıt sayısı
        - `görüntülenme`: Görüntülenme sayısı

        **🎨 Excel Formatting Özellikleri:**
        - Mavi başlık satırı (Twitter rengi)
        - Otomatik kolon genişliği
        - Tweet kolonu 60 karakter genişlik
        - İstatistik sayfası ayrı formatlama
        - Professional görünüm
        """)

if __name__ == "__main__":
    print("🚀 Excel Destekli X Scraper başlatılıyor...")
    print("✨ Yeni özellikler: Excel import/export, Gelişmiş formatting")
    print("📊 2 sayfalı Excel: Veriler + İstatistikler")
    print("💾 Çift format desteği: CSV + Excel")
    app.launch(server_name="127.0.0.1", server_port=7864, inbrowser=True)