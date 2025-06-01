import os
import dotenv

# Load environment variables from a .env file if present
dotenv.load_dotenv()

# =========================
# General Configuration
# =========================

# Directory for temporary files
TEMP_DIR = ".temp"

# File to dump logs or intermediate data
DUMP_FILE = "dump.txt"

# =========================
# Scraper Settings
# =========================

# Maximum number of browser instances running concurrently
MAX_CONCURRENT_BROWSERS = 5

# Timeout for browser operations (in milliseconds)
TIMEOUT_MS = 60_000

# Directory to store scraped HTML pages
SCRAPED_DIR = "scraped_pages"

# Maximum number of pages to scrape per run
PAGE_LIMIT = 10

# =========================
# Data Extraction Settings
# =========================

# Maximum number of characters to extract from context
CONTEXT_LENGTH = 5_000

# Number of concurrent data extraction processes
CONCURRENT_EXTRACTIONS = 5

# Directory to save extracted data as CSV files (if enabled)
CSV_DIR = "csvs"

# Optional: Custom CSV writer function. ( well this can make this do anything)
# If set, should accept: counter (int), schema (dict), data (list[dict]), output_dir (str)
CSV_WRITER = None

# =========================
# AI Integration Settings
# =========================

# Name of the AI model to use for data extraction or analysis
AI_MODEL = "deepseek-r1-distill-llama-70b"

# API key for the AI service (read from environment variable 'AI_API_KEY')
API_KEY = os.getenv("AI_API_KEY", "")

# Optional: Custom AI host endpoint (set to None to use default)
AI_HOST = None

# Optional: Custom AI function for data extraction.
# If set, should accept: system_prompt (str), user_prompt (str)
AI_FUNCTION = None
