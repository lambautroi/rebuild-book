import uuid
from pipeline.book_rewrite_pipeline import run_full_pipeline

def test_run_full_pipeline():
    # Dữ liệu mẫu
    book_id = str(uuid.uuid4())
    title = "Test Book"
    author = "Test Author"
    tags = ["test", "fiction"]
    source = "manual"
    raw_text = """
    BOOK I.
    This is the first chapter. It is only a test.
                    BOOK II.
    This is the second chapter. Still testing.
    """
    chapters = [
        {"title": "BOOK I.", "content": "This is the first chapter. It is only a test."},
        {"title": " BOOK II.", "content": "This is the second chapter. Still testing."}
    ]
    style_description = "simple and clear"

    # Gọi pipeline
    run_full_pipeline(
        book_id=book_id,
        title=title,
        author=author,
        tags=tags,
        source=source,
        raw_text=raw_text,
        chapters=chapters,
        style_description=style_description
    )

if __name__ == "__main__":
    test_run_full_pipeline()
    print("✅ Đã chạy xong test pipeline (kiểm tra Firestore để xác nhận kết quả).")