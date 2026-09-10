from __future__ import annotations
from app.utils.text_utils import remove_html_tags, clean_encoding
import re

def preprocess_text(text: str) -> str:
    """
    Preprocess text by removing HTML, cleaning encoding, and collapsing whitespace.
    """
    if not text:
        return ""
    text = clean_encoding(text)
    text = remove_html_tags(text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text
