from pathlib import Path
from ebooklib import epub
import fitz  # PyMuPDF
import requests

def load_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    return "\n".join(page.get_text() for page in doc)

def load_epub(file_path: str) -> str:
    book = epub.read_epub(file_path)
    text = ""
    for item in book.get_items():
        if item.get_type() == epub.ITEM_DOCUMENT:
            text += item.get_content().decode("utf-8")
    return text

def load_txt(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")

def load_from_url(url: str) -> bytes:
    return requests.get(url).content
