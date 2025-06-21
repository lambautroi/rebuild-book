import os
from ebooklib import epub

def generate_epub(book_id, style_id, title, author, cover_path, chapters):
    try:
        book = epub.EpubBook()
        book.set_identifier(book_id)
        book.set_title(title)
        book.set_language('en')
        book.add_author(author)

        # Set cover nếu có
        if cover_path and os.path.exists(cover_path):
            with open(cover_path, 'rb') as img_file:
                book.set_cover("cover.jpg", img_file.read())

        # Tạo danh sách chương
        epub_chapters = []
        for i, chapter in enumerate(chapters):
            c = epub.EpubHtml(
                title=chapter.get("title", f"Chapter {i+1}"),
                file_name=f'chap_{i+1}.xhtml',
                lang='en'
            )
            content = chapter.get("content", "")
            if isinstance(content, list):
                content = " ".join(content)
            c.content = f"<h1>{chapter.get('title', '')}</h1><p>{content}</p>"
            book.add_item(c)
            epub_chapters.append(c)

        # Mục lục và bố cục
        book.toc = tuple(epub_chapters)
        book.spine = ['nav'] + epub_chapters
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # Tạo thư mục output nếu chưa có
        os.makedirs("output", exist_ok=True)
        output_path = f"output/{book_id}_{style_id}.epub"

        # Ghi file EPUB
        epub.write_epub(output_path, book)
        print(f"✅ File EPUB đã tạo: {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Lỗi khi tạo EPUB: {e}")
        return None
