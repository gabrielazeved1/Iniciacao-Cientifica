import sys
import os
import logging 


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(project_root, 'src'))

from logger import setup_logging
from minio_client import MinioClient

logger = setup_logging(log_file_name="pesquisadores_list_buckets.log")

def main():
    logger.info("Iniciando script para listar buckets.")

    try:
        client = MinioClient()
        buckets = client.list_buckets() 

        if buckets:
            logger.info("Buckets disponíveis no MinIO:")
            for b in buckets:
                logger.info(f"- {b.name} (Criado em: {b.creation_date})")

        else:
            logger.info("Nenhum bucket encontrado.")

    except Exception as e:
        logger.critical(f"Erro inesperado no script de listagem de buckets: {e}", exc_info=True)
    finally:
        logger.info("Script para listar buckets finalizado.")

if __name__ == "__main__":
    main()