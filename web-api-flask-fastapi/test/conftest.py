import pytest
from sqlalchemy import create_async_session
from project.config import FLASK_APP, FASTAPI_APP
import json


@pytest.fixture(scope="function")
def fixture_book_data():
    with open("fixtures/book_data.json") as f:
        return json.load(f)
