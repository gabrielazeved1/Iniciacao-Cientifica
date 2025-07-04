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
    print("Iniciando a verificação e configuração do ambiente do Data Lake...") # Print inicial

    try:
        # AQUI VOCÊ PRECISA DECIDIR O ENDPOINT PARA TESTES NO HOST
        # Se você está rodando no host e o MinIO via Docker Compose, use 127.0.0.1:9000
        # Se já instalou MinIO nativo no servidor, use o IP real do servidor.
        # minio_client = MinioClient(endpoint="127.0.0.1:9000") # Ou seu IP real, ou minio-server se estiver em ambiente Docker Compose
        
        # MELHOR ABORDAGEM: MinioClient lerá do ambiente, então defina a variável MINIO_ENDPOINT ANTES de rodar este script
        # Ex: export MINIO_ENDPOINT="127.0.0.1:9000"
        minio_client = MinioClient() # MinioClient agora resolve o endpoint via variável de ambiente

        try:
            logger.info("Testando conexão com o MinIO...")
            print("Testando conexão com o MinIO...") # Print de status
            minio_client.client.list_buckets()
            logger.info("Conexão com MinIO estabelecida com sucesso.")
            print(" Conexão com MinIO estabelecida com sucesso.") # Print de sucesso
        except Exception as e:
            logger.critical(f"NÃO FOI POSSÍVEL CONECTAR AO MINIO. Verifique se o MinIO está rodando e acessível. Erro: {e}")
            print(f"ERRO: NÃO FOI POSSÍVEL CONECTAR AO MINIO. Verifique se o MinIO está rodando e acessível. Detalhes no log.") # Print de erro
            sys.exit(1) 

        # Define os buckets essenciais para o seu Data Lake
        essential_buckets = ["datalake", "backup"]
        print("\nVerificando buckets essenciais:") # Print de status

        for bucket in essential_buckets:
            if not minio_client.client.bucket_exists(bucket):
                logger.info(f"Bucket '{bucket}' não existe. Criando...")
                print(f"  - Bucket '{bucket}' não existe. Criando...") # Print de status
                try:
                    minio_client.client.make_bucket(bucket)
                    logger.info(f"Bucket '{bucket}' criado com sucesso.")
                    print(f"   Bucket '{bucket}' criado com sucesso.") # Print de sucesso
                except Exception as e:
                    logger.error(f"Falha ao criar o bucket '{bucket}': {e}")
                    print(f" Falha ao criar o bucket '{bucket}'. Detalhes no log.") # Print de erro
            else:
                logger.info(f"Bucket '{bucket}' já existe. Ok.")
                print(f"  Bucket '{bucket}' já existe. Ok.") # Print de status

        logger.info("Verificação e configuração do ambiente do Data Lake concluída.")
        print("\n Verificação e configuração do ambiente do Data Lake concluída com sucesso!") # Print final de sucesso

    except Exception as e:
        logger.critical(f"Ocorreu um erro crítico durante a inicialização do ambiente do Data Lake: {e}", exc_info=True)
        print(f"ERRO CRÍTICO DURANTE A INICIALIZAÇÃO DO DATA LAKE. Detalhes no log.") # Print de erro crítico
    finally:
        logger.info("Processo de inicialização do ambiente finalizado.")
        print("Processo de inicialização do ambiente finalizado.") # Print final

if __name__ == "__main__":
   
    initialize_datalake_environment()