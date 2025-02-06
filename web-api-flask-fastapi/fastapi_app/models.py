from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


# **Classe base per Author**
class AuthorBase(SQLModel):
    first_name: str
    last_name: str
    birthdate: Optional[str] = None


# **Classe base per Book**
class BookBase(SQLModel):
    name: str
    sinopsys: str


# **Modelli di database (ereditano le basi e aggiungono tabella e relazione)**
class Author(AuthorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bookauthors: List["Books_Authors"] = Relationship(back_populates="author")


class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bookauthors: List["Books_Authors"] = Relationship(back_populates="book")


class Books_Authors(SQLModel, table=True):
    author_id: int = Field(foreign_key="author.id", primary_key=True)
    book_id: int = Field(foreign_key="book.id", primary_key=True)

    author: Author = Relationship(back_populates="bookauthors")
    book: Book = Relationship(back_populates="bookauthors")


# **Modelli di risposta con annidamento**
class AuthorRead(AuthorBase):
    id: int
    books: List["BookReadNested"] = []


class BookRead(BookBase):
    id: int
    authors: List["AuthorReadNested"] = []


# **Modelli annidati**
class AuthorReadNested(AuthorBase):
    id: int


class BookReadNested(BookBase):
    id: int
