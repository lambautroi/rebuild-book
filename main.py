import uuid
import argparse
import requests
import os
from fastapi import FastAPI
from google.cloud import firestore

# Import từ các module trong hệ thống
from utils.source_gutenberg import search_gutenberg, download_book as download_gutenberg, auto_tag as tag_gutenberg
from utils.source_archive import search_archive, download_book as download_archive, auto_tag as tag_archive
from utils.source_standardebooks import search_standard_ebooks, download_book as download_standardebooks, auto_tag as tag_standard
from utils.text_splitter import split_into_chapters
from pipeline.book_rewrite_pipeline import run_full_pipeline
from utils.epub_generator import generate_epub
from utils.text_cleaner import clean_text


from api.cover import router as cover_router

app = FastAPI()
# Đăng ký router cho API cover
app.include_router(cover_router)

# =====================
# Hàm hỗ trợ chọn nguồn
# =====================
def load_book_from_source(source: str, keyword: str):
    if source == "gutenberg":
        results = search_gutenberg(keyword, max_results=1)
        if not results:
            raise Exception("Không tìm thấy sách từ Gutenberg.")
        book = results[0]
        content = download_gutenberg(book["book_id"])
        tags = tag_gutenberg(book["title"], book["author"])
        return book["title"], book["author"], content, tags

    elif source == "archive":
        results = search_archive(keyword, max_results=1)
        if not results:
            raise Exception("Không tìm thấy sách từ Archive.org.")
        book = results[0]
        content = download_archive(book["identifier"])
        tags = tag_archive(book["title"], book["author"])
        return book["title"], book["author"], content, tags

    elif source == "standardebooks":
        results = search_standard_ebooks(keyword, max_results=1)
        if not results:
            raise Exception("Không tìm thấy sách từ Standard Ebooks.")
        book = results[0]
        content_bytes = download_standardebooks(book["slug"])
        content = content_bytes.decode("utf-8")
        tags = tag_standard(book["title"], book["author"])
        return book["title"], book["author"], content, tags

    else:
        raise ValueError("Nguồn không hợp lệ. Dùng: gutenberg, archive, standardebooks.")

# ====================
# MAIN ENTRY POINT
# ====================
def main():
    parser = argparse.ArgumentParser(description="RebuildBook - Rewrite Public Domain Books")
    parser.add_argument("--source", type=str, required=True, help="Nguồn sách: gutenberg | archive | standardebooks")
    parser.add_argument("--keyword", type=str, required=True, help="Từ khóa tìm sách (ví dụ: 'tolstoy')")
    parser.add_argument("--style", type=str, default="formal and elegant literary", help="Mô tả phong cách muốn viết lại")

    args = parser.parse_args()
    source = args.source.lower()
    keyword = args.keyword
    style = args.style

    print(f"🟢 Đang tìm và tải sách từ nguồn: {source} với từ khóa: '{keyword}'")

    # 1. Tải sách
    title, author, raw_text, tags = load_book_from_source(source, keyword)
    print(f"✅ Đã tải sách: '{title}' bởi {author}")
    
    # 1.5 Làm sạch văn bản
    raw_text = clean_text(raw_text)
    print("🧼 Đã làm sạch nội dung văn bản")

    # 2. Tách chương
    chapters = split_into_chapters(raw_text)
    print(f"📚 Số chương tách được: {len(chapters)}")

    # 3. Tạo ID sách
    book_id = str(uuid.uuid4())

    # 4. Gọi pipeline viết lại sách
    run_full_pipeline(
        book_id=book_id,
        title=title,
        author=author,
        tags=tags,
        source=source,
        raw_text=raw_text,
        chapters=chapters,
        style_description=style
    )

    print(f"🎉 Pipeline hoàn tất. Sách đã lưu với ID: {book_id}")

    # ===== Giai đoạn 4: Tạo EPUB =====
    print("📦 Bắt đầu tạo file EPUB...")

    db = firestore.Client()
    book_ref = db.collection("books").document(book_id)
    book_doc = book_ref.get()

    if not book_doc.exists:
        print("❌ Không tìm thấy sách để tạo EPUB.")
        return

    data = book_doc.to_dict()
    chapters_snapshots = db.collection("books").document(book_id).collection("rewrittenChapters").stream()
    chapters_rewritten = [
        doc.to_dict() for doc in sorted(chapters_snapshots, key=lambda d: d.id)
    ]
    cover_url = data.get("cover", {}).get("finalUrl")
    title_epub = f"{title} – Modern Style"
    author_epub = f"{author}, Rewritten by RebuildBook AI"

    # Tải ảnh cover nếu có
    cover_path = None
    if cover_url:
        os.makedirs("temp", exist_ok=True)
        cover_path = f"temp/{book_id}_cover.jpg"
        with open(cover_path, "wb") as f:
            f.write(requests.get(cover_url).content)

    # Tạo EPUB
    epub_path = generate_epub(book_id, "default", title_epub, author_epub, cover_path, chapters_rewritten)

    # Upload EPUB
    from google.cloud import storage
    client = storage.Client()
    bucket = client.bucket("rebuildbook-2b609.firebasestorage.app")
    blob = bucket.blob(f"books/{book_id}/book.epub")
    blob.upload_from_filename(epub_path)
    blob.make_public()
    epub_url = blob.public_url

    # Cập nhật vào Firestore
    book_ref.update({"epubUrl": epub_url})
    print(f"✅ EPUB đã được tạo và upload thành công: {epub_url}")


# ====================
# Chạy main
# ====================
if __name__ == "__main__":
    main()
