from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Field, Session, SQLModel, create_engine, select

from .models import (
    Author,
    Book,
    # Books_Authors,
    AuthorRead,
    BookRead,
    BookReadNested,
    AuthorReadNested,
)


sqlite_file_name = "library.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@app.post("/books/")
def create_book(book: Book, session: SessionDep) -> Book:
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@app.post("/authors/")
def create_author(author: Author, session: SessionDep) -> Author:
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@app.get("/books/", response_model=list[BookRead])
def read_books(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Book]:
    books = session.exec(select(Book).offset(offset).limit(limit)).all()
    return [
        BookRead(
            id=b.id,
            name=b.name,
            sinopsys=b.sinopsys,
            authors=[
                AuthorReadNested(
                    id=a.author.id,
                    first_name=a.author.first_name,
                    last_name=a.author.last_name,
                    birthdate=a.author.birthdate,
                )
                for a in b.bookauthors
            ],
        )
        for b in books
    ]


@app.get("/authors/", response_model=list[AuthorRead])
def read_authors(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    authors = session.exec(select(Author).offset(offset).limit(limit)).all()
    return [
        AuthorRead(
            id=a.id,
            first_name=a.first_name,
            last_name=a.last_name,
            birthdate=a.birthdate,
            books=[
                BookReadNested(id=b.book.id, name=b.book.name, sinopsys=b.book.sinopsys)
                for b in a.bookauthors
            ],
        )
        for a in authors
    ]


@app.get("/authors/{author_id}")
def read_author(author_id: int, session: SessionDep) -> Author:
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.get("/books/{book_id}")
def read_book(book_id: int, session: SessionDep) -> Book:
    book = session.get(Author, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, session: SessionDep):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    session.delete(book)
    session.commit()
    return {"ok": True}
