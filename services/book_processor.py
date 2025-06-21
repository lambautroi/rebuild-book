from utils.file_loader import load_pdf, load_epub, load_txt
from utils.text_cleaner import clean_text
from utils.chapter_splitter import split_chapters
from utils.firestore_utils import save_book_text

def process_book(book_id: str, file_path: str, file_type: str):
    if file_type == "pdf":
        raw_text = load_pdf(file_path)
    elif file_type == "epub":
        raw_text = load_epub(file_path)
    elif file_type == "txt":
        raw_text = load_txt(file_path)
    else:
        raise ValueError("Unsupported file type")

    cleaned = clean_text(raw_text)
    chapters = split_chapters(cleaned)
    save_book_text(book_id, cleaned, chapters)
