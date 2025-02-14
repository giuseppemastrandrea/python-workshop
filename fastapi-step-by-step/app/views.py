from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from .database import get_session
from .models import Author, Book, AuthorBookLink
from .schemas import AuthorRead, AuthorCreate, BookRead, BookCreate
from typing import List

router = APIRouter()


# 🔹 API per gli Autori
"""
@router.get("/authors/", response_model=List[AuthorRead])
def get_authors(session: Session = Depends(get_session)):
    return session.exec(select(Author)).all()
"""


@router.get("/authors/", response_model=List[AuthorRead])
def get_authors(session: Session = Depends(get_session)):
    authors = session.exec(select(Author)).all()
    for author in authors:
        author.books = session.exec(
            select(Book)
            .join(AuthorBookLink)
            .where(AuthorBookLink.author_id == author.id)
        ).all()
    return authors


@router.post("/authors/", response_model=AuthorRead)
def create_author(author: AuthorCreate, session: Session = Depends(get_session)):
    new_author = Author(**author.dict())
    session.add(new_author)
    session.commit()
    session.refresh(new_author)
    return new_author


@router.get("/authors/{author_id}", response_model=AuthorRead)
def get_author(author_id: int, session: Session = Depends(get_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Autore non trovato")
    return author


@router.delete("/authors/{author_id}", status_code=204)
def delete_author(author_id: int, session: Session = Depends(get_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Autore non trovato")
    session.delete(author)
    session.commit()


# 🔹 API per i Libri
@router.get("/books/", response_model=List[BookRead])
def get_books(session: Session = Depends(get_session)):
    return session.exec(select(Book)).all()


@router.post("/books/", response_model=BookRead)
def create_book(book: BookCreate, session: Session = Depends(get_session)):
    new_book = Book(**book.dict())
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book


@router.get("/books/{book_id}", response_model=BookRead)
def get_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Libro non trovato")
    return book


@router.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Libro non trovato")
    session.delete(book)
    session.commit()
