import os
import sys
import logging
import subprocess
import datetime
import shutil

# Adiciona o diretório 'src' ao sys.path para importar o logger
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(project_root, 'src'))

from logger import setup_logging

logger = setup_logging(log_file_name="datalake_backup.log")

MINIO_ALIAS = "localminio"  # Nome do alias MinIO configurado com 'mc alias set'

# --- AJUSTE ESTE CAMINHO PARA O SEU MAC ---
BACKUP_BASE_DIR = "/Users/gabrielazevedo/minio_backups" # Exemplo para Mac
# --- FIM DO AJUSTE ---

BUCKETS_TO_BACKUP = ["datalake", "backup"]

DAILY_RETENTION_DAYS = 7 # Manter backups diários por 7 dias

def run_mc_command(command_args, description):
    logger.info(f"Executando comando mc: {' '.join(command_args)}")
    try:
        result = subprocess.run(command_args, capture_output=True, text=True, check=True)
        logger.info(f"{description} sucesso.")
        logger.debug(f"Saída do mc: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"{description} falhou com erro: {e.stderr}", exc_info=True)
        return False
    except FileNotFoundError:
        logger.critical(f"Comando 'mc' não encontrado. Certifique-se de que o MinIO Client (mc) está instalado e no PATH.")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado ao executar comando mc: {e}", exc_info=True)
        return False

def perform_backup():
    logger.info("--- Iniciando processo de backup do Data Lake MinIO ---")
    
    # Criar diretórios base se não existirem
    os.makedirs(os.path.join(BACKUP_BASE_DIR, "daily"), exist_ok=True)

    # Criar um diretório para o backup diário com timestamp
    current_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    daily_backup_dir = os.path.join(BACKUP_BASE_DIR, "daily", current_timestamp)
    os.makedirs(daily_backup_dir, exist_ok=True)
    logger.info(f"Diretório de backup diário criado: {daily_backup_dir}")

    all_backups_successful = True
    for bucket_name in BUCKETS_TO_BACKUP:
        source_path = f"{MINIO_ALIAS}/{bucket_name}"
        destination_path = os.path.join(daily_backup_dir, bucket_name)
        
        logger.info(f"Espelhando bucket '{bucket_name}' de {source_path} para {destination_path}")
        # Usar --overwrite para garantir que a cópia seja uma imagem completa do bucket naquele timestamp
        success = run_mc_command(["mc", "mirror", "--overwrite", source_path, destination_path],
                                 f"Espelhamento do bucket '{bucket_name}'")
        if not success:
            all_backups_successful = False

    logger.info("--- Processo de espelhamento concluído ---")
    
    # Executar a política de retenção
    perform_retention()

    if all_backups_successful:
        logger.info("--- Backup do Data Lake concluído com SUCESSO ---")
    else:
        logger.error("--- Backup do Data Lake concluído com ERROS ---")
        sys.exit(1)

def perform_retention():
    logger.info("Iniciando política de retenção de backups.")
    
    daily_dir_path = os.path.join(BACKUP_BASE_DIR, "daily")
    if os.path.exists(daily_dir_path):
        for entry in os.listdir(daily_dir_path):
            full_path = os.path.join(daily_dir_path, entry)
            if os.path.isdir(full_path):
                try:
                    # O nome do diretório deve corresponder a YYYYMMDD_HHMMSS
                    dir_date_str = entry.split('_')[0]
                    dir_date = datetime.datetime.strptime(dir_date_str, "%Y%m%d").date()
                    
                    if (datetime.date.today() - dir_date).days > DAILY_RETENTION_DAYS:
                        logger.info(f"Removendo backup diário antigo: {full_path}")
                        shutil.rmtree(full_path)
                except ValueError:
                    logger.warning(f"Diretório de backup diário com formato de nome inválido, ignorando: {entry}")
                except Exception as e:
                    logger.error(f"Erro ao remover diretório de backup diário: {full_path}: {e}", exc_info=True)
    
    logger.info("Política de retenção concluída.")

if __name__ == "__main__":
    perform_backup()