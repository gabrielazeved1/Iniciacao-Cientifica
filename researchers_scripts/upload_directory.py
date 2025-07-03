import os
import sys
import logging
from logger import setup_logging
from minio_client import MinioClient

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(project_root, 'src'))


logger = setup_logging(log_file_name="pesquisadores_upload_diretorio.log")

def main():
    logger.info("Iniciando script de upload de diretório.")

    if len(sys.argv) < 3:
        logger.error("Uso correto: python upload_directory.py <bucket_name> <caminho_diretorio_local> [prefixo_minio_opcional]")
        sys.exit(1)

    bucket_name = sys.argv[1]
    local_directory = sys.argv[2]
    minio_prefix = sys.argv[3] if len(sys.argv) > 3 else ""

    logger.info(f"Tentando fazer upload do diretório '{local_directory}' para o bucket '{bucket_name}' com prefixo '{minio_prefix}'.")

    try:
        client = MinioClient()
        success = client.upload_directory(bucket_name, local_directory, minio_prefix)

        if success:
            logger.info(f"Diretório '{local_directory}' enviado para o bucket '{bucket_name}' com sucesso.")
        else:
            logger.error(f"[✖] Falha no envio do diretório '{local_directory}'. Verifique os logs para mais detalhes.")
    except Exception as e:
        logger.critical(f"Erro inesperado no script de upload de diretório: {e}", exc_info=True)
    finally:
        logger.info("Script de upload de diretório finalizado.")

if __name__ == "__main__":
    main()