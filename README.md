# Sistema de Recomendação de Filmes / Títulos

# 1. Introdução

Este projeto é uma **API** de recomendação de títulos (longa‑metragem, curta‑metragem e séries) construída com **FastAPI** e **MongoDB**. Ela utiliza dados brutos do **IMDb** para oferecer recomendações personalizadas de acordo com:

- Avaliações do usuário
- Gêneros preferidos
- Diretores e atores favoritos

O sistema permite também o gerenciamento de usuários e o registro de filmes assistidos.

# 2. Tecnologias

- **Linguagem:** Python 3.10+  
- **Framework:** FastAPI  
- **Banco de Dados:** MongoDB (utilizando PyMongo)  
- **Modelos de Dados:** Pydantic  
- **Pré‑processamento:** Dask e Pandas

# 4. Fonte dos Dados

Os dados utilizados são os dumps oficiais do **IMDb**, dentre eles:

- `title.basics.tsv`
- `title.ratings.tsv`
- `title.crew.tsv`
- `title.principals.tsv`

### Pré‑processamento
- Foi ultilizado **Dask** para filtrar somente os títulos desejados: `movie`, `short`, `tvMovie` e `tvSeries`.
- O resultado é materializado em um **Pandas DataFrame** e importado para o MongoDB.

### Dump Pré‑processado
Devido ao tamanho (quase **1 GB**), o dump completo foi hospedado externamente:
[⬇️ Baixar Dump Pré‑processado](https://drive.google.com/file/d/1TOs5Hlg9Y7aFKS7RX0-5N3n5gImht0n_/view?usp=sharing)

# 5. Instalação

### Clonando o repositório
```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```
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
Certifique-se de que o MongoDB esteja rodando localmente ou em um serviço gerenciado.

Crie o database movies_db.

Importe os dados:

Utilize o dump pré‑processado:

```bash
tar -xzvf imdb_dump.tar.gz
mongorestore --db movies_db imdb_dump/
```


---

# 6. Executando a API

Para iniciar a API em modo de desenvolvimento (com recarregamento automático), use o **fastapi run**:

```bash
fastapi run main.py
```

Acesse a documentação interativa da API em: http://localhost:8000/docs


---

# 7. Endpoints Principais

### Usuários

| Método | Rota                                  | Descrição                                  |
| ------ | ------------------------------------- | ------------------------------------------ |
| POST   | `/usuarios/`                          | Cria um novo usuário                       |
| GET    | `/usuarios/{usuario_id}`              | Busca o usuário pelo `usuario_id`          |
| PUT    | `/usuarios/{usuario_id}/assistidos`   | Adiciona/atualiza filme assistido e rating |

### Títulos

| Método | Rota                                      | Descrição                                                      |
| ------ | ----------------------------------------- | -------------------------------------------------------------- |
| GET    | `/filmes/`                                | Lista títulos com paginação e busca                            |
| GET    | `/filmes/{usuario_id}/recomendacoes`      | Retorna recomendações personalizadas                           |

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
