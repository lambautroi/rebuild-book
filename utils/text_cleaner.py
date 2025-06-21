import re
from bs4 import BeautifulSoup
from cleantext import clean

def clean_html(raw_text: str) -> str:
    """Loại bỏ HTML tags nếu còn"""
    return BeautifulSoup(raw_text, "html.parser").get_text()

def remove_headers_footers(text: str) -> str:
    """Loại bỏ header/footer hoặc số trang"""
    # Xóa dòng toàn số (page number)
    text = re.sub(r"(?m)^\s*\d+\s*$", "", text)
    # Xóa dòng in hoa toàn bộ (header/thẻ mục lục)
    text = re.sub(r"(?m)^\s*[A-Z\s]{6,}\s*$", "", text)
    return text

def normalize_spacing(text: str) -> str:
    """Chuẩn hóa khoảng trắng"""
    text = re.sub(r"\n{2,}", "\n\n", text)  # gộp nhiều dòng trống
    text = re.sub(r"[ \t]+", " ", text)    # bỏ tab/thừa khoảng trắng
    return text.strip()

def clean_text(raw_text: str) -> str:
    """Làm sạch tổng thể văn bản"""
    text = clean_html(raw_text)
    text = remove_headers_footers(text)
    text = normalize_spacing(text)
    text = clean(text,
                 no_urls=True,
                 no_emails=True,
                 no_phone_numbers=True,
                 no_currency_symbols=True,
                 no_line_breaks=False,
                 lang="en")
    return text
