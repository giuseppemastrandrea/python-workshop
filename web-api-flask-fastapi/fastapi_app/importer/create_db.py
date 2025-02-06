import json
from sqlmodel import SQLModel, create_engine, Session
from fastapi_app.models import Author, Books_Authors, Book

# Database configuration
sqlite_file_name = "fastapi_app/library.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


# Create DB function
def create_db():
    SQLModel.metadata.create_all(engine)


# Import data function
def import_data():
    with Session(engine) as session:
        # Import authors
        with open("fastapi_app/fixtures/authors.json", "r") as f:
            authors_data = [Author(**item) for item in json.load(f)]
            session.add_all(authors_data)

        # Import books
        with open("fastapi_app/fixtures/books.json", "r") as f:
            books_data = [Book(**item) for item in json.load(f)]
            session.add_all(books_data)

        # Import books_authors (association)
        with open("fastapi_app/fixtures/books_authors.json", "r") as f:
            books_authors_data = [Books_Authors(**item) for item in json.load(f)]
            session.add_all(books_authors_data)

        session.commit()


# Main function
def main():
    create_db()
    import_data()


if __name__ == "__main__":
    main()
