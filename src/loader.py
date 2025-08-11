# src/loader.py
import os
import logging
from dotenv import load_dotenv
import pandas as pd
import sys

# Adiciona o diretorio src ao caminho para que o logger possa ser encontrado
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(project_root, 'src'))

from logger import setup_logging

# Configura o logger para a classe Loader
logger = setup_logging(log_file_name="minio_loader.log")


class Loader:
    """
    Classe para carregar dados de forma específica do MinIO, como CSV para um DataFrame.
    """
    def __init__(self):
        # O construtor é simples, mas pode ser usado para inicializações futuras.
        pass

    def load_dataset(self, bucket, path, key=None, secret=None, endpoint=None):
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