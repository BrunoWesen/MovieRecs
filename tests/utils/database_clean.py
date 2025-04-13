# Como não tem um database próprio para testes esse arquivo foi feito para apagar os usuários criado pelos testes.

import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

DB_URI: str = os.getenv("DATABASE_URI")
client = MongoClient(DB_URI)
db = client["movies_db"]

def delete_test_users():
    # Executa a deleção dos documentos onde username é "testUser"
    result = db.users.delete_many({"username": "testUser"})

    # Exibe quantos documentos foram deletados
    print(f"Deletados {result.deleted_count} documentos.")

if __name__ == "__main__":
    delete_test_users()