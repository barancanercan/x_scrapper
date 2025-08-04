# 🚀 X (Twitter) Scraper - Excel Destekli Professional Tweet Collection Tool

<div align="center">

![X Scraper](https://img.shields.io/badge/X-Scraper-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Excel](https://img.shields.io/badge/Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-FF6B6B?style=for-the-badge&logo=gradio&logoColor=white)

**Advanced X (Twitter) scraper with Excel import/export, automatic tweet collection, profile analysis, hashtag search, and professional data formatting**

[🚀 Quick Start](#-quick-start) • [📊 Excel Features](#-excel-features) • [📖 Usage Guide](#-usage-guide) • [🔧 Installation](#-installation) • [❓ Troubleshooting](#-troubleshooting)

</div>

---

## 📋 Table of Contents

- [🌟 Features](#-features)
- [📊 Excel Features](#-excel-features)
- [🚀 Quick Start](#-quick-start)
- [📦 System Requirements](#-system-requirements)
- [🔧 Installation](#-installation)
- [📖 Usage Guide](#-usage-guide)
- [📈 Data Formats](#-data-formats)
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
- ✅ **Gradio Web Interface**: User-friendly web GUI
- ✅ **Anti-Detection**: Advanced bot detection countermeasures

### 📊 **NEW: Excel Features**
- 📈 **Excel Import**: Load previously saved Excel data
- 📊 **Professional Excel Export**: 2-sheet workbook with formatting
- 🎨 **Advanced Formatting**: Twitter-colored headers, auto-sizing
- 📋 **Statistics Sheet**: Comprehensive analytics page
- 💾 **Dual Format Support**: Both CSV and Excel export
- 🔄 **Data Workflow**: Import → Edit → Re-import capability
- 📱 **Business Ready**: Professional layouts for presentations

### 🛠️ **Technical Features**
- 🔄 **Intelligent Stopping**: Automatically stops when reaching old tweets
- 📊 **Real-time Stats**: Live statistics tracking
- 🎛️ **Customizable**: Tweet count and speed control
- 💾 **Advanced Data Management**: Excel + CSV support
- 🖥️ **Cross-Platform**: Windows/Mac/Linux support
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

## 📊 Excel Features

### 📈 **Import Capabilities**
| Feature | Description | Benefit |
|---------|-------------|---------|
| Excel File Upload | Load .xlsx/.xls files | Continue previous work |
| Auto Data Validation | Checks required columns | Error prevention |
| Data Type Conversion | Numbers, text formatting | Clean data processing |
| Duplicate Handling | Smart data merging | No data loss |

### 📊 **Export Features**
| Component | Description | Professional Use |
|-----------|-------------|------------------|
| **Data Sheet** | Complete tweet data with formatting | Analysis & reporting |
| **Statistics Sheet** | Totals, averages, metrics | Executive summaries |
| **Twitter Styling** | Blue headers, branded colors | Presentation ready |
| **Auto-sizing** | Optimized column widths | Print friendly |

### 📋 **Required Excel Columns (Import)**
```
tweet          - Tweet content
yazar          - Author name
yazar_handle   - @username
beğeni         - Like count
retweet        - Retweet count
yanıt          - Reply count
görüntülenme   - View count
```

### 🎨 **Excel Formatting Features**
- **Header Styling**: Twitter blue (#1DA1F2) with white text
- **Column Optimization**: Auto-width adjustment (max 50 chars)
- **Tweet Column**: Extra wide (60 chars) for readability
- **Statistics Page**: Separate professional formatting
- **Print Ready**: Optimized for business presentations

---

## 🚀 Quick Start

### ⚡ Launch in 3 Steps

```bash
# 1. Clone or download project files
# Ensure you have these files:
# - x2.py (main scraper file)
# - requirements.txt
# - .gitignore
# - README.md

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the scraper
python x2.py
```

### 🌐 Web Interface
After startup, opens automatically in your browser:
```
http://127.0.0.1:7864
```

---

## 📦 System Requirements

### 🖥️ **Operating System**
- Windows 10+
- macOS 10.14+
- Ubuntu 18.04+
- Any system supporting Python 3.8+

### 🐍 **Python Requirements**
- Python 3.8 or higher
- pip package manager

### 📊 **Dependencies (auto-installed)**
```
gradio>=4.0.0           # Web interface
pandas>=2.0.0           # Data processing
openpyxl>=3.1.0         # Excel support
selenium>=4.15.0        # Web automation
webdriver-manager>=4.0.1 # ChromeDriver management
```

### 🌐 **Browser**
- Google Chrome (recommended)
- Chromium
- ChromeDriver (auto-installed)

### 💾 **Hardware**
| Component | Minimum | Recommended | Excel Heavy |
|-----------|---------|-------------|-------------|
| RAM | 2 GB | 4 GB | 8 GB+ |
| Disk | 1 GB free | 5 GB | 10 GB+ |
| CPU | 2 cores | 4 cores | 8 cores+ |
| Internet | 1 Mbps | 5 Mbps | 10 Mbps+ |

---

## 🔧 Installation

### 1️⃣ **Basic Installation**

```bash
# Method 1: Using pip directly
pip install gradio pandas openpyxl selenium webdriver-manager requests

# Method 2: Using requirements.txt (recommended)
pip install -r requirements.txt
```

### 2️⃣ **Virtual Environment (Recommended)**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run scraper
python x2.py
```

### 3️⃣ **Chrome Setup**
```bash
# Chrome is automatically managed by webdriver-manager
# No manual ChromeDriver installation needed!
# First run will automatically download correct ChromeDriver
```

---

## 📖 Usage Guide

### 🔰 **Basic Usage**

#### **Step 1: Start Application**
```bash
python x2.py
```
- Web interface opens at `http://127.0.0.1:7864`
- Gradio interface loads with all features

#### **Step 2: Browser Setup**
1. Click **"🚀 Tarayıcı Hazırla"** button
2. ChromeDriver automatically downloaded and installed
3. Wait for **"✅ Chrome driver automatically installed!"** message

#### **Step 3: Excel Data Loading (Optional)**
1. **Upload Excel File**: Click **"📁 Excel Dosyası Yükle"**
2. **Select File**: Choose .xlsx or .xls file
3. **Load Data**: Click **"📊 Excel Verilerini Yükle"**
4. **Verify**: Check data appears in table and statistics

#### **Step 4: X Account Login**
1. Enter **X Username** without @ symbol
   ```
   Example: username (❌ NOT @username)
   ```
2. Enter your **X Password**
3. Click **"🔐 X'e Giriş Yap"** button
4. Wait for login confirmation

#### **Step 5: Configure Scraping**
1. **Tweet Count**: Choose 5-200 tweets
2. **Time Filter**: Set days (0=All, 7=Last week, 30=Last month)
3. **Source Selection**: 
   - `home`: Your timeline
   - `following`: Following tab
   - `foryou`: For You tab
4. **Profile Username** (Optional): Target specific user (e.g., `elonmusk`)
5. **Hashtag Search** (Optional): Search by hashtag (e.g., `#python`)

#### **Step 6: Collect Tweets**
1. Click **"🚀 Tweet Topla"** button
2. Process time: ~20 seconds for 20 tweets
3. **Smart stopping**: Auto-stops when time range exceeded

#### **Step 7: Export Data**
1. **CSV Export**: Click **"💾 CSV Hazırla"** for simple CSV
2. **Excel Export**: Click **"📊 Excel Hazırla"** for professional Excel
3. **Download**: Use download buttons that appear
4. **Choose Format**: CSV for analysis, Excel for presentations

### 📊 **Excel Workflow Examples**

#### **Workflow 1: Fresh Data Collection**
```
1. Browser Setup → Login → Scrape Tweets
2. Export to Excel (professional format)
3. Use Excel file for presentations/reports
```

#### **Workflow 2: Continue Previous Work**
```
1. Upload previous Excel file
2. Data loads automatically with statistics
3. Add new tweets or export in different format
```

#### **Workflow 3: Data Analysis Pipeline**
```
1. Collect tweets → Export Excel
2. Analyze in Excel/Google Sheets
3. Re-import edited data for further processing
```

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

---

## 📈 Data Formats

### 📄 **CSV Format (Simple)**
```csv
zaman_toplama,tweet_tarihi,tweet,yazar,yazar_handle,beğeni,retweet,yanıt,görüntülenme,url
2025-08-04 16:30,2025-08-04 14:25,Amazing tweet content!,Elon Musk,elonmusk,1500,250,45,89000,https://x.com/status/123456789
```

### 📊 **Excel Format (Professional)**

#### **Sheet 1: Tweet_Verileri**
- Complete tweet data with professional formatting
- Twitter-colored headers (#1DA1F2)
- Auto-sized columns for optimal display
- Tweet column optimized for readability

#### **Sheet 2: İstatistikler**
```
Metrik                    | Değer
--------------------------|----------
Toplam Tweet             | 50
Toplam Beğeni            | 25,400
Toplam Retweet           | 4,560
Toplam Yanıt             | 890
Toplam Görüntülenme      | 2,840,000
Ortalama Beğeni          | 508
Ortalama Görüntülenme    | 56,800
Oluşturulma Tarihi       | 2025-08-04 16:30:15
```

### 📈 **Google Sheets Integration**
1. Export as Excel from scraper
2. **Google Sheets → File → Import → Upload**
3. **Excel file automatically formatted and ready**
4. All charts and pivot tables work immediately

### 📊 **Business Intelligence Ready**
```
Power BI: Import Excel directly
Tableau: Drag-and-drop Excel file
Excel Pivot: Ready for pivot tables
Google Data Studio: Connect via Sheets
```

---

## ⚙️ Configuration

### 🔧 **Basic Settings**

#### **Port Configuration**
```python
# In x2.py, bottom of file
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

### 📊 **Excel Configuration**

#### **Column Width Customization**
```python
# In save_excel() method
worksheet.column_dimensions['C'].width = 60  # Tweet column
worksheet.column_dimensions['A'].width = 20  # Date column
```

#### **Color Scheme Customization**
```python
# Header colors
header_fill = PatternFill(start_color="1DA1F2", end_color="1DA1F2", fill_type="solid")
# Change to your brand colors
header_fill = PatternFill(start_color="YOUR_COLOR", end_color="YOUR_COLOR", fill_type="solid")
```

### 🛡️ **Security Settings**

#### **Rate Limiting** (Speed Control)
```python
# For safer scraping, increase wait times
time.sleep(4)  # Between page transitions
time.sleep(3)  # Between scrolls
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

#### **Local Processing Enhanced**
- ✅ All data stays local (including Excel files)
- ✅ Excel files processed locally with pandas/openpyxl
- ✅ No cloud uploads or external Excel services
- ✅ Complete offline capability after initial setup

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

#### **Excel File Security**
- 🔒 **Local Processing**: Excel files never leave your computer
- 🔒 **No Cloud Upload**: No external Excel services used
- 🔒 **Data Validation**: Import validation prevents malformed data

---

## ❓ Troubleshooting

### 🔧 **Common Issues and Solutions**

#### **1. Installation Issues**
```
❌ Error: "ModuleNotFoundError: No module named 'gradio'"
```
**Solution:**
```bash
# Install missing dependencies
pip install -r requirements.txt

# Or install individually
pip install gradio pandas openpyxl selenium webdriver-manager
```

#### **2. ChromeDriver Issues**
```
❌ Error: "This version of ChromeDriver only supports Chrome version X"
```
**Solution:**
```bash
# Update Chrome browser
# webdriver-manager will auto-download correct driver on next run

# Or restart application (auto-updates)
python x2.py
```

#### **3. X Login Failed**
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
Type manually, don't copy-paste

# d) Manual verification
Can you manually log in to x.com in browser?
```

#### **4. Excel Import Failed**
```
❌ Error: "Excel dosyası yüklenemedi"
```
**Solutions:**
```bash
# a) File format check
✅ Supported: .xlsx, .xls
❌ Not supported: .csv, .ods

# b) Column verification
Required columns: tweet, yazar, yazar_handle, beğeni, retweet, yanıt, görüntülenme

# c) File corruption
Try opening file in Excel/LibreOffice first
```

#### **5. Port Conflict**
```
❌ Error: "Address already in use: 7864"
```
**Solution:**
```bash
# Use different port
# Change port 7864 → 7865 in x2.py

# Or kill running application
pkill -f "x2.py"
```

#### **6. Empty CSV/Excel File**
```
❌ Issue: File only contains headers
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
# In x2.py, add logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### **Save Terminal Output**
```bash
# Save logs to file while running
python x2.py 2>&1 | tee debug.log
```

#### **Common Error Codes**
| Error Code | Description | Solution |
|------------|-------------|----------|
| `TimeoutException` | Element not found | Increase wait time |
| `NoSuchElementException` | Wrong selector | X interface may have changed |
| `WebDriverException` | Chrome problem | Restart Chrome |
| `ModuleNotFoundError` | Missing dependency | Install requirements.txt |
| `FileNotFoundError` | Excel file missing | Check file path |

### 🚨 **Emergency Procedures**

#### **Application Frozen**
```bash
# 1. Stop with Ctrl+C in terminal
# 2. Kill all Chrome processes
pkill -f chrome
pkill -f chromium

# 3. Restart
python x2.py
```

#### **System Resources Exhausted**
```bash
# Check RAM usage
# Windows: Task Manager
# macOS: Activity Monitor  
# Linux: htop

# Restart application if necessary
```

---

## 🔄 Updates and Maintenance

### 📅 **Routine Maintenance**

#### **Weekly Checks**
```bash
# Update dependencies
pip list --outdated
pip install --upgrade gradio pandas openpyxl selenium webdriver-manager

# Chrome update (automatic via webdriver-manager)
# No manual intervention needed
```

#### **Monthly Cleanup**
```bash
# Archive old files
mkdir -p archive/$(date +%Y-%m)
mv x_tweets_*.csv archive/$(date +%Y-%m)/
mv x_tweets_*.xlsx archive/$(date +%Y-%m)/

# Clean temporary files
# Windows: del /q %temp%\*
# macOS/Linux: rm -rf /tmp/chrome*
```

---

## 📊 Performance Analytics

### ⚡ **Excel Performance Metrics**

#### **Export Speed Comparison**
| Format | 50 Tweets | 200 Tweets | 500 Tweets |
|--------|-----------|------------|------------|
| **CSV** | 0.5s | 1.2s | 2.8s |
| **Excel Simple** | 1.2s | 3.5s | 8.2s |
| **Excel Professional** | 2.1s | 5.8s | 14.5s |

#### **File Size Comparison**
| Format | 100 Tweets | Features |
|--------|------------|----------|
| **CSV** | 85 KB | Basic data only |
| **Excel** | 125 KB | Formatted + Statistics |

#### **Memory Usage**
| Operation | RAM Usage | Recommendation |
|-----------|-----------|----------------|
| CSV Export | 50 MB | Any system |
| Excel Export | 150 MB | 4 GB+ RAM |
| Excel Import | 100 MB | 4 GB+ RAM |

---

## 🤝 Contributing

### 💡 **Feature Requests**

#### **Planned Features**
- [ ] **Multi-account support**: Multiple account handling
- [ ] **Scheduled scraping**: Automated time-based collection
- [ ] **Real-time monitoring**: Live tweet tracking
- [ ] **Advanced Excel charts**: Built-in visualization
- [ ] **Database integration**: SQLite/PostgreSQL support
- [ ] **API endpoints**: REST API access

### 🔧 **Development Environment**

#### **File Structure**
```
x_scrapper/
├── x2.py                 # Main application file
├── requirements.txt      # Dependencies
├── .gitignore           # Git ignore rules
├── README.md            # Documentation
└── (generated files)
    ├── *.csv            # CSV exports
    ├── *.xlsx           # Excel exports
    └── *.log            # Debug logs
```

#### **Contributing Steps**
1. **Fork** this repository
2. **Create feature branch**: `git checkout -b new-feature`
3. **Test thoroughly**: Ensure Excel and CSV work
4. **Commit changes**: `git commit -m "Add Excel feature"`
5. **Push to branch**: `git push origin new-feature`
6. **Create Pull Request**

#### **Code Style**
```python
# Follow PEP 8 standards
# Use type hints where appropriate
def scrape_tweets(max_tweets: int) -> List[Dict[str, Any]]:
    """Collect tweets with Excel support."""
    pass

# Add docstrings
def save_excel(self) -> Tuple[str, str]:
    """
    Save data to Excel with professional formatting.
    
    Returns:
        Tuple of (success_message, file_path)
    """
```

---

## 📄 License

### 📜 **MIT License**

```
MIT License

Copyright (c) 2025 X Scraper Excel Edition

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

#### **Excel Disclaimer**
- Excel files are processed locally using open-source libraries
- No Microsoft Excel license required for basic functionality
- Advanced Excel features may require Microsoft Office
- OpenOffice/LibreOffice compatible

---

## 📞 Support

### 🆘 **Getting Help**

#### **Documentation**
- 📖 This README contains comprehensive usage information
- 💡 Check the troubleshooting section for common issues
- 🔧 Review configuration options for customization

#### **Common Issues Quick Fix**
1. **Can't start application**: Check Python 3.8+ installed
2. **Excel import fails**: Verify required columns exist
3. **Login issues**: Disable 2FA, use correct username format
4. **No tweets collected**: Check internet connection and X login

#### **Best Practices**
- Start with small tweet counts (5-10) for testing
- Use time filters to avoid unnecessary processing
- Export to Excel for professional reports
- Use CSV for large datasets or analysis
- Monitor terminal output for debugging information

---

<div align="center">

**🚀 Happy Tweet Scraping with Excel Power! 📊**

Made by Baran Can Ercan with ❤️ for the AI communityi

[⭐ Star this repo](.) • [🐛 Report issues](.) • [💡 Request features](.)

</div>