import os

from pymongo import MongoClient

DB_URI: str = os.getenv("DATABASE_URI")
client = MongoClient(DB_URI)
db = client["movies_db"]

db.titles.create_index("tconst", unique=True)