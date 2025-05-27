from playwright.sync_api import sync_playwright

def fetch_rendered_html_sync(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000, wait_until="load")
        content = page.content()
        browser.close()
        return content

url = 'https://www.flipkart.com/mobiles/nothing~brand/pr?sid=tyy,4io'
html = fetch_rendered_html_sync(url)

# Save to a local file
with open("page.html", "w", encoding="utf-8") as f:
    f.write(html)

print("HTML saved to page.html")
