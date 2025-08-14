# API de Acesso ao Datalake MinIO
** 14/08 ** 
-   **`src/main.py`**: É o ponto de entrada da sua aplicação. É aqui que a mágica do FastAPI acontece, onde todas as rotas são definidas e conectadas. O `main.py` age como o orquestrador que usa as funcionalidades dos outros arquivos.

-   **`src/minio_client.py`**: Este é o cliente de baixo nível para o MinIO. Ele encapsula a lógica de conexão com o servidor MinIO, garantindo que o `main.py` não precise se preocupar com os detalhes de como a conexão é feita.

-   **`src/models/auth.py`**: Contém o modelo de dados Pydantic (`MinioCredentials`) que define a estrutura das informações de login (usuário e senha) que a sua API espera receber.

-   **`src/utils/token.py`**: Este arquivo é dedicado à lógica de segurança da sua API. Ele contém as funções para gerar (`create_access_token`) e para verificar (`verify_token`) os tokens JWT, além da dependência (`oauth2_scheme`) que o FastAPI usa para injetar o token nas rotas protegidas.
```bash
poetry run uvicorn src.main:app --reload --port 8000
````

2. Fazer login
```bash
curl -X POST "http://127.0.0.1:8000/login" \
-H "Content-Type: application/json" \
-d '{"access_key": "amanda", "secret_key": "amanda123"}'
````

3. Listar todos os buckets 
```bash
curl -X GET "http://127.0.0.1:8000/buckets/datalake" \
-H "Authorization: Bearer SEU_TOKEN_AQUI"
```

3. Listar todos os buckets 
```bash
curl -X GET "http://127.0.0.1:8000/buckets/datalake" \
-H "Authorization: Bearer SEU_TOKEN_AQUI"
```

4. Listar o conteúdo de um bucket específico
```bash
curl -X GET "http://127.0.0.1:8000/buckets" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbWFuZGEiLCJleHAiOjE3NTUxODYzNTV9.8CUJlF4K9zmDvXY4dtzkJR6fO95f1fnVANA_65UuT3U"
```
5. Listar o conteúdo de uma subpasta
```bash
curl -X GET "http://127.0.0.1:8000/buckets/datalake?prefix=Comfaulda/Combined%20Faults/" \
-H "Authorization: Bearer SEU_TOKEN_AQUI"
```
