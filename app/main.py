import os

from dotenv import load_dotenv
from fastapi import FastAPI
from app.controllers import movie_controller, user_controller

load_dotenv()

HOST: str = os.getenv("HOST")
PORT: int = int(os.getenv("PORT"))

app: FastAPI = FastAPI()

app.include_router(movie_controller.router, prefix="/filmes", tags=["Filmes"])
app.include_router(user_controller.router, prefix="/usuarios", tags=["Usuários"])

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
