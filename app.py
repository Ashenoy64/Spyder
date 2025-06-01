import streamlit as st
import os
import importlib
import Settings
from main import main as run_pipeline
import asyncio
import sys

if sys.platform.startswith('win'):
    print("Detected Windows platform, setting event loop policy for compatibility.")
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# === Helper functions ===
def reload_settings():
    importlib.reload(Settings)

def save_settings_ui():
    st.subheader("⚙️ Settings")
    with st.form("update_settings_form"):
        temp_dir = st.text_input("Temporary Directory", Settings.TEMP_DIR)
        dump_file = st.text_input("Dump File", Settings.DUMP_FILE)

        max_concurrent = st.number_input("Max Concurrent Browsers", min_value=1, value=Settings.MAX_CONCURRENT_BROWSERS)
        timeout_ms = st.number_input("Timeout (ms)", min_value=1000, value=Settings.TIMEOUT_MS)
        scraped_dir = st.text_input("Scraped HTML Directory", Settings.SCRAPED_DIR)
        page_limit = st.number_input("Max Pages to Scrape", min_value=1, value=Settings.PAGE_LIMIT)

        context_len = st.number_input("Context Length", min_value=100, value=Settings.CONTEXT_LENGTH)
        concurrent_extracts = st.number_input("Concurrent Extractions", min_value=1, value=Settings.CONCURRENT_EXTRACTIONS)
        csv_dir = st.text_input("CSV Output Directory", Settings.CSV_DIR)

        ai_model = st.text_input("AI Model", Settings.AI_MODEL)
        api_key = st.text_input("API Key", Settings.API_KEY)

        submit = st.form_submit_button("💾 Save Settings")

    if submit:
        with open("Settings.py", "w") as f:
            f.write(f'''import os\nimport dotenv\ndotenv.load_dotenv()\n\nTEMP_DIR = "{temp_dir}"
DUMP_FILE = "{dump_file}"
MAX_CONCURRENT_BROWSERS = {max_concurrent}
TIMEOUT_MS = {timeout_ms}
SCRAPED_DIR = "{scraped_dir}"
PAGE_LIMIT = {page_limit}
CONTEXT_LENGTH = {context_len}
CONCURRENT_EXTRACTIONS = {concurrent_extracts}
CSV_DIR = "{csv_dir}"
CSV_WRITER = None
AI_MODEL = "{ai_model}"
API_KEY = os.getenv("AI_API_KEY", "{api_key}")
AI_HOST = None
AI_FUNCTION = None
''')
        st.success("Settings updated. Reloading...")
        reload_settings()

# === UI ===
st.set_page_config(page_title="LLM Web Extractor", layout="wide")
st.title("🔍 LLM Web Scraper & Extractor")

with st.sidebar:
    st.markdown("## Navigation")
    tab = st.radio("Select Page", ["Main", "Settings"])

if tab == "Settings":
    save_settings_ui()

elif tab == "Main":
    st.subheader("🌐 Scrape + Extract")

    # Initialize session state for dynamic inputs
    if "url_inputs" not in st.session_state:
        st.session_state.url_inputs = [""]
    if "schema_inputs" not in st.session_state:
        st.session_state.schema_inputs = [""]

    # URLs Section
    st.markdown("### 🔗 URLs")
    for i, url in enumerate(st.session_state.url_inputs):
        st.session_state.url_inputs[i] = st.text_input(f"URL #{i+1}", value=url, key=f"url_{i}")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("➕ Add URL"):
            st.session_state.url_inputs.append("")
    with col2:
        if st.button("➖ Remove Last URL") and len(st.session_state.url_inputs) > 1:
            st.session_state.url_inputs.pop()

    # Depth Selection
    depth = st.slider("Depth of Recursion", min_value=1, max_value=5, value=2)

    # Schema Section
    st.markdown("### 📐 Schemas")
    for i, schema in enumerate(st.session_state.schema_inputs):
        st.session_state.schema_inputs[i] = st.text_area(
            f"Schema #{i+1}",
            value=schema,
            key=f"schema_{i}",
            height=200,
            placeholder='[\n  {"name": "string", "price": "string"}\n]'
        )

    col3, col4 = st.columns([1, 1])
    with col3:
        if st.button("➕ Add Schema"):
            st.session_state.schema_inputs.append("")
    with col4:
        if st.button("➖ Remove Last Schema") and len(st.session_state.schema_inputs) > 1:
            st.session_state.schema_inputs.pop()

    # Final Values
    urls = [u.strip() for u in st.session_state.url_inputs if u.strip()]
    schemas = [s.strip() for s in st.session_state.schema_inputs if s.strip()]


    if st.button("🚀 Run Extraction") and urls and schemas:
        try:
            st.info("Running pipeline... this may take a moment ⏳")
            csv_paths = run_pipeline(urls=urls, depth=depth, schemas=schemas)

            for i, csv_path in enumerate(csv_paths):
                st.markdown(f"### 📄 Schema {i+1} Extracted Data")
                with open(csv_path, "rb") as f:
                    csv_data = f.read()
                    st.download_button(
                        label=f"⬇️ Download CSV ({len(csv_data)//1024} KB)",
                        data=csv_data,
                        file_name=os.path.basename(csv_path),
                        mime="text/csv",
                    )
                import pandas as pd
                df = pd.read_csv(csv_path)
                st.dataframe(df.head(5))
        except Exception as e:
            st.error(f"Error running pipeline: {str(e)}")
