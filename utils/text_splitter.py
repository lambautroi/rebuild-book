# Chia chương & chia chunk tối ưu với tiktoken
import re
from typing import List, Dict
import tiktoken

def split_into_chapters(text: str) -> List[Dict[str, str]]:
    """
    Tách text thành các chương dựa trên nhiều kiểu tiêu đề chương phổ biến.
    Hỗ trợ: Chapter, Book, Part, Section, Canto...
    Trả về: [{"title": str, "content": str}, ...]
    """
    # Gộp nhiều mẫu tiêu đề chương
    heading_pattern = r"(?:Chapter|CHAPTER|Chap\.?|Book|BOOK|Part|PART|Section|SECTION|Canto|CANTO)\s+(?:[IVXLC\d]+|One|Two|Three|First|Second|Third)\b[^\n]*"

    pattern = re.compile(rf"(^|\n)\s*({heading_pattern})", re.IGNORECASE)

    matches = list(pattern.finditer(text))

    if not matches:
        return [{"title": "Full Text", "content": text.strip()}]

    chapters = []
    for i, match in enumerate(matches):
        start = match.end()
        title = match.group(2).strip()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        chapters.append({
            "title": title,
            "content": content
        })

    return chapters


def chunk_text_tiktoken(text: str, max_tokens: int = 1500) -> List[str]:
    """
    Chia nhỏ đoạn text thành các chunks token nhỏ
    Sử dụng tiktoken để chia chính xác theo token model
    """
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = enc.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk = enc.decode(tokens[i:i+max_tokens])
        chunks.append(chunk)
    return chunks

def split_and_chunk_text(text: str, max_tokens: int = 1500) -> List[Dict[str, List[str]]]:
    """
    Tách chương và chia nhỏ thành các chunk với tối đa max_tokens token mỗi chunk.
    Trả về list chứa dict {"title": str, "chunks": List[str]} cho mỗi chương.
    """
    chapters = split_into_chapters(text)
    result = []
    
    for chapter in chapters:
        chunks = chunk_text_tiktoken(chapter["content"], max_tokens)
        result.append({
            "title": chapter["title"],
            "chunks": chunks
        })
    
    return result

# ...existing code...

if __name__ == "__main__":
    # Ví dụ về văn bản sách
    text = """
    2 chuong sách mẫu:
    BOOK I.
    It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.
    
                BOOK II.
    However little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered the rightful property of some one or other of their daughters.
    """

    # Tách chương và chia chunk
    chapters_with_chunks = split_and_chunk_text(text, max_tokens=1500)

    # In kết quả
    for chapter in chapters_with_chunks:
        print(f"Title: {chapter['title']}")
        print(f"Number of chunks: {len(chapter['chunks'])}")
        print(f"First chunk preview: {chapter['chunks'][0][:100]}...\n")