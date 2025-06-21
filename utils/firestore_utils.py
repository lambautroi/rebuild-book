from google.cloud import firestore

db = firestore.Client()

def save_book_text(book_id: str, cleaned_text: str, chapters: list):
    book_ref = db.collection("books").document(book_id)
    book_ref.set({"originalText": cleaned_text}, merge=True)

    chapters_ref = book_ref.collection("chapters")
    for i, ch in enumerate(chapters):
        chapters_ref.document(f"chapter_{i+1}").set(ch)
