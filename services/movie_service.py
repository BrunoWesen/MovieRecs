from typing import List, Union

from repositories.movie_repository import MovieRepository
from repositories.user_repository import UserRepository
from schemas.movie import Movie


class MovieService:
    @staticmethod
    def get_all_movies(title: str, page: int, limit: int) -> List[Movie]:
        skip = (page - 1) * limit
        filter_query = {}
        if title:
            filter_query["primaryTitle"] = {"$regex": title, "$options": "i"}
        movies = MovieRepository.get_movies(skip, filter_query, limit)
        for movie in movies:
            movie["_id"] = str(movie["_id"])
        return movies

    @staticmethod
    def get_top_rated_movies(limit: int) -> List[Movie]:
        movies: list = []
        ratings: list = MovieRepository.get_ratings(limit)

        for rate in ratings:
            movie_doc = MovieRepository.find_one_title(rate['tconst'])
            if movie_doc:
                movies.append(movie_doc)

        for movie in movies:
            movie["_id"] = str(movie["_id"])

        return movies

    @staticmethod
    def get_directors_and_actors_movies(watched_tconsts: List[dict], high_rated: List[str], limit: int) -> List[Movie]:
        # busca filmes por diretores e/ou atores
        rec = []
        directors = set()
        actors = set()

        # extrai diretores
        for doc in MovieRepository.find_crew_by_high_rated(high_rated):
            dirs = doc.get("directors", "")
            for d in dirs.split(","):
                directors.add(d.strip())  # Somente adiciona o primeiro (melhor performance)
                break

        # buscar por diretor
        for director in directors:
            cursor = MovieRepository.filter_crew_by_directors(director, watched_tconsts, limit)
            for c in cursor:
                tc = c["tconst"]
                if tc not in rec:
                    rec.append(tc)
                    if len(rec) >= limit: break
            if len(rec) >= limit: break

        if len(rec) < limit:
            # extrai atores
            for doc in MovieRepository.find_actors(high_rated):
                actors.add(doc["nconst"])

            # buscar por ator
            for actor in actors:
                cursor = MovieRepository.filter_actors(actor, len(rec), limit)
                for c in cursor:
                    tc = c["tconst"]
                    if tc not in watched_tconsts and tc not in rec:
                        rec.append(tc)
                        if len(rec) >= limit: break
                if len(rec) >= limit: break

        if rec:
            movies: List[Movie] = MovieRepository.filter_movies(rec, limit)
            for m in movies: m["_id"] = str(m["_id"])
            return movies

    @staticmethod
    def get_recommended_by_genre(watched_titles: list, rating_by_tconst: dict, watched_tconsts: list, limit: int) -> \
    List[Movie]:
        # Calcula um score para cada gênero com base na avaliação do usuário
        genre_scores = {}
        for title in watched_titles:
            tconst = title.get("tconst")
            user_rating = rating_by_tconst.get(tconst)
            if not user_rating:
                genres_str = title.get("genres")
                if genres_str:
                    genres_list = [g.strip() for g in genres_str.split(",")]
                    for genre in genres_list:
                        genre_scores[genre] = genre_scores.get(genre, 0) + 1
                continue

            genres_str = title.get("genres")
            if genres_str:
                genres_list = [g.strip() for g in genres_str.split(",")]
                for genre in genres_list:
                    genre_scores[genre] = genre_scores.get(genre, 0) + user_rating

        # Se não for possível extrair nenhum gênero com base nas avaliações, fallback para filmes melhor avaliados
        if not genre_scores:
            return MovieService.get_top_rated_movies(limit)

        # Ordena os gêneros pelo score (maior score primeiro)
        sorted_genres: list = sorted(genre_scores.items(), key=lambda x: x[1], reverse=True)
        top_genres: list = [genre for genre, score in sorted_genres]
        regex: str
        if len(top_genres) > 1:
            regex = f"{top_genres[0]}.*{top_genres[1]}|{top_genres[1]}.*{top_genres[0]}"
        else:
            regex = top_genres[0]
        # Busca filmes na coleção "titles" que contenham pelo menos um dos gêneros favoritos
        # e que ainda não foram assistidos
        recommended_movies: List[Movie] = MovieRepository.filter_movies_by_genre(regex, watched_tconsts, limit)

        for movie in recommended_movies:
            movie["_id"] = str(movie["_id"])

        return recommended_movies

    @staticmethod
    def get_recommended_movies(usuario_id: str, limit: int) -> Union[List[Movie], None]:
        """
        Retorna recomendações considerando os gêneros dos filmes assistidos e
        as avaliações dadas pelo usuário.

        Se o usuário não tiver assistido nenhum filme, retorna os filmes melhor avaliados.
        Caso contrário:
          - Obtém os filmes assistidos e suas avaliações.
          - Faz o split do campo "genres" (uma string, ex: "Aventura, Ação") para obter uma lista de gêneros.
          - Acumula um score para cada gênero baseado na avaliação do usuário.
          - Ordena os gêneros pelo score e constrói uma expressão regular para buscar filmes
            com pelo menos um dos gêneros favoritos, excluindo os filmes que o usuário já assistiu.
        """
        user = UserRepository.find_user_by_id(usuario_id)
        if not user:
            return None

        # Se o usuário não assistiu nenhum filme, retorna os top avaliados
        watched = user.get("watched_movies", [])
        if not watched:
            return MovieService.get_top_rated_movies(limit)

        watched_tconsts = [movie["tconst"] for movie in user["watched_movies"]]
        rating_by_tconst = {
            wm["tconst"]: wm.get("rating")
            for wm in user["watched_movies"] if wm.get("rating") is not None
        }

        # Recupera os detalhes dos filmes assistidos para extrair os gêneros
        watched_titles: list = MovieRepository.filter_movies_by_tconst(watched_tconsts)

        high_rated = []
        max_rating = max((w.get("rating", 0) for w in watched), default=0)
        if max_rating:
            high_rated = [
                w["tconst"]
                for w in watched
                if w.get("rating", 0) == max_rating and max_rating >= 8.0
            ]

        if high_rated:
            return MovieService.get_directors_and_actors_movies(watched_titles, high_rated, limit)

        recommended_movies: List[Movie] = MovieService.get_recommended_by_genre(watched_titles, rating_by_tconst,
                                                                                watched_tconsts, limit)

        return recommended_movies
