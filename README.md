# 🛡️ Professional XSS Parameter Finder  

A comprehensive tool designed to detect XSS (Cross-Site Scripting) vulnerabilities on websites. With advanced crawling, payload testing, and custom configurations, this tool is ideal for professionals and enthusiasts.  

---

## 🚀 Features  
- 🔍 **Crawls entire domains and subdomains** to find internal links.  
- 🧪 **Tests XSS payloads** against all parameters in the URLs.  
- 🛠️ **Customizable payloads** via external files.  
- 🕒 **Adjustable delay** between requests to prevent overloading servers.  
- 📁 **Saves results in JSON format** for detailed analysis.  
- 🌐 Designed for professional and ethical use only.  

---

## 🛠️ Installation  

1. Clone this repository:  
   ```bash
   git clone https://github.com/Hackpy3/XSS-Parameter-Finder.git
   ```  
2. Navigate to the directory:  
   ```bash
   cd XSS-Parameter-Finder
   ```  
3. Install the required dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  

---

## 📖 Usage  

```bash
python3 xss.py [-h] [-o OUTPUT] [-d DEPTH] [--delay DELAY] [--payloads PAYLOADS] domain
```  

### **Positional Arguments:**  
| Argument | Description |  
|----------|-------------|  
| `domain` | Target domain (e.g., `https://example.com`). |  

### **Options:**  
| Option | Description | Default Value |  
|--------|-------------|---------------|  
| `-h, --help` | Show the help message and exit. | — |  
| `-o, --output OUTPUT` | Output file name for results. | `xss_results.json` |  
| `-d, --depth DEPTH` | Maximum crawl depth. | `3` |  
| `--delay DELAY` | Delay between requests in seconds. | `1` |  
| `--payloads PAYLOADS` | File containing custom XSS payloads. | None (Uses default payloads). |  

---

### 🛠️ Examples  

1. **Basic Scan:**  
   ```bash
   python3 xss-parameter-finder.py https://example.com
   ```  

2. **Increase Depth and Add Delay:**  
   ```bash
   python3 xss-parameter-finder.py https://example.com -d 5 --delay 2
   ```  

3. **Custom Payloads:**  
   ```bash
   python3 xss-parameter-finder.py https://example.com --payloads my_payloads.txt
   ```  

4. **Custom Output File:**  
   ```bash
   python3 xss-parameter-finder.py https://example.com -o custom_results.json
   ```  

---

## 📝 Example Output  
Results will be saved in JSON format for easy parsing and analysis.  

```json
[
    {
        "url": "https://example.com/vulnerable?page=<script>alert('XSS')</script>",
        "parameter": "page",
        "payload": "<script>alert('XSS')</script>",
        "status": "VULNERABLE"
    }
]
```  

---

## ⚠️ Disclaimer  
**This tool is intended for educational purposes and authorized testing only.** Do not use it on domains or applications without explicit permission. Misuse of this tool is illegal.  

---

## 🛠️ Contribution  
Contributions are welcome! Feel free to submit issues or pull requests to enhance the functionality.  

---

## 📜 License  
This project is licensed under the MIT License. See `LICENSE` for more details.  

--- 

