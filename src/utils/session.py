from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

ALGORITHM = "HS256"
SESSION_DURATION_MINUTES = 60
SECRET_KEY = "SUPER_SECRET_KEY"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Armazena sessões ativas
session_store = {}

def create_session_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=SESSION_DURATION_MINUTES)
    token = jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_session_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return token
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_session_token(token)
