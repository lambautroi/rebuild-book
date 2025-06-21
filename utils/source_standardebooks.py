import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://standardebooks.org"
CATALOG_URL = "https://standardebooks.org/ebooks"

def search_standard_ebooks(keyword: str, max_results: int = 10):
    """Tìm sách theo từ khóa trong danh sách ebook"""
    r = requests.get(CATALOG_URL)
    soup = BeautifulSoup(r.content, "html.parser")
    books = []

    for a in soup.select("li.ebook > a")[:max_results * 3]:
        title = a.select_one("h3").text.strip()
        author = a.select_one("p.author").text.strip()
        link = BASE_URL + a.get("href")
        if keyword.lower() in title.lower() or keyword.lower() in author.lower():
            slug = a.get("href").strip("/")
            books.append({
                "slug": slug,
                "title": title,
                "author": author,
                "url": link
            })
        if len(books) >= max_results:
            break
    return books

def get_download_url(slug: str):
    """Tạo link tải EPUB"""
    return f"https://standardebooks.org/ebooks/{slug}/download"

def download_book(slug: str, preferred_fmts=("epub",)) -> str:
    download_url = get_download_url(slug)
    if not download_url:
        raise Exception(f"❌ Không tìm được link tải EPUB cho sách {slug}")
    print(f"✅ Đang tải EPUB từ Standard Ebooks: {download_url}")
    r = requests.get(download_url)
    return r.content.decode("utf-8", errors="ignore")


def auto_tag(title: str, author: str) -> list:
    """Gắn tag đơn giản"""
    tags = []
    title_lower = title.lower()
    if "essay" in title_lower or "philosophy" in title_lower:
        tags.append("philosophy")
    if "novel" in title_lower or "classic" in title_lower:
        tags.append("classic")
    if "tale" in title_lower or "fiction" in title_lower:
        tags.append("fiction")
    if not tags:
        tags.append("general")
    return tags
