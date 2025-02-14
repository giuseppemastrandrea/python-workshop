"""
    Start from scratch: 
    - Primi passi (setup struttura)
    - Validazione di base -> Pydantic
    - Query parameters vs path parameters -> Query, Path
    - Simple CRUD
    - Validation with pydantic

"""

from typing import Annotated, Literal

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field


"""
Questo è l'item base PRIMA di mostrare la validation
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
"""


class Author(BaseModel):
    first_name: str
    last_name: str
    birth_date: str


app = FastAPI()


@app.get("/authors/")
async def get_authors():
    return {
        "authors": [
            {"first_name": "John", "last_name": "Doe", "birth_date": "1990-01-01"}
        ]
    }
