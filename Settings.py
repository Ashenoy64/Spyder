import dotenv
import os

dotenv.load_dotenv()



# Init 
TEMP_DIR = ".temp"
DUMP_FILE='dump.txt'

# Scraper
MAX_CONCURRENT_BROWSERS = 5
TIMEOUT_MS = 60000
SCRAPED_DIR = "scraped_pages"
PAGE_LIMIT = 10


# DataExtractor
CONTEXT_LENGTH = 5000
CONCURRENT_EXTRACTIONS = 5
# if set will give csv files, else returns data
CSV_DIR = 'csvs'
CSV_WRITER=None

# AI
AI_MODEL = "deepseek-r1-distill-llama-70b"
API_KEY = os.getenv("AI_API_KEY", "")
AI_HOST = None
# In case user has sperate AI function to extract Data, if this is set, it will use this ins
AI_FUNCTION = None
