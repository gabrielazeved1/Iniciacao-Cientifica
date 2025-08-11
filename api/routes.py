# api/routes.py
from fastapi import APIRouter, Body, HTTPException, Query # Adicionado: Body
from pydantic import BaseModel, validator
import os
import sys

# Adiciona o caminho para importar os serviços do MinIO
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(project_root, 'src'))

from src.list_service import ListService
from src.logger import setup_logging

logger = setup_logging(log_file_name="api_access.log")
router = APIRouter()

# Variável global para armazenar credenciais
stored_creds = None

class MinioCredentials(BaseModel):
    access_key: str
    secret_key: str
    endpoint: str = "http://127.0.0.1:9000"

    @validator('endpoint')
    def endpoint_must_not_have_path(cls, v):
        if v and v.endswith('/'):
            return v.rstrip('/')
        return v

@router.get("/")
def read_root():
    global stored_creds
    if stored_creds is None:
        return {"message": "Insira suas credenciais para testar a conexão com o MinIO."}
    else:
        return {
            "message": f"API de Teste de Conexão com MinIO está funcionando! "
                       f"Usuário: {stored_creds['access_key']}, "
                       f"Senha: {stored_creds['secret_key']}, "
                       f"Endpoint: {stored_creds['endpoint']}"
        }

@router.post("/check-connection")
def check_minio_connection(creds: MinioCredentials):
    """
    Tenta se conectar ao MinIO com as credenciais fornecidas
    e retorna o status da conexão.
    """
    global stored_creds
    try:
        service = ListService(
            access_key=creds.access_key,
            secret_key=creds.secret_key,
            endpoint=creds.endpoint
        )
        
        buckets = service.list_all_buckets()
        
        if buckets is not None:
            stored_creds = creds.dict()  # Salva credenciais globalmente
            logger.info(f"API: Conexão com Minio bem-sucedida para o usuário '{creds.access_key}'.")
            return {"status": "success", "message": "Conexão com o MinIO bem-sucedida e credenciais armazenadas!"}
        else:
            raise Exception("Falha ao listar buckets. Verifique suas credenciais e o endpoint.")

    except Exception as e:
        logger.error(f"API: Falha na conexão com Minio para o usuário '{creds.access_key}': {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Falha na conexão com Minio: {e}"
        )

@router.get("/list")
def list_datalakes():
    """
    Lista todos os buckets (Data Lakes) disponíveis no MinIO.
    Requer que as credenciais já tenham sido configuradas via /check-connection.
    """
    global stored_creds
    if stored_creds is None:
        raise HTTPException(
            status_code=400,
            detail="Credenciais não configuradas. Use /check-connection primeiro."
        )

    try:
        service = ListService(
            access_key=stored_creds['access_key'],
            secret_key=stored_creds['secret_key'],
            endpoint=stored_creds['endpoint']
        )
        buckets = service.list_all_buckets()
        
        return {
            "status": "success",
            "buckets": [b.name for b in buckets]
        }

    except Exception as e:
        logger.error(f"API: Falha ao listar Data Lakes: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Falha ao listar Data Lakes: {e}"
        )