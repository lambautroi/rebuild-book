import requests
from bs4 import BeautifulSoup
from ebooklib import epub, ITEM_DOCUMENT
import re
import io

BASE_URL = "https://www.gutenberg.org"
SEARCH_URL = "https://www.gutenberg.org/ebooks/search/?query="

def search_gutenberg(keyword: str, max_results: int = 10):
    """Tìm sách theo từ khóa"""
    url = SEARCH_URL + keyword.replace(" ", "+")
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    books = []
    for book_link in soup.select("li.booklink")[:max_results]:
        title = book_link.select_one("span.title").get_text(strip=True)
        author = book_link.select_one("span.subtitle").get_text(strip=True) if book_link.select_one("span.subtitle") else ""
        href = book_link.a["href"]
        book_id = href.split("/")[-1]
        books.append({
            "book_id": book_id,
            "title": title,
            "author": author,
            "url": BASE_URL + href
        })
    return books

def get_download_url(book_id: str, fmt="utf-8"):
    """Tìm link download EPUB hoặc TXT cho sách"""
    url = f"{BASE_URL}/ebooks/{book_id}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    links = soup.select("a.link")
    for link in links:
        href = link.get("href", "")
        if fmt == "epub" and "epub.images" in href and href.endswith(".epub.images"):
            return BASE_URL + href
        elif fmt == "txt" and href.endswith(".txt") and "utf-8" in href:
            return BASE_URL + href
    return None

def download_book(book_id: str, preferred_fmts=("epub", "txt", "html")) -> str:
    for fmt in preferred_fmts:
        download_url = get_download_url(book_id, fmt)
        if download_url:
            print(f"✅ Tìm thấy định dạng: {fmt} → đang tải từ Gutenberg...")
            r = requests.get(download_url)

            if fmt == "epub":
                # Dùng ebooklib để parse nội dung epub đúng
                book = epub.read_epub(io.BytesIO(r.content))
                text = ""
                for item in book.get_items():
                    if item.get_type() == ITEM_DOCUMENT:  # Sửa lại ở đây
                        soup = BeautifulSoup(item.get_content(), "html.parser")
                        text += soup.get_text() + "\n"
                return text

            else:
                return r.text
    raise Exception(f"❌ Không tìm được định dạng phù hợp cho sách {book_id}")

def auto_tag(title: str, author: str) -> list:
    """Gắn tag cơ bản từ tiêu đề hoặc tác giả"""
    tags = []
    title_lower = title.lower()
    if any(k in title_lower for k in ["philosophy", "plato", "ethics"]):
        tags.append("philosophy")
    if any(k in title_lower for k in ["war", "peace", "pride", "prejudice", "novel"]):
        tags.append("classic")
    if any(k in title_lower for k in ["tale", "fiction", "story"]):
        tags.append("fiction")
    if not tags:
        tags.append("general")
    return tags
