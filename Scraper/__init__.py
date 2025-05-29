from Utils import Config
from .scraper import __scraper
from .cleanup import __clean_and_normalize_html_files


def scraper( urls: list[str] , depth : int, config:Config ):
    """
    Scrapes the given URLs with the specified depth and configuration.

    Args:
        urls (list[str]): List of URLs to scrape.
        depth (int): Depth of scraping.
        config (Config): Configuration object containing settings.

    Returns:
        list[str]: List of file paths where the scraped content is saved.
    """
    return __scraper(
        urls=urls,
        depth=depth,
        outputDir=config.scrapedDir,
        maxConcurrentBrowsers=config.maxConcurrentBrowsers,
        timeoutMs=config.timeoutMs,
        maxPages=config.pageLimit,
    )


def clean_and_normalize_html_files( files: list[str], config: Config ):
    """
    Cleans up and normalizes the scraped files.

    Args:
        files (list[str]): List of file paths to clean up.
        config (Config): Configuration object containing settings.
    """
    __clean_and_normalize_html_files(files)
    