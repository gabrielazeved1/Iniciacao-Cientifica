import sys
import os
import logging 


# adicionar o diretório 'src' ao sys.path . -> garantir que consiga encontrar outros modulos,mesmo executando em diretorio diferente.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(project_root, 'src'))

from logger import setup_logging
from minio_client import MinioClient

#  configuração de logging 
logger = setup_logging(log_file_name="pesquisadores_download.log")


def main():
    logger.info("Iniciando script de download de arquivo.")
    
    #verificar se tem os 3 argumentos necessarios
    if len(sys.argv) < 3:
        logger.error("Uso correto: python download_file.py <bucket_name> <object_name> [local_filename]") 
        print("Uso correto: python download_file.py <bucket_name> <object_name> [local_filename]") 
        sys.exit(1) 

    bucket = sys.argv[1]
    object_name = sys.argv[2]
    local_filename = sys.argv[3] if len(sys.argv) > 3 else None 

    logger.info(f"Tentando baixar o objeto '{object_name}' do bucket '{bucket}'.")
    #tratar erros
    try:
        client = MinioClient()
        success = client.download_file(bucket, object_name, local_filename) 

        if success:
            logger.info(f"Download do arquivo '{object_name}' do bucket '{bucket}' realizado com sucesso na pasta Downloads.")
            print(f" Download do arquivo '{object_name}' do bucket '{bucket}' realizado com sucesso na pasta Downloads.")
           
        else:
            logger.error(f"Falha no download do arquivo '{object_name}'. Verifique os logs para mais detalhes.")
            print(f"Falha no download do arquivo '{object_name}'. Verifique os logs para mais detalhes.")
    
    except Exception as e:
        logger.critical(f"Erro inesperado no script de download: {e}", exc_info=True)
        print(f"[✖] Ocorreu um erro inesperado: {e}")
        
    finally:
        logger.info("Download de arquivo finalizado.")

if __name__ == "__main__":
    main()