from fastapi import APIRouter, Depends
from app.services.facade import MLBFacade
from app.api.dependencies import get_facade
from app.api.auth_dependencies import auth_current_user
from app.api.schemas.books import BookSearchResponse, BookResponse
from typing import List

# book search function
@router.get("/books/search", response_model=List[BookSearchResponse], status_code=200)
def search_books(
    query: str,
    subject: List[str] | None = None
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
):
    firebase_uid = decoded_token['uid']
    return facade.search_books(query, subject, firebase_uid)

# get book by ID (to return book deets to dashy b)
# this method should offer greater stability for timeline than accessing ext API every time
@router.get("/books/{book_id}", response_model=BookResponse, status_code=200)
def get_book(
    book_id: str,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
):
    firebase_uid = decoded_token['uid']
    return facade.get_book(book_id, firebase_uid)
