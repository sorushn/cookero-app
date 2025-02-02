from fastapi import FastAPI
from settings import settings

app = FastAPI(title="Cookero Backend API", description="The backend API for Cookero", version="0.1.0")

from neo4j import GraphDatabase

DB_host = settings.get("database", "DB_HOST")
URI = f"neo4j://localhost:7687"
USERNAME = settings.get("database", "DB_USER")
PASSWORD = settings.get("database", "DB_PASSWORD")

with GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD)) as driver:
    driver.verify_connectivity()