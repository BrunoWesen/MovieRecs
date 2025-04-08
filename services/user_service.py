from typing import Union

from pymongo.errors import DuplicateKeyError

from repositories.user_repository import UserRepository
from schemas.user import User
from schemas.watched_movie import WatchedMovie


class UserService:
    @staticmethod
    def create_user(user_data: dict) -> Union[str, None]:
        try:
            result = UserRepository.insert_one_user(user_data)
            return str(result.inserted_id)
        except DuplicateKeyError:
            return None

    @staticmethod
    def get_user_by_userid(usuario_id: str) -> User:
        user = UserRepository.find_user_by_id(usuario_id)
        if user:
            user["_id"] = str(user["_id"])
        return user

    @staticmethod
    def update_user_watched_movie(usuario_id: str, movie: WatchedMovie) -> Union[dict, None]:
        user = UserRepository.find_user_by_id(usuario_id)
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
