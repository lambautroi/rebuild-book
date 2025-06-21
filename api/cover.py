from fastapi import APIRouter
from pydantic import BaseModel
from google.cloud import firestore

router = APIRouter()
db = firestore.Client()

class BookRequest(BaseModel):
    book_id: str

@router.post("/api/trigger_cover")
def trigger_cover(data: BookRequest):
    book_id = data.book_id
    book_ref = db.collection("books").document(book_id)
    book_ref.update({
        "cover.status": "pending"
    })
    return {"message": f"Book {book_id} marked as pending for cover generation."}

@router.get("/api/cover_status/{book_id}")
def get_cover_status(book_id: str):
    doc = db.collection("books").document(book_id).get()
    if not doc.exists:
        return {"error": "Book not found"}
    return doc.to_dict().get("cover", {})
