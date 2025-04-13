# Sistema de Recomendação de Filmes

# 1. Introdução

Este projeto é uma **API** de recomendação de Filmes construída com **FastAPI** e **MongoDB**. Ela utiliza dados brutos do **IMDb** para oferecer recomendações personalizadas de acordo com:

- Avaliações do usuário
- Gêneros preferidos
- Diretores e atores favoritos

O sistema permite também o gerenciamento de usuários e o registro de filmes assistidos.

# 2. Tecnologias

- **Linguagem:** Python 3.9+  
- **Framework:** FastAPI  
- **Banco de Dados:** MongoDB (utilizando PyMongo)  
- **Modelos de Dados:** Pydantic  
- **Pré‑processamento:** Pandas

# 4. Fonte dos Dados

Os dados utilizados são os dumps oficiais do [**IMDb**](https://developer.imdb.com/non-commercial-datasets/), dentre eles:

- `title.basics.tsv`
- `title.ratings.tsv`
- `title.crew.tsv`
- `title.principals.tsv`

### Pré‑processamento
- Foi ultilizado **Pandas** para filtrar somente os títulos desejados: `movie` e `tvMovie`.

# 5. Instalação

### Clonando o repositório
```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```
### Crie um .env
Crie um .env a partir do .env.example (copie e cole) ou no bash:
```bash
cp .env.example .env
```
e depois o configure conforme seu ambiente.
### Criando e ativando o ambiente virtual
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```
### Instalando as dependências
```bash
pip install -r requirements.txt
```
### Configurando o MongoDB
Certifique-se de que o MongoDB esteja rodando localmente ou em um serviço gerenciado e depois rode o script `import_imdb` localizado em `scripts/import_imdb.py`, certifique-se de configurar o .env corretamente.

> **⚠️ Aviso**  
> Se você já tiver o database movies_db faça o backup pois o script irá excluí-lo para importar os dados dos filmes.
---

# 6. Executando a API

Para iniciar a API em modo de desenvolvimento (com recarregamento automático) basta executar o `main` ou se preferir, use o **uvicorn**:

```bash
uvicorn app.main:app --reload 
```

Acesse a documentação interativa da API em `/docs` comumente localizado em: http://localhost:8000/docs


---

# 7. Endpoints Principais

### Usuários

| Método | Rota                                  | Descrição                                  |
|--------| ------------------------------------- |--------------------------------------------|
| POST   | `/usuarios/`                          | Cria um novo usuário                       |
| GET    | `/usuarios/`                          | Lista os usuários com paginação e busca    |
| GET    | `/usuarios/{usuario_id}`              | Busca o usuário pelo `usuario_id`          |
| PUT    | `/usuarios/{usuario_id}/assistidos`   | Adiciona/atualiza filme assistido e rating |

### Títulos

| Método | Rota                                      | Descrição                             |
| ------ | ----------------------------------------- |---------------------------------------|
| GET    | `/filmes/`                                | Lista os filmes com paginação e busca |
| GET    | `/filmes/{usuario_id}/recomendacoes`      | Retorna recomendações personalizadas  |

# 8. Lógica de Recomendação

A API recomenda títulos com base em uma hierarquia de critérios:

1. **Filmes com avaliação alta (≥ 8.0) pelo usuário**  
   - Extração de diretores e atores dos títulos avaliados.
   - Recomenda outros títulos envolvendo estes profissionais.

2. **Fallback por gênero**  
   - Caso não existam títulos com alta avaliação, calcula o “top gênero” preferido.
   - Recomenda títulos que contenham esse gênero.

3. **Fallback geral**  
   - Se nenhum critério específico for atendido, retorna os títulos com maior avaliação global.

# 9. Testes de api

Os testes de api se localizam na pasta `tests` e para executar basta executar cada arquivo de teste ou se quiser testar todos os testes use o comando:
```bash
pytest
```
com o comando `pytest` ele já localiza todos os arquivos `test_` da pasta de `tests` e executa todas as funções de testes.
