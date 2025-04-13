from typing import Union, List

from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserResponse
from app.schemas.watched_movie import WatchedMovie


class UserService:
    @staticmethod
    def create_user(user_data: dict) -> Union[str, None]:
        try:
            result = UserRepository.insert_one_user(user_data)
            return str(result.inserted_id)
        except DuplicateKeyError:
            return None

    @staticmethod
    def get_all_users(username: str, page: int, limit: int) -> List[UserResponse]:
        skip: int = (page - 1) * limit
        filter_query: dict = {}
        if username:
            filter_query["username"] = {"$regex": username, "$options": "i"}
        users: List[UserResponse] = UserRepository.get_users(skip, filter_query, limit)
        for user in users:
            user["_id"] = str(user["_id"])
        return users

    @staticmethod
    def get_user_by_userid(usuario_id: ObjectId) -> UserResponse:
        return UserRepository.find_user_by_id(usuario_id)

    @staticmethod
    def update_user_watched_movie(usuario_id: ObjectId, movie: WatchedMovie) -> Union[UserResponse, None]:
        user: UserResponse = UserRepository.find_user_by_id(usuario_id)
        if not user:
            return None

        # Se o usuário já assistiu ao filme, atualiza a avaliação
        if any(m.get("tconst") == movie.tconst for m in user.get("watched_movies", [])):
            UserRepository.update_watched_movie(usuario_id, movie)
        else:
            # Se não encontrou, insere o novo filme na lista
            UserRepository.insert_watched_movie(usuario_id, movie)

        # Retorna o usuário atualizado
        return UserRepository.find_user_by_id(usuario_id)
