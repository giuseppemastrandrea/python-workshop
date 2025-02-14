from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


# 🔹 Modello di relazione tra Autori e Libri (Many-to-Many)
class AuthorBookLink(SQLModel, table=True):
    author_id: Optional[int] = Field(
        default=None, foreign_key="author.id", primary_key=True
    )
    book_id: Optional[int] = Field(
        default=None, foreign_key="book.id", primary_key=True
    )


# 🔹 Modello Autore
class Author(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    birthdate: Optional[str] = None  # Usato come stringa per semplicità

    books: List["Book"] = Relationship(
        back_populates="authors", link_model=AuthorBookLink
    )


# 🔹 Modello Libro
class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    published_date: Optional[str] = None  # Usato come stringa per semplicità

    authors: List[Author] = Relationship(
        back_populates="books", link_model=AuthorBookLink
    )
