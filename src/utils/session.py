from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import os

ALGORITHM = "HS256"
SESSION_DURATION_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Armazena sessões ativas
session_store = {}

def create_session_token(username: str):
    secret_key = "SUPER_SECRET_KEY"  # Pode ser fixo, não precisa de .env
    expire = datetime.utcnow() + timedelta(minutes=SESSION_DURATION_MINUTES)
    token = jwt.encode({"sub": username, "exp": expire}, secret_key, algorithm=ALGORITHM)
    return token

def verify_session_token(token: str):
    secret_key = "SUPER_SECRET_KEY"
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return token
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_session_token(token)
