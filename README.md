# 🔍 XSS Parameter Finder

## 🌟 Overview

**XSS Parameter Finder** is a Python-based tool designed to scan and detect Cross-Site Scripting (XSS) vulnerabilities in web applications. The tool supports crawling web pages, testing parameters with customizable payloads, and integrating Wayback Machine to find additional archived URLs for testing.

---

## ✨ Features

- 🌐 **Crawl Websites**: Automatically discover links and parameters from a target domain.
- 🛡️ **Test for XSS**: Use default or custom payloads to test for XSS vulnerabilities.
- 🕰️ **Wayback Machine Integration**: Fetch archived URLs for testing with `waybackurls`.
- 📂 **Save Results**: Export findings to a JSON file.
- 🚀 **User-Friendly Menu**: Simple configuration options through an interactive menu.

---

## 📋 Requirements

Install the necessary Python libraries:
```bash
pip install -r requirements.txt
```

---

## 🚀 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Hackpy3/XSS-Parameter-Finder
   cd XSS-Parameter-Finder
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Install `waybackurls`** for fetching archived URLs:
   ```bash
   go install github.com/tomnomnom/waybackurls@latest
   ```

---

## 🔧 Usage

Run the script:
```bash
python m.py
```

### 🖥️ Menu Options
1. **Domain**: Enter the target URL (e.g., `https://example.com`).
2. **Payloads**: 
   - Option 1: Use default payloads.
   - Option 2: Load custom payloads from a `.txt` file.
3. **Output**: Specify the result file name (default: `result.json`).
4. **Delay**: Set delay between requests (default: `1.0` seconds).

---

## 💡 Example

1. **Run the Script**:
   ```bash
   python m.py
   ```

2. **Menu Interaction**:
   - Enter domain: `https://example.com`
   - Choose payloads: `1` (Default Payloads)
   - Specify output file: `xss_results.json`
   - Set delay: `1.5`

3. **Sample Output**:
   ```json
   [
       {
           "url": "https://example.com/search?q=<script>alert('XSS')</script>",
           "parameter": "q",
           "payload": "<script>alert('XSS')</script>",
           "status": "VULNERABLE"
       }
   ]
   ```

4. **View Results**:
   Results will be saved in `xss_results.json`.

---

## ⚠️ Disclaimer

This tool is intended for **educational purposes** and **ethical penetration testing** only. **Unauthorized use** is strictly prohibited. Always ensure you have the proper permissions before testing any website.

---

Let me know if you'd like to include more details or additional emojis! 🎉
