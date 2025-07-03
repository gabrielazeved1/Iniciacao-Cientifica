import sys
import os
import logging 


# adicionar o diretório 'src' ao sys.path 
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(project_root, 'src'))

from logger import setup_logging
from minio_client import MinioClient

# configuração de logging 
logger = setup_logging(log_file_name="pesquisadores_list_contents.log")


def list_objects_and_log(minio_client_instance, bucket_name, prefix=""):
    """
    lista objetos e pastas em um bucket e loga os resultados.
    """
    logger.info(f"Listando conteúdo do bucket '{bucket_name}' com prefixo '{prefix}'.")
    try:
        objects = minio_client_instance.client.list_objects(bucket_name, prefix=prefix, recursive=False)
        folders = set()
        files = []
        prefix_len = len(prefix)

        for obj in objects:
            rest_key = obj.object_name[prefix_len:]
            if "/" in rest_key:
                folder = rest_key.split("/")[0]
                folders.add(folder)
            else:
                files.append(rest_key)

        if folders:
            logger.info(f"Pastas encontradas em '{bucket_name}': {sorted(folders)}")
            for f in sorted(folders):
                print(f"  [DIR] {f}")
        if files:
            logger.info(f"Arquivos encontrados em '{bucket_name}': {sorted(files)}")
            for f in sorted(files):
                print(f"  {f}")
        if not folders and not files:
            logger.info(f"Conteúdo vazio para o bucket '{bucket_name}' com prefixo '{prefix}'.")

        return True 

    except Exception as e:
        logger.error(f"Erro ao listar conteúdo do bucket '{bucket_name}' com prefixo '{prefix}': {e}", exc_info=True)
        return False 

def main():
    logger.info("Iniciando script para listar conteúdo do bucket.")

    if len(sys.argv) < 2:
        logger.error("Uso correto: python list_bucket_contents.py <nome_bucket> [prefixo_opcional]")
        sys.exit(1)

    bucket = sys.argv[1]
    prefix = sys.argv[2] if len(sys.argv) > 2 else ""

    # Verifica se o bucket existe antes de tentar listar o conteúdo
    try:
        client = MinioClient()
        if not client.client.bucket_exists(bucket):
            logger.warning(f"O bucket '{bucket}' não existe.")
            sys.exit(1)

        print(f"Conteúdo do bucket '{bucket}' com prefixo '{prefix}':")
        list_objects_and_log(client, bucket, prefix)

    except Exception as e:
        logger.critical(f"Erro inesperado no script de listagem de conteúdo do bucket: {e}", exc_info=True)
    finally:
        logger.info("Script para listar conteúdo do bucket finalizado.")


if __name__ == "__main__":
    main()