from typing import List, Optional
from sqlmodel import SQLModel


# 🔹 Modelli per gli Autori
class AuthorBase(SQLModel):
    first_name: str
    last_name: str
    birthdate: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int
    books: List["BookBase"] = []


# 🔹 Modelli per i Libri
class BookBase(SQLModel):
    title: str
    published_date: Optional[str] = None


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    id: int
    authors: List[AuthorBase] = []
