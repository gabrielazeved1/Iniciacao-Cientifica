import logging
import sys
import os


# adicionar o diretório 'src' ao sys.path para permitir importações relativas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logger import setup_logging
from minio_client import MinioClient

logger = setup_logging(log_file_name="datalake_admin.log")

def initialize_datalake_environment():
    """
    função para inicializar o ambiente do Data Lake:
    - verificar conexão com MinIO.
    - criar buckets essenciais se não existirem.
    """
    logger.info("Iniciando a verificação e configuração do ambiente do Data Lake.")

    try:
        minio_client = MinioClient()
        try:
            minio_client.client.list_buckets()
            logger.info("Conexão com MinIO estabelecida com sucesso.")
        except Exception as e:
            logger.critical(f"NÃO FOI POSSÍVEL CONECTAR AO MINIO. Verifique se o MinIO está rodando e acessível. Erro: {e}")
            sys.exit(1) 

        # Define os buckets essenciais para o seu Data Lake
        essential_buckets = ["datalake", "backup"]

        for bucket in essential_buckets:
            if not minio_client.client.bucket_exists(bucket):
                logger.info(f"Bucket '{bucket}' não existe. Criando...")
                try:
                    minio_client.client.make_bucket(bucket)
                    logger.info(f"Bucket '{bucket}' criado com sucesso.")
                except Exception as e:
                    logger.error(f"Falha ao criar o bucket '{bucket}': {e}")
            else:
                logger.info(f"Bucket '{bucket}' já existe. Ok.")

        logger.info("Verificação e configuração do ambiente do Data Lake concluída.")

    except Exception as e:
        logger.critical(f"Ocorreu um erro crítico durante a inicialização do ambiente do Data Lake: {e}", exc_info=True)
    finally:
        logger.info("Processo de inicialização do ambiente finalizado.")

if __name__ == "__main__":
    initialize_datalake_environment()