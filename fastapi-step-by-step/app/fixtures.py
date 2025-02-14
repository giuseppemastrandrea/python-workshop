from sqlmodel import Session
from app.database import engine, create_db
from app.models import Author, Book, AuthorBookLink


def load_fixtures():
    """Carica dati di test nel database."""
    with Session(engine) as session:
        # 📌 Creiamo alcuni autori
        author1 = Author(first_name="Umberto", last_name="Eco", birthdate="1932-01-05")
        author2 = Author(
            first_name="George", last_name="Orwell", birthdate="1903-06-25"
        )
        author3 = Author(
            first_name="J.R.R.", last_name="Tolkien", birthdate="1892-01-03"
        )

        # 📌 Creiamo alcuni libri
        book1 = Book(title="Il Nome della Rosa", published_date="1980-01-01")
        book2 = Book(title="1984", published_date="1949-06-08")
        book3 = Book(title="Il Signore degli Anelli", published_date="1954-07-29")

        # 📌 Creiamo le relazioni tra autori e libri
        book1.authors.append(author1)  # Umberto Eco ha scritto "Il Nome della Rosa"
        book2.authors.append(author2)  # George Orwell ha scritto "1984"

        session.add_all([author1, author2, author3, book1, book2, book3])
        session.commit()


# Eseguiamo lo script se viene chiamato direttamente
if __name__ == "__main__":
    create_db()
    load_fixtures()
