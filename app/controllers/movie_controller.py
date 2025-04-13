from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional

from app.schemas.movie import Movie
from app.services.movie_service import MovieService

router = APIRouter()


@router.get("/", response_model=List[Movie])
def list_movies(title: Optional[str] = Query(None, description="Título para pesquisa, ex: 'Django Unchained'"),
                page: int = Query(1, gt=0), limit: int = Query(100, gt=0)):
    """
    Endpoint para listar os filmes com paginação.
    Retorna 100 registros por padrão.
    """
    movies: List[Movie] = MovieService.get_all_movies(title, page, limit)
    return movies


@router.get("/{usuario_id}/recomendacoes", response_model=List[Movie])
def get_recommendations(usuario_id: str, limit: int = Query(15, gt=0)):
    """
    Retorna uma lista de filmes recomendados ao usuário.
    """
    try:
        movies = MovieService.get_recommended_movies(ObjectId(usuario_id), limit)
    except InvalidId:
        raise HTTPException(status_code=404, detail="Id inválido.")

    if movies is None or len(movies) == 0:
        raise HTTPException(status_code=404, detail="Nenhuma recomendação encontrada ou usuário não encontrado.")
    return movies
