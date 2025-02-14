from typing import Annotated, Literal

from fastapi import FastAPI, Path, Query, Depends
from pydantic import BaseModel, Field
from sqlmodel import create_engine, Session, select


from .models import Author

sqlite_file_name = "library.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.post("/authors/")
def create_book(author: Author, session: SessionDep) -> Author:
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@app.get("/authors/")
def create_book(session: SessionDep) -> list[Author]:
    authors = session.exec(select(Author)).all()
    return authors


# @app.delete("/authors/{author_id}")


# @app.put("/authors/{author_id}")
