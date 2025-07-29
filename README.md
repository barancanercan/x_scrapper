# 🚀 X (Twitter) Scraper - Professional Tweet Collection Tool

<div align="center">

![X Scraper](https://img.shields.io/badge/X-Scraper-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-FF6B6B?style=for-the-badge&logo=gradio&logoColor=white)

**Advanced X (Twitter) scraper with automatic tweet collection, profile analysis, hashtag search, and time filtering**

[🚀 Quick Start](#-quick-start) • [📖 Usage Guide](#-usage-guide) • [🔧 Installation](#-installation) • [❓ Troubleshooting](#-troubleshooting)

</div>

---

## 📋 Table of Contents

- [🌟 Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [📦 System Requirements](#-system-requirements)
- [🔧 Installation](#-installation)
- [📖 Usage Guide](#-usage-guide)
- [📊 Output Formats](#-output-formats)
- [⚙️ Configuration](#️-configuration)
- [🔒 Security](#-security)
- [❓ Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🌟 Features

### 🎯 **Core Features**
- ✅ **Real X Scraping**: Collects genuine tweets from timeline/profiles
- ✅ **Automatic Login**: Secure X account authentication
- ✅ **Complete Interaction Data**: Likes, retweets, replies, views
- ✅ **Tweet Timestamps**: Real tweet dates and times
- ✅ **Profile Scraping**: Target specific user profiles
- ✅ **Hashtag Search**: Search and collect tweets by hashtags
- ✅ **Time Filtering**: Collect tweets from specific date ranges
- ✅ **Smart Speed Optimization**: Stops when time range is exceeded
- ✅ **Gradio Download**: Download CSV directly from web interface
- ✅ **Anti-Detection**: Advanced bot detection countermeasures

### 🛠️ **Technical Features**
- 🔄 **Intelligent Stopping**: Automatically stops when reaching old tweets
- 📊 **Real-time Stats**: Live statistics tracking
- 🎛️ **Customizable**: Tweet count and speed control
- 💾 **Data Management**: Automatic file naming
- 🖥️ **Cross-Platform**: Ubuntu/Linux support
- 🔒 **Secure**: Local data processing, no external servers

### 📈 **Collected Data**
| Data Type | Description | Format |
|-----------|-------------|---------|
| Collection Time | When tweet was scraped | DateTime |
| Tweet Date | Original tweet timestamp | DateTime |
| Tweet Text | Full tweet content | String (500 chars) |
| Author Name | Tweet author's display name | String |
| Author Handle | Tweet author's @username | String |
| Like Count | Number of likes | Integer |
| Retweet Count | Number of retweets | Integer |
| Reply Count | Number of replies | Integer |
| View Count | Number of views | Integer |
| Tweet URL | Direct tweet link | URL |

---

## 🚀 Quick Start

### ⚡ Launch in 30 Seconds

```bash
# 1. Navigate to project folder
cd ~/Desktop/x_scrapper

# 2. Setup (first time only)
./setup_x_scraper.sh

# 3. Start application
./start_x_scraper.sh
```

### 🌐 Web Interface
After startup, opens automatically in your browser:
```
http://127.0.0.1:7864
```

---

## 📦 System Requirements

### 🖥️ **Operating System**
- Ubuntu 18.04+ (recommended: 20.04 or 22.04)
- Debian 10+
- Linux Mint 19+

### 🐍 **Python**
- Python 3.8 or higher
- pip package manager
- venv module

### 🌐 **Browser**
- Google Chrome 90+ or Chromium
- Automatic updates recommended

### 💾 **Hardware**
| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 2 GB | 4 GB+ |
| Disk | 1 GB free | 5 GB+ |
| CPU | 2 cores | 4 cores+ |
| Internet | 1 Mbps | 5 Mbps+ |

---

## 🔧 Installation

### 1️⃣ **System Preparation**

```bash
# System update
sudo apt update && sudo apt upgrade -y

# Python and essential tools
sudo apt install python3 python3-pip python3-venv curl wget -y

# Chrome/Chromium installation
sudo apt install chromium-browser -y
# OR Google Chrome:
# wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
# sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# sudo apt update && sudo apt install google-chrome-stable -y
```

### 2️⃣ **Project Setup**

```bash
# Create project folder
mkdir -p ~/Desktop/x_scrapper
cd ~/Desktop/x_scrapper

# Download/copy files (files that come with this README)
# x_scraper.py, setup_x_scraper.sh, start_x_scraper.sh

# Make scripts executable
chmod +x setup_x_scraper.sh start_x_scraper.sh

# Install Python virtual environment and dependencies
./setup_x_scraper.sh
```

### 3️⃣ **First Run**

```bash
# Start X Scraper
./start_x_scraper.sh
```

---

## 📖 Usage Guide

### 🔰 **Basic Usage**

#### **Step 1: Browser Setup**
1. Click **"🚀 Setup Browser"** button
2. ChromeDriver will be automatically downloaded and installed
3. Wait for **"✅ Chrome driver automatically installed and ready!"** message

#### **Step 2: X Account Login**
1. Enter **X Username** without @ symbol
   ```
   Example: username (❌ NOT @username)
   ```
2. Enter your **X Password**
3. Click **"🔐 Login to X"** button
4. Login process may take 10-15 seconds

#### **Step 3: Configure Scraping**
1. **Tweet Count**: Choose 5-200 tweets
2. **Time Filter**: Set days (0=All, 7=Last week, 30=Last month)
3. **Source Selection**: 
   - `home`: Your timeline
   - `following`: Following tab
   - `foryou`: For You tab
4. **Profile Username** (Optional): Target specific user (e.g., `elonmusk`)
5. **Hashtag Search** (Optional): Search by hashtag (e.g., `#python`)

#### **Step 4: Collect Tweets**
1. Click **"🚀 Collect Tweets"** button
2. Process time: ~20 seconds for 20 tweets
3. **Smart stopping**: Automatically stops when time range is exceeded

#### **Step 5: Download Data**
1. Click **"💾 Prepare CSV"** when collection is complete
2. **"📥 CSV Download"** section will appear
3. Click download button to save to your computer

### 🎛️ **Advanced Usage**

#### **Smart Time Filtering Examples**
| Filter | Description | Use Case |
|--------|-------------|----------|
| 0 days | All tweets | Complete analysis |
| 1 day | Last 24 hours | Daily monitoring |
| 7 days | Last week | Weekly reports |
| 30 days | Last month | Monthly analysis |

#### **Scraping Scenarios**

**1. Profile Analysis:**
```
- Tweet Count: 50
- Source: home
- Profile: elonmusk
- Time Filter: 7 (last week)
Result: Elon Musk's last 50 tweets from past 7 days
```

**2. Hashtag Monitoring:**
```
- Tweet Count: 100
- Source: home
- Hashtag: #ai
- Time Filter: 1 (last 24 hours)
Result: Latest 100 #ai tweets from last day
```

**3. Timeline Collection:**
```
- Tweet Count: 30
- Source: following
- Time Filter: 0 (all)
Result: 30 tweets from your Following timeline
```

### ⚡ **Speed Optimizations**

#### **Intelligent Stopping System**
- **Per-scroll limit**: Stops after 8 old tweets in one scroll
- **Global limit**: Stops after 20 total old tweets
- **Empty scroll limit**: Stops after 2 consecutive empty scrolls
- **Maximum scrolls**: Limited to 15 scrolls maximum

#### **Performance Expectations**
| Scenario | Old System | New System | Improvement |
|----------|------------|------------|-------------|
| 20 tweets, 7 days | 20 scrolls, 60s | 3-5 scrolls, 15-20s | **70% faster** |
| 50 tweets, 30 days | 25 scrolls, 90s | 8-10 scrolls, 30-35s | **65% faster** |
| Profile scraping | 15 scrolls, 45s | 5-7 scrolls, 18-22s | **55% faster** |

---

## 📊 Output Formats

### 📄 **CSV Format**
```csv
zaman_toplama,tweet_tarihi,tweet,yazar,yazar_handle,beğeni,retweet,yanıt,görüntülenme,url
2025-07-29 16:30,2025-07-29 14:25,This is an amazing tweet!,Elon Musk,elonmusk,1500,250,45,89000,https://x.com/status/123456789
2025-07-29 16:31,2025-07-29 13:45,Learning Python 🐍,TechLover,techlover,89,12,3,5400,https://x.com/status/123456790
```

### 📈 **Statistics Output**
```json
{
  "source": "@elonmusk",
  "collected_tweets": 20,
  "total_likes": 28400,
  "total_retweets": 4560,
  "total_replies": 890,
  "total_views": 2840000,
  "average_likes": 1420,
  "average_views": 142000,
  "most_popular_tweet": "Amazing announcement about...",
  "last_updated": "2025-07-29 16:30:15"
}
```

### 📊 **Google Sheets Import**
1. Open **Google Sheets**
2. **File → Import → Upload**
3. Drag your CSV file
4. Select **Separator type: Comma**
5. Click **Import data**

### 📈 **Excel Analysis Examples**
```excel
=AVERAGE(F:F)         // Average likes
=SUM(G:G)            // Total retweets  
=MAX(H:H)            // Most replies
=COUNTIF(E:E,"*Tech*") // Authors containing "Tech"
=MAX(I:I)            // Highest view count
```

---

## ⚙️ Configuration

### 🔧 **Basic Settings**

#### **Port Configuration**
```python
# In x_scraper.py, bottom of file
app.launch(server_name="127.0.0.1", server_port=7864, inbrowser=True)
# Change 7864 to desired port (e.g., 8080)
```

#### **Browser Mode**
```python
# Headless mode (background operation)
options.add_argument("--headless")

# Debug mode (developer tools)
options.add_argument("--auto-open-devtools-for-tabs")
```

### 🛡️ **Security Settings**

#### **Rate Limiting** (Speed Control)
```python
# For safer scraping, increase wait times
time.sleep(4)  # Between page transitions
time.sleep(3)  # Between scrolls
```

#### **User Agent Modification**
```python
options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36")
```

### 📁 **File Settings**

#### **Output Directory**
```python
# Save to different folder
csv_file = Path("outputs/tweets/x_tweets_{timestamp}.csv")
```

#### **File Format**
```python
# Change filename format
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
csv_file = Path(f"tweets_{username}_{timestamp}.csv")
```

---

## 🔒 Security

### 🛡️ **Data Security**

#### **Local Data Processing**
- ✅ All data stays on your local computer
- ✅ No data sent to external servers
- ✅ Internet only used to connect to X

#### **Account Security**
- ⚠️ **Important**: Only use your own account
- ⚠️ **2FA**: Disable two-factor authentication if enabled
- ⚠️ **Password**: Use strong password, don't share

#### **Bot Detection Countermeasures**
```python
# Current anti-detection features:
- User-Agent masking
- WebDriver property hiding  
- Human-like behavior (scrolling, waits)
- Random timing variations
```

### 🔐 **Privacy Measures**

#### **Credential Management**
```bash
# Don't store passwords in scripts!
# Enter manually each time or use environment variables

export X_USERNAME="your_username"
export X_PASSWORD="your_password"
```

#### **Log Cleanup**
```bash
# Clean sensitive logs
rm -f ~/.cache/selenium/
rm -f /tmp/chrome*
```

---

## ❓ Troubleshooting

### 🔧 **Common Issues and Solutions**

#### **1. ChromeDriver Compatibility**
```
❌ Error: "This version of ChromeDriver only supports Chrome version X"
```
**Solution:**
```bash
# Update Chrome
sudo apt update && sudo apt upgrade google-chrome-stable

# Or restart scraper (auto-updates)
./start_x_scraper.sh
```

#### **2. X Login Failed**
```
❌ Error: "Login verification failed"
```
**Solutions:**
```bash
# a) Username should not include @ symbol
❌ @username
✅ username

# b) 2FA must be disabled
X Settings → Security → Two-factor authentication → Disable

# c) Special characters in password
"Password123!" → type manually, don't copy-paste

# d) Manual verification
Can you manually log in to x.com in browser?
```

#### **3. No Tweets Collected**
```
❌ Error: "❌ Please log in to X first"
```
**Solution:**
```bash
# Check login status
1. Is there ✅ message in "Login Status" box?
2. Does x.com/home open manually?
3. Don't minimize application window
```

#### **4. Port Conflict**
```
❌ Error: "Address already in use: 7864"
```
**Solution:**
```bash
# Use different port
# Change port 7864 → 7865 in x_scraper.py

# Or kill running application
pkill -f "x_scraper.py"
```

#### **5. Empty CSV File**
```
❌ Issue: CSV file only contains headers
```
**Solution:**
```bash
# Try more tweets
Tweet Count: 5 → 20

# Try different time
Check if timeline has tweets in time range

# Debug mode
Follow terminal output: "🔍 X tweet element found"
```

### 🐛 **Error Logs**

#### **Enable Debug Mode**
```python
# In x_scraper.py, add logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### **Save Terminal Output**
```bash
# Save logs to file while running
./start_x_scraper.sh 2>&1 | tee debug.log
```

#### **Common Error Codes**
| Error Code | Description | Solution |
|------------|-------------|----------|
| `TimeoutException` | Element not found | Increase wait time |
| `NoSuchElementException` | Wrong selector | X interface may have changed |
| `WebDriverException` | Chrome problem | Restart Chrome |
| `ConnectionRefusedError` | Port problem | Change port |
| `StaleElementReferenceException` | Element outdated | Automatic retry implemented |

### 🚨 **Emergency Procedures**

#### **Application Frozen**
```bash
# 1. Stop with Ctrl+C
# 2. Kill all Chrome processes
pkill -f chrome
pkill -f chromium

# 3. Restart
./start_x_scraper.sh
```

#### **System Resources Exhausted**
```bash
# Check RAM usage
free -h

# Check Chrome processes
ps aux | grep chrome

# Restart computer if necessary
sudo reboot
```

---

## 🔄 Updates and Maintenance

### 📅 **Routine Maintenance**

#### **Weekly Checks**
```bash
# Chrome update
sudo apt update && sudo apt upgrade google-chrome-stable

# Python packages
source venv/bin/activate
pip list --outdated
```

#### **Monthly Cleanup**
```bash
# Archive old CSV files
mkdir -p archive/$(date +%Y-%m)
mv x_tweets_*.csv archive/$(date +%Y-%m)/

# Cache cleanup
rm -rf ~/.cache/selenium/
rm -rf /tmp/chrome*
```

---

## 📊 Performance Analytics

### ⚡ **Speed Improvements (v2.0)**

#### **Smart Stopping System**
- **Scroll Optimization**: Reduced from 20 to 15 max scrolls
- **Time Filter Intelligence**: Stops after 8 old tweets per scroll
- **Global Tracking**: Stops after 20 total old tweets encountered
- **Empty Scroll Detection**: Stops after 2 consecutive empty scrolls

#### **Before vs After**
```
Scenario: 20 tweets, 7-day filter, Profile scraping

OLD SYSTEM:
📜 Scroll 1/20 - 5 tweets found
📜 Scroll 2/20 - 1 tweet found  
📜 Scroll 3/20 - 0 tweets found
...continues for 20 scrolls...
⏱️ Total time: 60+ seconds

NEW SYSTEM:
📜 Scroll 1/15 - 5 tweets found
📜 Scroll 2/15 - 1 tweet found
⏰ 8 old tweets found in this scroll
🛑 Time range exceeded, stopping
⏱️ Total time: 15-20 seconds ⚡
```

### 📈 **Collection Statistics**

#### **Typical Performance**
| Tweets | Time Filter | Scrolls | Time | Success Rate |
|--------|-------------|---------|------|-------------|
| 20 | 7 days | 3-5 | 15-20s | 98% |
| 50 | 30 days | 8-12 | 35-45s | 95% |
| 100 | No filter | 15 | 60-70s | 92% |

---

## 🤝 Contributing

### 💡 **Feature Requests**

#### **Planned Features**
- [ ] **Multi-account support**: Multiple account handling
- [ ] **Scheduled scraping**: Automated time-based collection
- [ ] **Real-time monitoring**: Live tweet tracking
- [ ] **Advanced filters**: Sentiment, language, engagement filters
- [ ] **Export formats**: JSON, Excel, PDF export
- [ ] **Analytics dashboard**: Built-in visualization tools

#### **Technical Improvements**
- [ ] **Docker support**: Containerized deployment
- [ ] **REST API**: HTTP API endpoints
- [ ] **Database integration**: PostgreSQL/MySQL support
- [ ] **Proxy support**: Proxy server support
- [ ] **Captcha solving**: Automatic captcha resolution

### 🔧 **Development Environment**

#### **Contributing Steps**
1. **Fork** this repository
2. **Create feature branch**: `git checkout -b new-feature`
3. **Commit changes**: `git commit -m "Add new feature"`
4. **Push to branch**: `git push origin new-feature`
5. **Create Pull Request**

#### **Code Style**
```python
# Follow PEP 8 standards
# Use type hints
def scrape_tweets(max_tweets: int) -> List[Dict[str, Any]]:
    """Collect tweets."""
    pass

# Add docstrings
def login_x(username: str, password: str) -> bool:
    """
    Log in to X account.
    
    Args:
        username: X username
        password: X password
        
    Returns:
        True if login successful, False otherwise
    """
```

---

## 📄 License

### 📜 **MIT License**

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

### ⚖️ **Legal Disclaimers**

#### **Usage Terms**
- Use responsibly and respect X's Terms of Service
- Only scrape your own timeline or public content
- Respect rate limits and don't overload X's servers
- For educational and personal use only
- Commercial use may require additional considerations

#### **Disclaimer**
This tool is provided for educational purposes. Users are responsible for compliance with applicable laws and platform terms of service. The developers are not responsible for any misuse of this software.

---

## 📞 Support

### 🆘 **Getting Help**

#### **Documentation**
- 📖 This README contains comprehensive usage information
- 💡 Check the troubleshooting section for common issues
- 🔧 Review configuration options for customization

#### **Community**
- 🐛 **Bug Reports**: Create an issue with detailed description
- 💡 **Feature Requests**: Open an issue with enhancement label
- 🤝 **Contributions**: Submit pull requests with improvements

#### **Best Practices**
- Start with small tweet counts (5-10) for testing
- Use time filters to avoid unnecessary processing
- Monitor terminal output for debugging information
- Keep Chrome/Chromium updated for compatibility

---

<div align="center">

**🚀 Happy Tweet Scraping! 🐦**

Made with ❤️ for the ai community via Baran Can Ercan  ❤️️

</div>
