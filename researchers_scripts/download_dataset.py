import sys
import os
import logging # Importar o módulo logging

# Adicionar o diretório 'src' ao sys.path de forma robusta
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(project_root, 'src'))

# Importar as classes/funções necessárias
from logger import setup_logging
from minio_client import MinioClient

# --- Configuração de Logging para este script ---
logger = setup_logging(log_file_name="pesquisadores_download.log")
# --- FIM da Configuração de Logging ---

def main():
    logger.info("Iniciando script de download de dataset.")

    if len(sys.argv) < 3:
        logger.error("Uso correto: python download_dataset.py <bucket_name> <object_name>")
        sys.exit(1) # Melhor usar sys.exit(1) para indicar erro

    bucket = sys.argv[1]
    object_name = sys.argv[2]

    logger.info(f"Tentando baixar o objeto '{object_name}' do bucket '{bucket}'.")

    try:
        client = MinioClient()
        success = client.download_file(bucket, object_name)

        if success:
            logger.info(f"Download do arquivo '{object_name}' do bucket '{bucket}' realizado com sucesso na pasta Downloads.")
            print(f"Download do arquivo '{object_name}' do bucket '{bucket}' realizado com sucesso na pasta Downloads.") # Manter print
        else:
            logger.error(f"Falha no download do arquivo '{object_name}'. Verifique os logs para mais detalhes.")
            print("Falha no download. Verifique os logs para mais detalhes.") # Manter print
    except Exception as e:
        logger.critical(f"Erro inesperado no script de download: {e}", exc_info=True)
    finally:
        logger.info("Script de download de dataset finalizado.")

if __name__ == "__main__":
    main()