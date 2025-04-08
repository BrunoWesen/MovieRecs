from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["movies_db"]

db.users.create_index("id", unique=True)
