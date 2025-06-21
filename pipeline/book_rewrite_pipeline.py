# pipeline/book_rewrite_pipeline.py
import os
from utils.openai_rewriter import rewrite_text_with_style
from utils.firestore_writer import save_book_full, auto_style_from_tags
from utils.text_splitter import split_and_chunk_text
from utils.summary_generator import generate_summary
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_full_pipeline(book_id: str, title: str, author: str, tags: list,
                      source: str, raw_text: str, chapters: list,
                      style_description: str):
    """
    Pipeline xử lý cuốn sách từ đầu đến cuối:
    - Tách chương và chia thành các chunk
    - Gửi các chunk đến OpenAI API để viết lại theo phong cách
    - Lưu kết quả vào Firestore
    """
    logger.info(f"Starting pipeline for book: {title}")
    
    # 1. Tạo đường dẫn cache cho từng cuốn sách
    cache_path = f"cache/{book_id}_cache.json"
    os.makedirs("cache", exist_ok=True)
    
    # 2. Tách chương và chia chunk
    logger.info("Splitting and chunking the text into chapters...")
    chapters_with_chunks = split_and_chunk_text(raw_text)
    
    rewritten_chapters = []
    total_chunks = sum([len(chapter["chunks"]) for chapter in chapters_with_chunks])
    logger.info(f"Total chunks to process: {total_chunks}")
    
    # 3. Gửi từng chunk đến OpenAI để viết lại theo phong cách
    cache = {}  # Cache để lưu kết quả đã viết lại
    chunk_counter = 0  # Đếm số lượng chunk đã xử lý

    for chapter in chapters_with_chunks:
        chapter_rewritten = {"title": chapter["title"], "content": []}
        
        for chunk in chapter["chunks"]:
            chunk_counter += 1
            logger.info(f"Processing chunk {chunk_counter}/{total_chunks} for chapter '{chapter['title']}'")

            # Gọi hàm viết lại từng chunk với OpenAI API
            rewritten_chunk = rewrite_text_with_style(chunk, style_description, cache_path)
            chapter_rewritten["content"].append(rewritten_chunk)
        
        rewritten_chapters.append(chapter_rewritten)
    
    # 4. Tạo bản tóm tắt sách
    # 4. Tạo tóm tắt sách theo từng chương
    logger.info("Generating summary for each chapter...")

    chapter_summaries = []
    for idx, ch in enumerate(rewritten_chapters, start=1):
        chapter_text = " ".join(ch["content"])
        logger.info(f"→ Tóm tắt chương {idx}: {ch['title'][:30]}...")
        try:
            summary_chapter = generate_summary(chapter_text, max_tokens=300)
            chapter_summaries.append(f"{ch['title']}: {summary_chapter}")
        except Exception as e:
            logger.warning(f"⚠️ Lỗi khi tóm tắt chương {idx}: {e}")
            chapter_summaries.append(f"{ch['title']}: (Không tóm tắt được)")

    # Gộp lại và tóm tắt cấp cao toàn bộ sách
    logger.info("Generating overall summary from all chapter summaries...")
    try:
        summary = generate_summary("\n".join(chapter_summaries), max_tokens=500)
    except Exception as e:
        logger.warning(f"⚠️ Lỗi khi tóm tắt toàn bộ sách: {e}")
        summary = "(Không thể tạo tóm tắt)"

    
    # 5. Lưu sách vào Firestore
    logger.info("Saving book and chapters to Firestore...")
    style = auto_style_from_tags(tags)
    save_book_full(
        book_id,
        title,
        author,
        tags,
        source,
        " ".join([" ".join(ch["content"]) for ch in rewritten_chapters]),
        rewritten_chapters,  # lưu vào trường "rewrittenChapters" trong document chính
        summary,
        styles=[style_description],
        cover={
            "status": "pending",
            "style": style
        }
    )

    
    logger.info("Pipeline completed and saved to Firestore.")


