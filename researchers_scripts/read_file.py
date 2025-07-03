import sys
import os
import pandas as pd
import logging 


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(project_root, 'src'))

from logger import setup_logging
logger = setup_logging(log_file_name="pesquisadores_read_file.log")


def read_csv_from_minio(bucket_name, file_path):
    """
    leitura do arquivo csv de forma direta
    """
    logger.info(f"Tentando ler CSV do MinIO: bucket='{bucket_name}', arquivo='{file_path}'")
    s3_path = f"s3://{bucket_name}/{file_path}"
    storage_options = {
        "key": "minio",
        "secret": "miniol23",
        "client_kwargs": {"endpoint_url": "http://localhost:9000"},
    }
    try:
        df = pd.read_csv(s3_path, storage_options=storage_options)
        logger.info(f"Arquivo '{file_path}' lido com sucesso do bucket '{bucket_name}'.")
        return df
    except Exception as e:
        logger.error(f"Falha ao ler o arquivo CSV '{file_path}' do bucket '{bucket_name}': {e}", exc_info=True)
        raise 

def main():
    logger.info("Iniciando leitura do arquivo.")

    if len(sys.argv) < 3:
        logger.error("Uso correto: python read_file.py <bucket_name> <caminho_arquivo>")
        sys.exit(1)

    bucket = sys.argv[1]
    file_path = sys.argv[2]

    try:
        df = read_csv_from_minio(bucket, file_path)
        logger.info(f"Mostrando as primeiras 5 linhas do arquivo '{file_path}' no bucket '{bucket}'.")
        print(f"\nMostrando as primeiras linhas do arquivo '{file_path}' no bucket '{bucket}':\n")
        print(df.head())
        print("\n") # Adicionar uma nova linha para melhor legibilidade
    except Exception as e:
        logger.critical(f"Erro no script de leitura de dataset: {e}") # O erro já foi logado na função read_csv_from_minio
        print(f"\nErro ao ler o arquivo: {e}") # Manter print para output direto
    finally:
        logger.info("Script de leitura de dataset finalizado.")

if __name__ == "__main__":
    main()