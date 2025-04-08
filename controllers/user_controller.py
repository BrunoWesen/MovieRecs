from fastapi import APIRouter, HTTPException

from schemas.user import User
from schemas.watched_movie import WatchedMovie
from services.user_service import UserService

router = APIRouter()

@router.post("/", response_model=User)
def add_user(user: User):
    """
    Cria um novo usuário com ID único, username e a lista de filmes assistidos.
    """
    user_dict = user.model_dump()
    inserted_id = UserService.create_user(user_dict)
    if inserted_id is None:
        raise HTTPException(status_code=400, detail="User ID already exists")
    return UserService.get_user_by_userid(user.id)


@router.get("/{usuario_id}", response_model=User)
def get_user(usuario_id: str):
    """
    Retorna os dados do usuário especificado pelo ID do usuário.
    """
    user = UserService.get_user_by_userid(usuario_id)
    if not user:
        return {"error": "Usuário não encontrado"}
    return user

@router.put("/{usuario_id}/assistidos", response_model=User)
def update_watched_movie(usuario_id: str, movie: WatchedMovie):
    """
    Adiciona ou atualiza um filme assistido para o usuário.
    Se o filme já existir na lista, apenas atualiza a avaliação.
    """
    updated_user = UserService.update_user_watched_movie(usuario_id, movie)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return updated_user