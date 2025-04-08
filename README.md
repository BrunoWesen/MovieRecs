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

> **Importante:** o dump completo ocupa mais de **4.5 GB**. Para evitar versionamento de arquivos grandes, disponibilizo um link externo para download pré-processado:
> ![Captura de tela de 2025-04-08 16-10-01](https://github.com/user-attachments/assets/2877d0cb-82b9-40f9-8671-e8606a47211d)


[⬇️ Baixar MongoDB dump pré-processado (4.5 GB)](https://drive.google.com/file/d/1h4htTdC15YqB09IaXSYpeu3qOQfRxxmW/view?usp=sharing)


---

> **⚠️ Aviso de Compatibilidade**  
> Este sistema foi desenvolvido e testado apenas em **Linux Ubuntu**.  
> Embora deva funcionar em outras plataformas, não foram realizados testes em macOS ou Windows.

