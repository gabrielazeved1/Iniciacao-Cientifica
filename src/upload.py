from fastapi import UploadFile
import shutil
import os
from .minio_client import MinioClient
import logging

logger = logging.getLogger('minio_datalake_app')

class Upload:
    def __init__(self, client: MinioClient):
        self.client = client.client

    def upload_file(self, bucket_name: str, file: UploadFile, prefix: str = "") -> str:
        temp_path = f"/tmp/{file.filename}"
        try:
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            self.client.fput_object(bucket_name, f"{prefix}/{file.filename}" if prefix else file.filename, temp_path)
            logger.info(f"Arquivo '{file.filename}' enviado para bucket '{bucket_name}'.")
            return f"{prefix}/{file.filename}" if prefix else file.filename
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def upload_directory(self, bucket_name: str, local_directory: str, prefix: str = "") -> bool:
        try:
            for root, _, files in os.walk(local_directory):
                for f in files:
                    file_path = os.path.join(root, f)
                    obj_name = f"{prefix}/{f}" if prefix else f
                    self.client.fput_object(bucket_name, obj_name, file_path)
            logger.info(f"Diretório '{local_directory}' enviado para bucket '{bucket_name}'.")
            return True
        except Exception as e:
            logger.error(f"Falha no upload do diretório: {e}")
            return False
