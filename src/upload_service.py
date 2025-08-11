# src/upload_service.py
import os
import logging
from minio.error import S3Error
from src.minio_client import MinioClient
from src.logger import setup_logging

logger = setup_logging(log_file_name="api_access.log")

class UploadService:
    def __init__(self, access_key, secret_key, endpoint):
        self.minio_client = MinioClient(access_key=access_key, secret_key=secret_key, endpoint=endpoint)

    def upload_file(self, bucket_name: str, local_path: str, object_prefix: str = "") -> bool:
        if not os.path.isfile(local_path):
            logger.error(f"Arquivo '{local_path}' não encontrado para upload.")
            return False

        if not self.minio_client.client.bucket_exists(bucket_name):
            logger.info(f"Bucket '{bucket_name}' não existe. Tentando criar...")
            try:
                self.minio_client.client.make_bucket(bucket_name)
                logger.info(f"Bucket '{bucket_name}' criado com sucesso.") 
            except S3Error as err:
                logger.error(f"Erro S3 ao tentar criar o bucket '{bucket_name}': {err}")
                return False
            except Exception as e:
                logger.error(f"Erro inesperado ao criar o bucket '{bucket_name}': {e}")
                return False

        object_name = os.path.basename(local_path)
        if object_prefix:
            object_prefix = object_prefix.strip('/')
            object_name = f"{object_prefix}/{object_name}"
       
        try:
            logger.info(f"Iniciando upload de '{local_path}' para '{bucket_name}/{object_name}'.")
            with open(local_path, "rb") as file_data:
                file_size = os.path.getsize(local_path)
                self.minio_client.client.put_object(
                    bucket_name=bucket_name,
                    object_name=object_name, 
                    data=file_data,
                    length=file_size,
                    content_type="application/octet-stream"
                )
            logger.info(f"Upload de '{local_path}' como '{object_name}' no bucket '{bucket_name}' realizado com sucesso.")
            return True
        except S3Error as err:
            logger.error(f"Erro S3 no upload de '{local_path}' para '{bucket_name}/{object_name}': {err}", exc_info=True)
            return False
        except Exception as err:
            logger.error(f"Erro inesperado no upload de '{local_path}': {err}", exc_info=True)
            return False
            
    def upload_directory(self, bucket_name: str, local_directory: str, minio_base_prefix: str = "") -> bool:
        if not os.path.isdir(local_directory):
            logger.error(f"Diretório local '{local_directory}' não encontrado para upload de diretório.")
            return False

        if not self.minio_client.client.bucket_exists(bucket_name):
            logger.info(f"Bucket '{bucket_name}' não existe. Tentando criar...")
            try:
                self.minio_client.client.make_bucket(bucket_name)
                logger.info(f"Bucket '{bucket_name}' criado com sucesso para upload de diretório.")
            except S3Error as err:
                logger.error(f"Erro S3 ao tentar criar o bucket '{bucket_name}': {err}")
                return False
            except Exception as e:
                logger.error(f"Erro inesperado ao criar o bucket '{bucket_name}': {e}")
                return False

        all_successful = True
        num_files_uploaded = 0
        num_files_failed = 0

        if not minio_base_prefix:
            minio_base_prefix = os.path.basename(os.path.normpath(local_directory)) + "/"

        logger.info(f"Iniciando upload recursivo do diretório '{local_directory}' para '{bucket_name}/{minio_base_prefix}'.")
        for root, dirs, files in os.walk(local_directory):
            for file_name in files:
                local_file_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(local_file_path, local_directory)
                minio_object_name = os.path.join(minio_base_prefix, relative_path).replace("\\", "/")

                logger.debug(f"Processando arquivo para upload: '{local_file_path}' como '{minio_object_name}'.")
                try:
                    with open(local_file_path, "rb") as file_data:
                        file_size = os.path.getsize(local_file_path)
                        self.minio_client.client.put_object(
                            bucket_name=bucket_name,
                            object_name=minio_object_name,
                            data=file_data,
                            length=file_size,
                            content_type="application/octet-stream"
                        )
                    logger.debug(f"Upload de '{local_file_path}' bem-sucedido.")
                    num_files_uploaded += 1
                except S3Error as err:
                    logger.error(f"Erro S3 ao fazer upload de '{local_file_path}' para '{bucket_name}/{minio_object_name}': {err}", exc_info=True)
                    all_successful = False
                    num_files_failed += 1
                except Exception as e:
                    logger.error(f"Erro inesperado ao fazer upload de '{local_file_path}': {e}", exc_info=True)
                    all_successful = False
                    num_files_failed += 1

        if all_successful:
            logger.info(f"Upload do diretório '{local_directory}' para '{bucket_name}/{minio_base_prefix}' concluído com sucesso. ({num_files_uploaded} arquivos upados).")
        else:
            logger.error(f"Upload do diretório '{local_directory}' para '{bucket_name}/{minio_base_prefix}' finalizado com erros. ({num_files_uploaded} arquivos upados, {num_files_failed} falharam).")
        return all_successful