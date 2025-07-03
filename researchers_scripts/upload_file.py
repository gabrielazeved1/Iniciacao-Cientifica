import os
import sys
import logging
from logger import setup_logging
from minio_client import MinioClient

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(project_root, 'src'))


logger = setup_logging(log_file_name="pesquisadores_upload.log")


def main():
    logger.info("Iniciando script de upload do arquivo.")

    # colocar 3 ou 4 argumentos (script, bucket, arquivo, [prefixo])
    if len(sys.argv) < 3:
        logger.error("Uso correto: python upload_file.py <bucket_name> <caminho_arquivo_local> [pasta_destino_no_bucket]")
        sys.exit(1)

    bucket_name = sys.argv[1]
    file_path = sys.argv[2]
    # captura de prefixo
    object_prefix = sys.argv[3] if len(sys.argv) > 3 else ""

    # log da tentativa de upload
    logger.info(f"Tentando fazer upload do arquivo '{file_path}' para o bucket '{bucket_name}' na pasta '{object_prefix}'.")

    try:
        client = MinioClient()
        success = client.upload_file(bucket_name, file_path, object_prefix=object_prefix)

        if success:
            final_object_name = os.path.basename(file_path)
            if object_prefix:
                final_object_name = f"{object_prefix.strip('/')}/{final_object_name}"
            logger.info(f"Arquivo '{file_path}' enviado como '{final_object_name}' para o bucket '{bucket_name}' com sucesso.")
        
        else:
            logger.error(f"Falha no envio do arquivo '{file_path}'. Verifique os logs para mais detalhes.")
    
    except Exception as e:
        logger.critical(f"Erro inesperado no script de upload: {e}", exc_info=True)
        
    finally:
        logger.info("Script de upload do arquiv finalizado.")

if __name__ == "__main__":
    main()