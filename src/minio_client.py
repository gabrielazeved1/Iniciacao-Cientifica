# minio_Client.py (remova a linha logging.basicConfig)
import os
import logging # Mantenha este import
from minio import Minio
from minio.error import S3Error

# Obtém uma instância do logger globalmente configurado
# O nome 'minio_datalake_app' DEVE ser o mesmo usado em setup_logging no logger.py
logger = logging.getLogger('minio_datalake_app')

class MinioClient:
    """
    Classe responsável por interagir com o MinIO usando o SDK oficial.
    """

    def __init__(self, endpoint="localhost:9000", access_key="minio", secret_key="miniol23", secure=False):
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        logger.info("MinioClient inicializado com endpoint: %s", endpoint) # Use o logger

    def upload_file(self, bucket_name: str, local_path: str, object_name: str = None, object_prefix: str = "") -> bool:
        if not os.path.isfile(local_path):
            logger.error(f"Arquivo '{local_path}' não encontrado para upload.")
            return False

        if not self.client.bucket_exists(bucket_name):
            logger.info(f"Bucket '{bucket_name}' não existe. Tentando criar...")
            try:
                self.client.make_bucket(bucket_name)
                logger.info(f"Bucket '{bucket_name}' criado com sucesso para upload.")
            except S3Error as err:
                logger.error(f"Erro S3 ao tentar criar o bucket '{bucket_name}': {err}")
                return False
            except Exception as e:
                logger.error(f"Erro inesperado ao criar o bucket '{bucket_name}': {e}")
                return False

        if object_name is None:
            object_name = os.path.basename(local_path)

        # --- NOVA LÓGICA AQUI ---
        # Se um prefixo for fornecido, adicione-o ao nome do objeto
        if object_prefix:
            # Garante que o prefixo termine com '/' e o nome do objeto não comece com '/'
            object_prefix = object_prefix.strip('/')
            object_name = f"{object_prefix}/{object_name}"
        # --- FIM DA NOVA LÓGICA ---

        try:
            with open(local_path, "rb") as file_data:
                file_size = os.path.getsize(local_path)
                self.client.put_object(
                    bucket_name=bucket_name,
                    object_name=object_name, # Este já foi ajustado com o prefixo
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

    def download_file(self, bucket_name: str, object_name: str, local_filename: str = None) -> bool:
        try:
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            if not os.path.exists(downloads_path):
                os.makedirs(downloads_path)
                logger.info(f"Diretório de Downloads '{downloads_path}' criado.")

            if local_filename is None:
                local_filename = object_name

            local_path = os.path.join(downloads_path, local_filename)

            logger.info(f"Tentando baixar '{object_name}' do bucket '{bucket_name}' para '{local_path}'.")

            # Verifica se o objeto existe antes de tentar baixar
            try:
                self.client.stat_object(bucket_name, object_name)
            except S3Error as err:
                if err.code == "NoSuchKey":
                    logger.error(f"Objeto '{object_name}' não encontrado no bucket '{bucket_name}'.")
                else:
                    logger.error(f"Erro S3 ao verificar objeto '{object_name}': {err}")
                return False

            data = self.client.get_object(bucket_name, object_name)

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

    # Adicione outros métodos se existirem, como list_buckets, list_objects, remove_object etc.
    def list_buckets(self):
        try:
            buckets = self.client.list_buckets()
            logger.info("Buckets existentes no MinIO:")
            for bucket in buckets:
                logger.info(f" - {bucket.name} (Criado em: {bucket.creation_date})")
            return buckets
        except S3Error as err:
            logger.error(f"Erro S3 ao listar buckets: {err}", exc_info=True)
            return []
        except Exception as e:
            logger.error(f"Erro inesperado ao listar buckets: {e}", exc_info=True)
            return []
    def upload_directory(self, bucket_name: str, local_directory: str, minio_base_prefix: str = "") -> bool:
        """
        Faz o upload recursivo de um diretório local para um bucket no MinIO.

        :param bucket_name: Nome do bucket no MinIO.
        :param local_directory: Caminho do diretório local a ser upado.
        :param minio_base_prefix: Prefixo no MinIO para os arquivos (ex: 'pasta_raiz/'). Se vazio, usa o nome do diretório.
        :return: True se todos os uploads forem bem-sucedidos, False caso contrário.
        """
        if not os.path.isdir(local_directory):
            logger.error(f"Diretório local '{local_directory}' não encontrado para upload.")
            return False

        if not self.client.bucket_exists(bucket_name):
            logger.info(f"Bucket '{bucket_name}' não existe. Tentando criar...")
            try:
                self.client.make_bucket(bucket_name)
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

        # Se minio_base_prefix não for fornecido, use o nome do diretório local
        if not minio_base_prefix:
            minio_base_prefix = os.path.basename(os.path.normpath(local_directory)) + "/"

        for root, dirs, files in os.walk(local_directory):
            for file_name in files:
                local_file_path = os.path.join(root, file_name)
                # Calcula o caminho relativo para MinIO
                relative_path = os.path.relpath(local_file_path, local_directory)
                minio_object_name = os.path.join(minio_base_prefix, relative_path).replace("\\", "/") # Garante barras corretas

                logger.info(f"Iniciando upload de '{local_file_path}' para '{bucket_name}/{minio_object_name}'")
                try:
                    with open(local_file_path, "rb") as file_data:
                        file_size = os.path.getsize(local_file_path)
                        self.client.put_object(
                            bucket_name=bucket_name,
                            object_name=minio_object_name,
                            data=file_data,
                            length=file_size,
                            content_type="application/octet-stream"
                        )
                    logger.info(f"Upload de '{local_file_path}' como '{minio_object_name}' realizado com sucesso.")
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