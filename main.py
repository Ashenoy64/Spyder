import Settings
from Utils import Config
from AI.AI_groq import get_groq_autocompletion
from AI import set_auto_complete

from Scraper import scraper, clean_and_normalize_html_files
from DataExtractor import extract_data_from_html

def setup_config( Settings ):
    """
    Sets up the configuration for the scraper.
    
    Returns:
        Config: Configuration object with default settings.
    """
    return Config(
        tempDir=Settings.TEMP_DIR,
        dumpFile=Settings.DUMP_FILE,
        scraper = {   'maxConcurrentBrowsers':Settings.MAX_CONCURRENT_BROWSERS,
            'timeoutMs':Settings.TIMEOUT_MS,
            'scrapedDir':Settings.SCRAPED_DIR,
            'pageLimit':Settings.PAGE_LIMIT,
        },
        extractor = {   
            'contextLength':Settings.CONTEXT_LENGTH,
            'concurrentExtractions':Settings.CONCURRENT_EXTRACTIONS,
            'csvDir' : Settings.CSV_DIR,
            'csvWriter' : Settings.CSV_WRITER,
        },
        ai = {
            'model':Settings.AI_MODEL,
            'apiKey':Settings.API_KEY,
            'host':Settings.AI_HOST,
            'function':Settings.AI_FUNCTION
        }
    )

def setup_ai( config ):
    if config.ai['function'] is not None:
        set_auto_complete(config.ai['function'])
    else:
        set_auto_complete( get_groq_autocompletion(config.ai['apiKey'], config.ai['model']) )


def main( urls: list[str] = [], depth: int = 2, schemas : list[str] = [] ):
    """
    Main function to run the scraper with default settings.
    """
    config = setup_config( Settings )
    setup_ai( config )
    # Scrape the URLs with a depth of 2
    scraped_files = scraper(urls, depth=depth, config=config)
    clean_and_normalize_html_files(scraped_files, config)
    csv = extract_data_from_html(scraped_files, schemas, config)
    if not csv:
        print("No data extracted. Please check the schemas and URLs.")
        return []
    print("Data extraction complete. CSV files generated.")
    return csv


if __name__ == "__main__":
    pass