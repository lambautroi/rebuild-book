import requests
import re
from bs4 import BeautifulSoup

ARCHIVE_SEARCH_URL = "https://archive.org/advancedsearch.php"

def search_archive(keyword: str, max_results: int = 10):
    """Tìm sách theo từ khóa trên Archive.org"""
    params = {
        "q": f"{keyword} AND mediatype:texts",
        "fl[]": "identifier,title,creator",
        "rows": max_results,
        "page": 1,
        "output": "json"
    }
    response = requests.get(ARCHIVE_SEARCH_URL, params=params)
    data = response.json()
    books = []
    for doc in data["response"]["docs"]:
        books.append({
            "identifier": doc["identifier"],
            "title": doc.get("title", "Unknown"),
            "author": doc.get("creator", ["Unknown"])[0] if isinstance(doc.get("creator"), list) else doc.get("creator"),
            "url": f"https://archive.org/details/{doc['identifier']}"
        })
    return books

def get_txt_url(identifier: str):
    """Tìm link file TXT phù hợp"""
    item_url = f"https://archive.org/download/{identifier}/"
    response = requests.get(item_url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [a.get("href") for a in soup.find_all("a", href=True)]
    for link in links:
        if link.endswith("_djvu.txt"):  # dạng OCR text
            return item_url + link
        elif link.endswith(".txt"):
            return item_url + link
    return None

def download_book(identifier: str, preferred_fmts=("txt", "epub", "html")) -> str:
    item_url = f"https://archive.org/download/{identifier}/"
    response = requests.get(item_url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [a.get("href") for a in soup.find_all("a", href=True)]

    for fmt in preferred_fmts:
        for link in links:
            if fmt == "txt" and (link.endswith(".txt") or "_djvu.txt" in link):
                url = item_url + link
                print(f"✅ Đang tải {fmt} từ Archive.org: {url}")
                return requests.get(url).text
            if fmt == "epub" and link.endswith(".epub"):
                url = item_url + link
                print(f"✅ Đang tải {fmt} từ Archive.org: {url}")
                return requests.get(url).content.decode("utf-8", errors="ignore")
            if fmt == "html" and link.endswith(".htm") or link.endswith(".html"):
                url = item_url + link
                print(f"✅ Đang tải {fmt} từ Archive.org: {url}")
                return requests.get(url).text

    raise Exception(f"❌ Không tìm được định dạng phù hợp cho sách {identifier}")



def auto_tag(title: str, author: str) -> list:
    """Gắn tag đơn giản dựa trên tiêu đề hoặc tác giả"""
    tags = []
    title_lower = title.lower()
    if any(k in title_lower for k in ["history", "philosophy", "essay"]):
        tags.append("philosophy")
    if any(k in title_lower for k in ["novel", "classic", "literature"]):
        tags.append("classic")
    if any(k in title_lower for k in ["story", "tale", "fiction"]):
        tags.append("fiction")
    if not tags:
        tags.append("general")
    return tags
