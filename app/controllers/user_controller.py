from typing import List, Optional, Union

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException, Query

from app.schemas.user import UserResponse, UserCreate
from app.schemas.watched_movie import WatchedMovie
from app.services.user_service import UserService

router = APIRouter()


@router.post("/", response_model=UserResponse)
def add_user(user: UserCreate):
    """
    Cria um novo usuário com ID único, username e a lista de filmes assistidos.
    """
    user_dict: dict = user.model_dump(exclude={"id"})
    inserted_id: Union[str, None] = UserService.create_user(user_dict)
    if inserted_id is None:
        raise HTTPException(status_code=400, detail="User ID already exists")
    return UserService.get_user_by_userid(ObjectId(inserted_id))


@router.get("/", response_model=List[UserResponse])
def list_users(username: Optional[str] = Query(None, description="username do usuário, ex: 'FelipeHay12'"),
               page: int = Query(1, gt=0), limit: int = Query(100, gt=0)):
    """
    Endpoint para listar os usuários com paginação.
    Retorna 100 registros por padrão.
    """
    movies: List[UserResponse] = UserService.get_all_users(username, page, limit)
    return movies


@router.get("/{usuario_id}", response_model=UserResponse)
def get_user(usuario_id: str):
    """
    Retorna os dados do usuário especificado pelo ID do usuário.
    """
    try:
        user: UserResponse = UserService.get_user_by_userid(ObjectId(usuario_id))
    except InvalidId:
        raise HTTPException(status_code=404, detail="Id inválido")

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return user


@router.put("/{usuario_id}/assistidos", response_model=UserResponse)
def update_watched_movie(usuario_id: str, movie: WatchedMovie):
    """
    Adiciona ou atualiza um filme assistido para o usuário.
    Se o filme já existir na lista, apenas atualiza a avaliação.
    """
    try:
        updated_user: UserResponse = UserService.update_user_watched_movie(ObjectId(usuario_id), movie)
    except InvalidId:
        raise HTTPException(status_code=404, detail="Id inválido")

    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return updated_user
