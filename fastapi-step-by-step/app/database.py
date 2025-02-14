from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=True)


# 🔹 Funzione per creare il database
def create_db():
    SQLModel.metadata.create_all(engine)


# 🔹 Funzione per ottenere una sessione del database
def get_session():
    with Session(engine) as session:
        yield session
