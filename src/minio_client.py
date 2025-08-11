import os
import logging
from urllib.parse import urlparse
from minio import Minio

logger = logging.getLogger('minio_datalake_app')

class MinioClient:
    """
    Cliente de baixo nível para gerenciar a conexão e o objeto Minio.
    Todas as lógicas de negócio devem usar este cliente.
    """
    def __init__(self, endpoint=None, access_key="minio", secret_key="miniol23", secure=False):
        raw_endpoint = endpoint or os.environ.get("MINIO_ENDPOINT", "http://127.0.0.1:9000")

        # Faz o parse da URL para extrair protocolo e host
        parsed = urlparse(raw_endpoint)
        if parsed.scheme in ["http", "https"]:
            secure = parsed.scheme == "https"
            resolved_endpoint = parsed.netloc
        else:
            resolved_endpoint = raw_endpoint

        self.client = Minio(
            resolved_endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        logger.info("MinioClient inicializado com endpoint: %s (secure=%s)", resolved_endpoint, secure)
