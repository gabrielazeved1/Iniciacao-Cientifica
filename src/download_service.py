# src/download_service.py
import os
import logging
from src.minio_client import MinioClient
from src.logger import setup_logging
from minio.error import S3Error

logger = setup_logging(log_file_name="api_access.log")

class DownloadService:
    def __init__(self, access_key, secret_key, endpoint):
        self.minio_client = MinioClient(access_key=access_key, secret_key=secret_key, endpoint=endpoint)

    def download_file(self, bucket_name: str, object_name: str, local_path: str) -> bool:
        """
        faz o download de um objeto do MinIO para um arquivo local.
        """
        try:
            local_file_directory = os.path.dirname(local_path)
            if not os.path.exists(local_file_directory):
                os.makedirs(local_file_directory, exist_ok=True)
                logger.info(f"Diretório local para download criado: '{local_file_directory}'.")
            
            logger.info(f"Tentando baixar '{object_name}' do bucket '{bucket_name}' para '{local_path}'.")

            if not self.minio_client.client.bucket_exists(bucket_name):
                logger.error(f"O bucket '{bucket_name}' não existe.")
                return False

            try:
                self.minio_client.client.stat_object(bucket_name, object_name)
            except S3Error as err:
                if err.code == "NoSuchKey":
                    logger.error(f"Objeto '{object_name}' não encontrado no bucket '{bucket_name}'.")
                else:
                    logger.error(f"Erro S3 ao verificar objeto '{object_name}': {err}")
                return False

            data = self.minio_client.client.get_object(bucket_name, object_name)

            with open(local_path, "wb") as file_data:
                for chunk in data.stream(32*1024):
                    file_data.write(chunk)

            logger.info(f"Arquivo '{object_name}' do bucket '{bucket_name}' baixado em '{local_path}'.")
            return True 

        except S3Error as err:
            logger.error(f"Erro S3 no download de '{object_name}' do bucket '{bucket_name}': {err}", exc_info=True)
            return False
        except Exception as e:
            logger.error(f"Erro inesperado no download de '{object_name}': {e}", exc_info=True)
            return False