# minio_loader.py
import os
import sys
import pandas as pd
import logging
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import IPython 

# --- config logging ---
logging.basicConfig(
    level=logging.INFO,  
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("minio_loader.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger()


def load_dataset(bucket, path, key=None, secret=None, endpoint=None):
    """
    o objetivo é carregar um arquivo CSV do MinIO diretamente para um 
    DataFrame pandas na memória (download -> RAM)
    """
    key = key or os.getenv("MINIO_ACCESS_KEY")
    secret = secret or os.getenv("MINIO_SECRET_KEY")
    endpoint = endpoint or os.getenv("MINIO_ENDPOINT")

    if not key or not secret or not endpoint:
        raise ValueError("Credenciais MinIO (key, secret, endpoint) devem ser configuradas ou passadas como argumento.")

    s3_path = f"s3://{bucket}/{path}"
    storage_options = {
        "key": key,
        "secret": secret,
        "client_kwargs": {"endpoint_url": endpoint},
    }

    try:
        logger.info(f"Lendo arquivo '{path}' do bucket '{bucket}' no Minio...")
        df = pd.read_csv(s3_path, storage_options=storage_options)
        logger.info(f"Arquivo lido com sucesso, {len(df)} linhas carregadas.")
        return df
    except Exception as e:
        logger.error(f"Erro ao ler arquivo: {e}", exc_info=True)
        raise





def main():
    load_dotenv()

    if len(sys.argv) < 3:
        print("Uso: python minio_loader.py <bucket> <caminho_arquivo>")
        sys.exit(1)

    bucket = sys.argv[1]
    path = sys.argv[2]
    
    access_key = os.environ.get("MINIO_ACCESS_KEY")
    secret_key = os.environ.get("MINIO_SECRET_KEY")
    endpoint = os.environ.get("MINIO_ENDPOINT")

    if not access_key or not secret_key or not endpoint:
        print("[✖] Erro: Credenciais MinIO (key, secret, endpoint) não estão configuradas.")
        print("Use o script de login: 'source researchers_scripts/login_datalake.sh usuario senha [endpoint]'")
        sys.exit(1)

    try:
        # carrega o dataset
        df = load_dataset(bucket, path)

        print("verificando se deu certo...")
        # aqui entra o shell interativo
        IPython.embed()
        

    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()