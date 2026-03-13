import os
from neo4j import GraphDatabase
from .queries import KnowledgeGraphClient
from dotenv import load_dotenv

load_dotenv()

class KGManager:
    """Singleton manager for Neo4j driver and client."""
    _driver = None
    _client = None

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            uri = os.getenv("NEO4J_URI")
            user = os.getenv("NEO4J_USERNAME")
            password = os.getenv("NEO4J_PASSWORD")
            cls._driver = GraphDatabase.driver(uri, auth=(user, password))
        return cls._driver

    @classmethod
    def get_client(cls) -> KnowledgeGraphClient:
        if cls._client is None:
            cls._client = KnowledgeGraphClient(cls.get_driver())
        return cls._client

    @classmethod
    def close(cls):
        if cls._driver:
            cls._driver.close()
            cls._driver = None

def get_kg_client() -> KnowledgeGraphClient:
    return KGManager.get_client()
