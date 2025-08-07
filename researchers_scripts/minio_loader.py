# minio_loader.py
import os
import sys
import pandas as pd
import logging
from dotenv import load_dotenv

# --- config logging ---
# esta parte e pra configurar o sistema de log do script
# eu uso o logging padrao do python pra registrar tudo que acontece
logging.basicConfig(
    level=logging.INFO, # o nivel de log e INFO entao vai registrar informacoes e erros
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("minio_loader.log"), # aqui eu digo pra salvar o log em um arquivo
        logging.StreamHandler(sys.stdout) # e aqui eu digo pra mostrar o log tambem no terminal
    ]
)
logger = logging.getLogger()


def load_dataset(bucket, path, key=None, secret=None, endpoint=None):
    """
    o objetivo é carrega arquivo CSV do MinIO diretamente para um DataFrame pandas na memria
    download -> RAM
    """
    # le as credenciais e o endereco do minio das variaveis de ambiente
    # se elas nao foram passadas como argumento na funcao
    key = key or os.getenv("MINIO_ACCESS_KEY")
    secret = secret or os.getenv("MINIO_SECRET_KEY")
    endpoint = endpoint or os.getenv("MINIO_ENDPOINT")

    if not key or not secret or not endpoint:
        # se as credenciais ou o endereco nao existirem eu dou um erro
        raise ValueError("Credenciais MinIO (key, secret, endpoint) devem ser configuradas ou passadas como argumento.")

    # aqui eu monto o caminho completo para o arquivo no minio usando s3://
    s3_path = f"s3://{bucket}/{path}"
    
    # e aqui eu defino as opcoes de conexao pro pandas se conectar ao minio
    # isso e o que permite o pandas funcionar como a gente quer
    storage_options = {
        "key": key,
        "secret": secret,
        "client_kwargs": {"endpoint_url": endpoint},
    }

    try:
        # eu registro no log que estou comecando a ler o arquivo
        logger.info(f"Lendo arquivo '{path}' do bucket '{bucket}' no Minio...")
        # aqui eu uso o pandas pra ler o csv direto pra um dataframe na memoria ram
        df = pd.read_csv(s3_path, storage_options=storage_options)
        # se der certo eu registro no log que consegui ler o arquivo e quantas linhas
        logger.info(f"Arquivo lido com sucesso, {len(df)} linhas carregadas.")
        return df # e a funcao retorna o dataframe pra ser usado
    except Exception as e:
        # se der algum erro na leitura eu registro e o script para
        logger.error(f"Erro ao ler arquivo: {e}", exc_info=True)
        raise

def main():
    # eu carrego as variaveis de ambiente do arquivo .env se ele existir
    load_dotenv()
    
    # tratamento de erros caso o usuario nao passe os argumentos certos no terminal
    if len(sys.argv) < 3:
        print("Uso: python minio_loader.py <bucket> <caminho_arquivo>")
        sys.exit(1)

    # aqui eu pego os argumentos que o usuario digitou no terminal
    bucket = sys.argv[1]
    path = sys.argv[2]

    try:
        # eu chamo a funcao load_dataset pra iniciar o processo de leitura
        df = load_dataset(bucket, path)
        print("\n=== Primeiras 5 linhas ===")
        print(df.head()) # eu mostro as primeiras 5 linhas do dataframe

        print("\n=== Estatísticas descritivas ===")
        print(df.describe(include='all')) # e mostro as estatisticas descritivas

        # essa e a parte interativa que eu fiz
        col = input("\nDigite o nome da coluna para filtrar (ou ENTER para pular): ").strip()
        if col and col in df.columns:
            val = input(f"Digite o valor para filtrar na coluna '{col}': ").strip()
            df_filtrado = df[df[col].astype(str) == val]
            print(f"\n=== Linhas filtradas onde {col} == '{val}' ===")
            print(df_filtrado)
        else:
            print("Nenhum filtro aplicado.")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    # aqui e onde o script comeca a rodar quando o usuario chama ele no terminal
    main()