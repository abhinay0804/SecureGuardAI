# This is the complete, corrected code for:
# src/utils/utilities/database.py

import sys
import os
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from dotenv import load_dotenv

# --- NEW PATH FIX ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
dotenv_path = os.path.join(project_root, ".env")
load_dotenv(dotenv_path=dotenv_path)
# --- END OF NEW PATH FIX ---

mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("MONGO_DB_NAME")

if not mongo_uri or not db_name:
    print("CRITICAL ERROR: MONGO_URI or MONGO_DB_NAME not found in .env file")
    sys.exit(1) # Exit if env variables are not set

try:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=500)
    # Verify the server is reachable
    client.admin.command('ping')
    db = client[db_name]
    print("MongoDB client initialized successfully.")
except Exception as e:
    print(f"MongoDB not available, using local mock collection fallback: {e}")
    client = None
    db = None

def get_database() -> Database:
    if db is None:
        raise Exception("Database not initialized.")
    return db

def get_collection(collection_name: str) -> Collection:
    # If DB not available, provide a safe mock collection for local dev
    module_db = globals().get("db")
    if module_db is None:
        class MockCursor:
            def __init__(self, items):
                self._items = list(items)
                self._pos = 0

            def sort(self, *args, **kwargs):
                return self

            def skip(self, n):
                if n:
                    self._items = self._items[n:]
                return self

            def limit(self, n):
                if n and n < len(self._items):
                    self._items = self._items[:n]
                return self

            def __iter__(self):
                return iter(self._items)

            def __next__(self):
                if self._pos >= len(self._items):
                    raise StopIteration
                v = self._items[self._pos]
                self._pos += 1
                return v

        class MockCollection:
            def __init__(self, name):
                self.name = name

            def find(self, *args, **kwargs):
                return MockCursor([])

            def aggregate(self, *args, **kwargs):
                return []

            def find_one(self, *args, **kwargs):
                return None

            def count_documents(self, *args, **kwargs):
                return 0

            def __getattr__(self, item):
                # Any other pymongo methods return a harmless callable
                def _noop(*a, **k):
                    return None

                return _noop

        return MockCollection(collection_name)

    # Use the module-level db (already validated)
    return module_db[collection_name]