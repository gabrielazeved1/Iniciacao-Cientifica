# src/models/auth.py

from pydantic import BaseModel

class MinioCredentials(BaseModel):
    """
    Define o modelo de dados para as credenciais de login.
    Esperamos receber um 'access_key' e um 'secret_key', ambos como strings.
    """
    access_key: str
    secret_key: str