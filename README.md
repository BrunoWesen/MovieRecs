# Sistema de Recomendação de Filmes

Este repositório contém a API de recomendação de filmes construída com **FastAPI** e **MongoDB**, utilizando dados brutos do **IMDb**. A API oferece endpoints para gerenciamento de usuários, registro de filmes assistidos e recomendações personalizadas com base em gêneros, avaliações, diretores e atores favoritos.

---

## 📦 Tecnologias

- **Linguagem**: Python 3.9+  
- **Framework**: [FastAPI]  
- **Banco de Dados**: MongoDB (4.5 GB+ de dados importados dos dumps do IMDb)  
- **Driver**: PyMongo  
- **Modelagem**: Pydantic (schemas)  
- **Gerenciamento de dependências**: pip / virtualenv  

---

## 📊 Fonte dos Dados

Os dados utilizados são os dumps oficiais do **IMDb** (https://developer.imdb.com/non-commercial-datasets/):

- `title.basics.tsv`  
- `title.ratings.tsv`  
- `title.crew.tsv`  
- `title.principals.tsv`  

> **Importante:** o dump completo ocupa mais de **4.5 GB**. Para evitar versionamento de arquivos grandes, disponibilizamos um link externo para download pré-processado:

[⬇️ Baixar MongoDB dump pré-processado (4.5 GB)](https://seu-servidor.com/imdb_dump.tar.gz)

---

📑 Endpoints Principais
Usuários
Método	Rota	Descrição
POST	/users/	Cria novo usuário
GET	/users/{username}	Busca dados do usuário
PUT	/users/{username}/watched	Adiciona/atualiza filme assistido e rating
Filmes
Método	Rota	Descrição
GET	/filmes/	Lista filmes (filtro por título, paginação)
GET	/filmes/{tconst}	Busca filme(s) pelo tconst
GET	/filmes/{username}/recomendacoes	Retorna recomendações personalizadas (diretores, atores, gênero)

