import json
from typing import List, Optional
from sqlmodel import SQLModel, create_engine, Session, Field, Relationship
from datetime import date


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


class BooksAuthors(SQLModel, table=True):
    author_id: int = Field(foreign_key="author.id", primary_key=True)
    book_id: int = Field(foreign_key="book.id", primary_key=True)


class Author(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    first_name: str
    last_name: str
    birthdate: Optional[date] = Field(default=None)  # Ora è di tipo date
    books: List["Book"] = Relationship(
        back_populates="authors", link_model=BooksAuthors
    )

    def __init__(self, first_name, last_name, birthdate=None):
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = date.fromisoformat(birthdate) if birthdate else None


class Book(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    sinopsys: str
    authors: List[Author] = Relationship(
        back_populates="books", link_model=BooksAuthors
    )


create_db_and_tables()

with Session(engine) as session:
    with open("fixtures/authors.json", "r") as f:
        authors_data: List[Author] = [
            Author(**item) for item in json.load(f)
        ]  # Usa il costruttore personalizzato e list comprehension
    session.add_all(authors_data)

    with open("fixtures/books.json", "r") as f:
        books_data: List[Book] = json.load(f)
    session.add_all(books_data)

    with open("fixtures/books_authors.json", "r") as f:
        books_authors_data: List[BooksAuthors] = json.load(f)
    session.add_all(books_authors_data)

    session.commit()
