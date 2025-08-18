import os
import shutil
import logging
from .minio_client import MinioClient

logger = logging.getLogger('minio_datalake_app')

class Download:
    def __init__(self, client: MinioClient):
        self.client = client.client

    def download_file(self, bucket_name: str, object_name: str, local_filename: str = None) -> bool:
        """
        Baixa um arquivo do MinIO.
        """
        try:
            local_filename = local_filename or os.path.join(os.path.expanduser("~"), "Downloads", os.path.basename(object_name))
            os.makedirs(os.path.dirname(local_filename), exist_ok=True)
            self.client.fget_object(bucket_name, object_name, local_filename)
            logger.info(f"Arquivo '{object_name}' baixado com sucesso em '{local_filename}'.")
            return True
        except Exception as e:
            logger.error(f"Falha ao baixar arquivo '{object_name}': {e}")
            return False

    def download_directory(self, bucket_name: str, prefix: str, local_directory: str = None) -> bool:
        """
        Baixa todos os arquivos de um prefixo (diretório virtual) do MinIO.
        """
        try:
            local_directory = local_directory or os.path.join(os.path.expanduser("~"), "Downloads", prefix)
            os.makedirs(local_directory, exist_ok=True)

            objects = self.client.list_objects(bucket_name, prefix=prefix, recursive=True)
            for obj in objects:
                obj_path = os.path.join(local_directory, os.path.relpath(obj.object_name, prefix))
                os.makedirs(os.path.dirname(obj_path), exist_ok=True)
                self.client.fget_object(bucket_name, obj.object_name, obj_path)
                logger.info(f"Arquivo '{obj.object_name}' baixado com sucesso em '{obj_path}'.")

            return True
        except Exception as e:
            logger.error(f"Falha ao baixar diretório '{prefix}': {e}")
            return False
