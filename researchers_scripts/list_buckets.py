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
logger = setup_logging(log_file_name="pesquisadores_list_buckets.log")
# --- FIM da Configuração de Logging ---

def main():
    logger.info("Iniciando script para listar buckets.")

    try:
        client = MinioClient()
        buckets = client.list_buckets() # Usar o método list_buckets já existente na sua MinioClient

        if buckets:
            logger.info("Buckets disponíveis no MinIO:")
            print("\nBuckets disponíveis:") # Manter print para output direto ao pesquisador
            for b in buckets:
                logger.info(f"- {b.name} (Criado em: {b.creation_date})")
                print(f"- {b.name}") # Manter print para output direto ao pesquisador
        else:
            logger.info("Nenhum bucket encontrado ou erro ao listar buckets.")
            print("\nNenhum bucket disponível ou ocorreu um erro.") # Manter print para output direto ao pesquisador

    except Exception as e:
        logger.critical(f"Erro inesperado no script de listagem de buckets: {e}", exc_info=True)
    finally:
        logger.info("Script para listar buckets finalizado.")

if __name__ == "__main__":
    main()