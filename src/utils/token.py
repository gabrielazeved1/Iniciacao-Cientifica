# src/utils/token.py

from datetime import datetime, timedelta # serve para lidar com datas e horas
from jose import jwt, JWTError # codifica e decodifica tokens JWT
from fastapi.security import OAuth2PasswordBearer # injeta o token na função
from fastapi import HTTPException, Depends # lida com exceções HTTP
import os

ALGORITHM = "HS256" #cadeado

# Esta instância faz o FastAPI procurar pelo token no cabeçalho
# "Authorization: Bearer <token>" e o injeta na sua função.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict,secret_key: str, expires_delta: timedelta | None = None):
    """
    Cria um token de acesso JWT a partir de um dicionário de dados.
    Recebe um dicionario com os dados do usuario e um tempo de expiração opcional.
    Se o tempo de expiração não for fornecido, o token expirará em 15 minutos.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15) # tempo padrão de expiração de 15 minutos
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM) 
    # retorna o token codificado
    # print para debug
    print(f"Token criado: {encoded_jwt}")
    print(f"Expira em: {expire}")
    return encoded_jwt

def verify_token(token: str, secret_key: str):
    """
    Verifica se o token é válido e retorna o payload.
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
def get_current_user_access_key(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
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