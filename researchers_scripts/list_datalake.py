#researcher_scripts/list_datalake.py
import sys
import os
import logging


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(project_root, 'src'))


from logger import setup_logging
from minio_client import MinioClient

logger = setup_logging(log_file_name="pesquisadores_list_datalake.log")

def print_usage():
    print("Uso:")
    print("  python list_datalake.py") 
    print("    - Lista todos os buckets disponíveis.")
    print("  python list_datalake.py <nome_do_bucket>") 
    print("    - Lista o conteúdo (arquivos e pastas) na raiz do bucket.")
    print("  python list_datalake.py <nome_do_bucket> <caminho_da_pasta_no_bucket>") 
    print("    - Lista o conteúdo (arquivos e pastas) dentro da pasta especificada no bucket.")
    print("  python list_datalake.py <nome_do_bucket> <caminho_da_pasta_no_bucket> --recursive") 
    print("    - Lista todo o conteúdo recursivamente (subpastas e arquivos) dentro da pasta especificada.")

def main():
    logger.info("Iniciando script de exploração do Data Lake.")

    # Obter credenciais das variáveis de ambiente (como em outros scripts de pesquisador)
    access_key = os.environ.get("MINIO_ACCESS_KEY")
    secret_key = os.environ.get("MINIO_SECRET_KEY")

    if not access_key or not secret_key:
        logger.critical("Variáveis de ambiente MINIO_ACCESS_KEY e MINIO_SECRET_KEY não configuradas.")
        print("[✖] Erro: Configure as variáveis de ambiente MINIO_ACCESS_KEY e MINIO_SECRET_KEY com suas credenciais.")
        sys.exit(1)

    client = MinioClient(access_key=access_key, secret_key=secret_key)
    
    # Analisar os argumentos da linha de comando
    num_args = len(sys.argv)
    
    # Comandos como --recursive
    recursive_flag = False
    if "--recursive" in sys.argv:
        recursive_flag = True
        sys.argv.remove("--recursive") # Remove a flag para não atrapalhar a contagem de args
        num_args = len(sys.argv) # Atualiza a contagem

    if num_args == 1: # Apenas o nome do script (explore_datalake.py)
        # Listar todos os buckets
        logger.info("Listando todos os buckets.")
        buckets = client.list_buckets() # Reutiliza o método existente
        if buckets:
            print("\nBuckets disponíveis:")
            for b in buckets:
                print(f"- {b.name}")
        else:
            print("\nNenhum bucket disponível ou erro ao listar.")

    elif num_args >= 2 and num_args <= 3: # explore_datalake.py <bucket_name> [prefixo]
        bucket_name = sys.argv[1]
        prefix = sys.argv[2] if num_args == 3 else ""
        
        # Garante que prefixos de pastas terminem em '/'
        if prefix and not prefix.endswith('/') and not recursive_flag:
            # Se não for recursivo e for uma pasta, o prefixo deve terminar em '/' para listar o conteúdo 'direto'
            # Mas o MinIOClient trata isso internamente, então apenas garantimos a intenção
            pass 

        logger.info(f"Listando conteúdo para bucket '{bucket_name}', prefixo '{prefix}', recursivo={recursive_flag}.")
        
        folders, files = client.list_objects_and_prefixes(bucket_name, prefix=prefix, recursive=recursive_flag)

        print(f"\nConteúdo de '{bucket_name}/{prefix}' (recursivo: {recursive_flag}):")
        if folders:
            print("Pastas:")
            for f in sorted(folders):
                # Se não for recursivo, garante que o nome da pasta termine com /
                display_name = f if f.endswith('/') else f + '/'
                print(f"  [DIR] {display_name}")
        if files:
            print("Arquivos:")
            for f in sorted(files):
                print(f"  [FILE] {f}")
        if not folders and not files:
            print("  Conteúdo vazio ou prefixo não encontrado.")

    else: # Uso inválido
        print_usage()
        sys.exit(1)

    logger.info("Script de exploração do Data Lake finalizado.")

if __name__ == "__main__":
    main()