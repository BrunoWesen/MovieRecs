import os

import pymongo
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DB_URI: str = os.getenv("DATABASE_URI")

client = pymongo.MongoClient(DB_URI)
client.drop_database("movies_db")
db = client["movies_db"]

collections = ["titles", "crew", "principals_part1", "principals_part2", "ratings"]

for idx, collection in enumerate(collections):
    path = os.path.join("Data", collection + ".parquet")
    print(f"lendo a coleção: {collection}")
    df = pd.read_parquet(path)
    print("inserindo no banco de dados")
    collection = "principals" if "principals" in collection else collection
    db[collection].insert_many(df.to_dict(orient="records"))
    print(f'{idx + 1} de {len(collections)} concluídos.\n')
