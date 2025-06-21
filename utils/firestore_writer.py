from google.cloud import firestore
from datetime import datetime

db = firestore.Client()

def save_book_full(book_id, title, author, tags, source, full_text, chapters, summary, styles, cover):
    book_ref = db.collection("books").document(book_id)
    book_ref.set({
        "title": title,
        "author": author,
        "tags": tags,
        "source": source,
        "createdAt": datetime.utcnow(),
        "rawText": full_text,
        "summary": summary,
        "styles": styles,
        "cover": cover
    })

    # Lưu từng chương vào subcollection
    chapters_ref = book_ref.collection("rewrittenChapters")
    for idx, chapter in enumerate(chapters, start=1):
        chapters_ref.document(f"chapter_{idx}").set({
            "title": chapter.get("title", f"Chapter {idx}"),
            "content": " ".join(chapter["content"]),
            "style": "rewritten"
        })


    chapters_ref = book_ref.collection("chapters")
    for idx, chapter in enumerate(chapters, start=1):
        chapters_ref.document(f"chapter_{idx}").set({
            "title": chapter.get("title", f"Chapter {idx}"),
            "content": chapter.get("content", ""),
            "style": "rewritten"
        })

def auto_style_from_tags(tags: list) -> str:
    if "fantasy" in tags:
        return "fantasy illustrated"
    elif "romance" in tags:
        return "minimalist soft tone"
    elif "philosophy" in tags:
        return "classic vintage"
    else:
        return "modern clean"
