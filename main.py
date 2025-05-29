import Settings
from Utils import Config


from Scraper import scraper, clean_and_normalize_html_files

def setup_config():
    """
    Sets up the configuration for the scraper.
    
    Returns:
        Config: Configuration object with default settings.
    """
    return Config(
        tempDir=Settings.TEMP_DIR,
        maxConcurrentBrowsers=Settings.MAX_CONCURRENT_BROWSERS,
        timeoutMs=Settings.TIMEOUT_MS,
        scrapedDir=Settings.SCRAPED_DIR,
        pageLimit=Settings.PAGE_LIMIT
    )

def main( urls: list[str] = [], depth: int = 2, schema : list[dict] = [] ):
    """
    Main function to run the scraper with default settings.
    """
    config = setup_config()

    # Scrape the URLs with a depth of 2
    scraped_files = scraper(urls, depth=depth, config=config)
    clean_and_normalize_html_files(scraped_files, config)

if __name__ == "__main__":
    urls=[
        'https://www.flipkart.com/mobiles/nothing~brand/pr?sid=tyy,4io'
    ]
    main(urls, depth=2)