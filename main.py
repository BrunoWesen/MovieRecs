from fastapi import FastAPI
from controllers import movie_controller, user_controller

app = FastAPI()

app.include_router(movie_controller.router, prefix="/filmes", tags=["Filmes"])
app.include_router(user_controller.router, prefix="/usuarios", tags=["Usuários"])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
