import asyncio
import os
from playwright.async_api import async_playwright
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        if href.startswith("javascript:") or href.startswith("mailto:"):
            continue
        full_url = urljoin(base_url, href)
        links.add(full_url)
    return list(links)

async def fetch_and_save(page, url, semaphore, out_dir: str, timeout_ms: int, file_index: int, saved_files: list):
    async with semaphore:
        try:
            await page.goto(url, timeout=timeout_ms)
            await page.wait_for_load_state("networkidle")
            html = await page.content()
            filename = os.path.join(out_dir, f"page_{file_index}.html")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)
            saved_files.append(filename)
            print(f"[✓] Fetched ({file_index}): {url}")
            return html
        except Exception as e:
            print(f"[✗] Failed ({file_index}): {url} — {str(e)}")
            return None

async def scrape_recursive(urls, out_dir, semaphore, timeout_ms, depth, seen, saved_files, file_counter, max_pages):
    if depth == 0 or not urls or file_counter[0] >= max_pages:
        return
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        tasks = []
        for url in urls:
            if url not in seen and file_counter[0] < max_pages:
                seen.add(url)
                page = await browser.new_page()
                index = file_counter[0]
                file_counter[0] += 1
                tasks.append(fetch_and_save(page, url, semaphore, out_dir, timeout_ms, index, saved_files))
        htmls = await asyncio.gather(*tasks)
        await browser.close()
    next_urls = set()
    for html, url in zip(htmls, urls):
        if html and file_counter[0] < max_pages:
            next_urls.update(extract_links(html, url))
    next_urls = [u for u in next_urls if u not in seen]
    await scrape_recursive(next_urls, out_dir, semaphore, timeout_ms, depth - 1, seen, saved_files, file_counter, max_pages)

def run_scraper(urls: list[str], depth: int, output_dir: str, max_concurrent: int = 5, timeout_ms: int = 60000, max_pages: int = 100):
    os.makedirs(output_dir, exist_ok=True)
    semaphore = asyncio.Semaphore(max_concurrent)

    if depth <= 0:
        print("Depth must be greater than 0.")
        return []

    seen = set()
    saved_files = []
    file_counter = [0]  # Mutable counter for page numbering

    print(f"Starting scraper: depth={depth}, max_pages={max_pages}, urls={len(urls)}")
    asyncio.run(scrape_recursive(urls, output_dir, semaphore, timeout_ms, depth, seen, saved_files, file_counter, max_pages))
    return saved_files
s