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
    print("Iniciando a verificação e configuração do ambiente do Data Lake...") 

    try:
        #instancia o Minio
        minio_client = MinioClient() 

        try:
            logger.info("Testando conexão com o MinIO...")
            print("Testando conexão com o MinIO...")
            minio_client.client.list_buckets() # se listar ta conectado
            logger.info("Conexão com MinIO estabelecida com sucesso.")
            print(" Conexão com MinIO estabelecida com sucesso.") 
        except Exception as e:
            logger.critical(f"NÃO FOI POSSÍVEL CONECTAR AO MINIO. Verifique se o MinIO está rodando e acessível. Erro: {e}")
            print(f"ERRO: NÃO FOI POSSÍVEL CONECTAR AO MINIO. Verifique se o MinIO está rodando e acessível. Detalhes no log.") 
            sys.exit(1) 

        # garante que ha buckts ja criados
        essential_buckets = ["datalake", "backup"]
        print("\nVerificando buckets essenciais:") 
        # se ja nao tiver sido criado, ele cria
        for bucket in essential_buckets:
            if not minio_client.client.bucket_exists(bucket):
                logger.info(f"Bucket '{bucket}' não existe. Criando...")
                print(f"  - Bucket '{bucket}' não existe. Criando...") 
                try:
                    minio_client.client.make_bucket(bucket)
                    logger.info(f"Bucket '{bucket}' criado com sucesso.")
                    print(f"   Bucket '{bucket}' criado com sucesso.") 
                except Exception as e:
                    logger.error(f"Falha ao criar o bucket '{bucket}': {e}")
                    print(f" Falha ao criar o bucket '{bucket}'. Detalhes no log.") 
            else:
                logger.info(f"Bucket '{bucket}' já existe. Ok.")
                print(f"  Bucket '{bucket}' já existe. Ok.")

        logger.info("Verificação e configuração do ambiente do Data Lake concluída.")
        print("\n Verificação e configuração do ambiente do Data Lake concluída com sucesso!")

    except Exception as e:
        logger.critical(f"Ocorreu um erro crítico durante a inicialização do ambiente do Data Lake: {e}", exc_info=True)
        print(f"ERRO CRÍTICO DURANTE A INICIALIZAÇÃO DO DATA LAKE. Detalhes no log.") 
    finally:
        logger.info("Processo de inicialização do ambiente finalizado.")
        print("Processo de inicialização do ambiente finalizado.") 

if __name__ == "__main__":
   
    initialize_datalake_environment()