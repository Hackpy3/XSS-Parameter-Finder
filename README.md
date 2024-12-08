# 🚀 XSS Parameter Finder  

**XSS Parameter Finder** is a Python-based tool designed for ethical hackers, penetration testers, and security enthusiasts to find Cross-Site Scripting (XSS) vulnerabilities across a target domain and its subdomains. It tests query parameters for vulnerabilities by injecting a variety of payloads and reports its findings.  

---

## ✨ **Features**  

- 🌐 **Domain-wide Scanning**: Crawls the target domain and its subdomains.  
- 🔍 **XSS Testing**: Tests query parameters with multiple XSS payloads.  
- 📂 **Output Logging**: Saves the results to a file for review.  
- ⚡ **Lightweight and Efficient**: Easy to run with minimal dependencies.  

---

## 📥 **Installation**  

1. Clone the repository:  
   ```bash
   git clone https://github.com/Hackpy3/XSS-Parameter-Finder
   cd XSS-Parameter-Finder
   ```  

2. Install the required dependencies:  
   ```bash
   pip install requests beautifulsoup4 tldextract
   ```  

3. Run the tool:  
   ```bash
   python xss-parameter-finder.py
   ```  

---

## 🛠️ **Usage**  

1. Run the script:  
   ```bash
   python xss-parameter-finder.py
   ```  

2. Provide the target domain and output file name when prompted:  
   ```
   🌟 Welcome to XSS Parameter Finder 🌟
   🔗 Enter the target domain (e.g., https://example.com): https://example.com  
   📂 Enter the name of the output file (e.g., results.txt): xss_results.txt  
   ```  

3. Review the results in the terminal and the saved file:  
   - Example terminal output:  
     ```
     ✅ [VULNERABLE] Parameter 'q' is vulnerable to XSS on https://example.com/page?q=<script>alert('XSS')</script>
     🛡️ [SAFE] No vulnerabilities found for https://sub.example.com/path
     📁 Results saved to: xss_results.txt
     ```  

   - Example saved file (`xss_results.txt`):  
     ```
     ✅ [VULNERABLE] Parameter 'q' is vulnerable to XSS on https://example.com/page?q=<script>alert('XSS')</script>
     🛡️ [SAFE] No vulnerabilities found for https://sub.example.com/path
     ❌ Error testing https://sub.example.com/test: Connection Timeout
     ```  


## ⚠️ **Disclaimer**  

> 🚨 **Warning**:  
> This tool is intended for **educational purposes** and **authorized penetration testing** only.  
> 🚫 **Do not use this tool on systems without explicit permission. Unauthorized usage is illegal and unethical.**  
> The author assumes **no responsibility** for misuse or damages caused by this tool.  

**Always ensure you have proper authorization before testing any system!**  

---

## 🤝 **Contributions**  

Contributions are welcome! If you have ideas for new features, improvements, or bug fixes:  

1. 🍴 Fork the repository.  
2. 🌿 Create a new branch for your changes.  
3. 📝 Submit a pull request with a detailed description.  

---

## 📜 **License**  

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.  

---

## 📬 **Contact**  

For issues, suggestions, or feedback, please open an issue on the [GitHub repository](https://github.com/your-username/xss-parameter-finder/issues).  

---

## ⚠️ Disclaimer  

This tool is for **educational purposes** and **authorized testing** only. Unauthorized use is strictly prohibited and may violate local, state, or federal laws.  

---


Let me know if you need further adjustments or more features added! 😊

--- 

Made ❤️ by Mamun
