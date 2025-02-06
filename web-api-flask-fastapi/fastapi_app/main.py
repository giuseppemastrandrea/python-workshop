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

from .db import Hero


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


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None
    tags: list[str] = []
    author: Author | None = None


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item


@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


"""
@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None,
    user: User | None = None
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

    
    payload nella richiesta HTTP: 
    {
        "item": {
            "name": "Foo",
            "description": "The pretender",
            "price": 42.0,
            "tax": 3.2
        },
        "user": {
            "username": "dave",
            "full_name": "Dave Grohl"
        }
    }
"""


@app.get("/items/")
async def get_items(query: Annotated[FilterParams, Query()]):
    return query


@app.get("/items/{item_id}")
async def get_item(
    item_id: Annotated[str, Path(title="L'ID dell'oggetto che vogliamo")],
    q: str | None = None,
):
    results = {"item_id": item_id}
    if q:
        return {"q": q}
    return results
