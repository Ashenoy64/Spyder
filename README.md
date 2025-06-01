# 🕷️ Spyder

**Spyder** is a modular, asynchronous web scraper and AI-powered structured data extractor. It lets you define one or more data schemas and extract structured information from a set of websites, including JavaScript-rendered pages.

It includes a simple Streamlit interface for running extractions, managing schemas, and downloading results.

---

## ✅ Overview

- Scrape static and JS-based websites using Playwright
- Recursively follow internal links (depth-limited)
- Normalize and clean HTML before processing
- Extract structured data based on your schema using LLMs
- Outputs one CSV file per schema
- Streamlit UI for managing scraping and reviewing results

---

## 🛠️ Setup

### 1. Install dependencies

```bash
git clone https://github.com/Ashenoy64/Spyder
cd Spyder
pip install -r requirements.txt
````

### 2. Optional: Set your API key

Create a `.env` file and add:

```
AI_API_KEY=your_groq_or_other_api_key
```

Or modify `Settings.py` directly.

---

## ▶️ Usage

### Run via script

```python
from main import main

urls = ["https://example.com"]
schemas = [
    '''
    [
      {
        "title": "string - Page title",
        "date": "string - Published date"
      }
    ]
    '''
]
main(urls, depth=2, schema=schemas)
```

### Run via Streamlit

```bash
streamlit run app.py
```

Use the UI to enter URLs, schemas, configure depth, and download extracted CSV files.

---

## ⚙️ Configuration

Edit `Settings.py` or use the Streamlit sidebar to configure:

* `TEMP_DIR`, `SCRAPED_DIR`, `CSV_DIR`
* `MAX_CONCURRENT_BROWSERS`, `PAGE_LIMIT`, `TIMEOUT_MS`
* AI model, API key, and optional custom extraction function

---

## 🧠 Supported Models

Tested with the following LLMs via GROQ:

* `deepseek-r1-distill-llama-70b` (recommended)
* `llama-3.3-70b-versatile`
* `meta-llama/llama-4-maverick`
* `qwen-qwq-32b`

You can also integrate with your own local model or function via `AI_FUNCTION`.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — © 2025 Avanish Shenoy


