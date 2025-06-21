from utils.source_gutenberg import search_gutenberg, download_book, auto_tag

def test_search():
    print("\n=== Test tìm kiếm sách ===\n")
    books = search_gutenberg("tolstoy", max_results=3)
    for i, book in enumerate(books, 1):
        print(f"Kết quả {i}:")
        print(f"  - ID: {book['book_id']}")
        print(f"  - Tiêu đề: {book['title']}")
        print(f"  - Tác giả: {book['author']}")
        print(f"  - URL: {book['url']}")
        print()

def test_download():
    print("\n=== Test tải nội dung sách ===\n")
    # Pride and Prejudice có ID là 1342
    book_id = 1342
    content = download_book(book_id, fmt="txt")
    print(f"Đã tải sách ID {book_id}. Đoạn đầu nội dung:")
    print("---")
    print(content[:500])
    print("---")
    print(f"Tổng số ký tự: {len(content)}")

def test_auto_tag():
    print("\n=== Test gắn tag tự động ===\n")
    test_cases = [
        ("War and Peace", "Leo Tolstoy"),
        ("Pride and Prejudice", "Jane Austen"),
        ("A Tale of Two Cities", "Charles Dickens"),
        ("The Republic", "Plato"),
    ]
    
    for title, author in test_cases:
        tags = auto_tag(title, author)
        print(f"Sách: '{title}' bởi {author}")
        print(f"Tags: {tags}")
        print()

def run_all_tests():
    print("Bắt đầu chạy các test cho source_gutenberg.py\n")
    
    try:
        test_search()
    except Exception as e:
        print(f"Lỗi khi test tìm kiếm: {e}")
    
    try:
        test_download()
    except Exception as e:
        print(f"Lỗi khi test tải sách: {e}")
    
    try:
        test_auto_tag()
    except Exception as e:
        print(f"Lỗi khi test gắn tag: {e}")
    
    print("\nĐã hoàn thành tất cả các test!")

if __name__ == "__main__":
    run_all_tests()