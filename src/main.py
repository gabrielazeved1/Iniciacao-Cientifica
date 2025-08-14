# src/main.py

# Bibliotecas padrão do Python
import os
from datetime import timedelta

# Bibliotecas de terceiros
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from minio import Minio
from minio.error import S3Error

# Módulos do seu projeto
from .minio_client import MinioClient
from .models.auth import MinioCredentials
from .utils.token import create_access_token, verify_token

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Variáveis e configurações globais
SECRET_KEY = os.getenv("SECRET_KEY")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Simulação de um banco de dados de usuários
fake_db = {
    "minio": "miniol23",
    "amanda": "amanda123",
    "pedro": "pedro456"
}

# Instancia a aplicação FastAPI
app = FastAPI()

# Rota para obter o token a partir de um usuário autenticado
def get_current_user_access_key(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_token(token, SECRET_KEY)
        access_key: str = payload.get("sub")
        if access_key is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return access_key
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/")
def read_root():
    return {
        "message": "Bem-vindo à API do Datalake MinIO!",
        "instrucoes_login": (
            "Para acessar, faça o login enviando um POST para a rota '/login' "
            "com suas credenciais Minio no corpo da requisição."
        )
    }

@app.post("/login", status_code=status.HTTP_200_OK)
def login(credentials: MinioCredentials):
    """
    Recebe as credenciais do MinIO, verifica a validade e retorna um JWT.
    """
    # Verifica se o usuário e a senha existem no nosso banco de dados
    if not (credentials.access_key in fake_db and fake_db[credentials.access_key] == credentials.secret_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas. Verifique seu access_key e secret_key."
        )
    
    # Se a verificação interna for bem-sucedida, tentamos a conexão com o MinIO
    try:
        minio_client_instance = MinioClient(
            access_key=credentials.access_key,
            secret_key=credentials.secret_key,
            endpoint=MINIO_ENDPOINT
        )
        minio_client_instance.client.list_buckets()
        
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": credentials.access_key},
            secret_key=SECRET_KEY, 
            expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
    except S3Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao conectar ao MinIO: {err}"
        )

@app.get("/buckets")
def list_buckets(current_user_access_key: str = Depends(get_current_user_access_key)):
    """
    Lista todos os buckets acessíveis para o usuário autenticado.
    """
    try:
        minio_client_instance = MinioClient(
            access_key=current_user_access_key,
            secret_key=fake_db.get(current_user_access_key),
            endpoint=MINIO_ENDPOINT
        )
        buckets = minio_client_instance.client.list_buckets()
        return {"buckets": [bucket.name for bucket in buckets]}
    except S3Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar buckets: {err}"
        )