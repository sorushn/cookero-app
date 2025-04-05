from neo4j import GraphDatabase
from backend.app.settings import settings
import contextlib

DB_host = settings.get("database", "DB_HOST")
DB_port = settings.get("database", "DB_PORT")
URI = f"neo4j://{DB_host}:{DB_port}"
USERNAME = settings.get("database", "DB_USER")
PASSWORD = settings.get("database", "DB_PASSWORD")

DB_name = settings.get("database", "DB_NAME")
driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
if driver.verify_connectivity():
    print("Connected to Neo4j")
    with driver.session(database=DB_name) as session:
        session.run(f"USE {DB_name}")


@contextlib.contextmanager
def get_session():
    yield driver.session(database=DB_name)
