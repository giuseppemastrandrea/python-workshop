from fastapi import FastAPI
from .database import create_db
from .views import router

app = FastAPI()


# Creiamo il database al primo avvio
@app.on_event("startup")
def startup():
    create_db()


# Registriamo le API
app.include_router(router, prefix="/api")
