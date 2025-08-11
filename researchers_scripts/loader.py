import os
import pandas as pd
import logging
import sys
class Loader:
    
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