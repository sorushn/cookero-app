import pytest
from backend.app.settings import Settings
from backend.app.core.db import get_session

@pytest.fixture
def settings():
    return Settings("..//settings.ini")

@pytest.fixture
def session(settings):
    with get_session() as session:
        yield session
        session.run("MATCH (n) DETACH DELETE n")