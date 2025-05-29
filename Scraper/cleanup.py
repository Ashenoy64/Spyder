from bs4 import BeautifulSoup, Comment
from bs4.element import NavigableString
import os

def __clean_and_normalize_html_files(file_paths: list[str]):
    for path in file_paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                html = f.read()

            soup = BeautifulSoup(html, "html.parser")

            # Remove script, style, and noscript tags
            for tag in soup(["script", "style", "noscript"]):
                tag.decompose()

            # Optional: Remove comments
            for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
                comment.extract()

            # Clean up extra whitespace in text
           
            for tag in soup.find_all(string=True):
                if isinstance(tag, NavigableString):
                    tag.replace_with(tag.strip())

            # Normalize line breaks and indentation
            cleaned_html = soup.prettify()

            # Write cleaned content back to the same file
            with open(path, "w", encoding="utf-8") as f:
                f.write(cleaned_html)

            print(f"[✓] Cleaned: {path}")
        except Exception as e:
            print(f"[✗] Failed to clean {path}: {str(e)}")
