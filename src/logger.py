import logging
import os
from datetime import datetime

def setup_logging(log_file_name="app.log"):
    """
    Configura o log para a aplicação.
    Os logs serão gravados no diretório 'logs/'.
    """
    # Constrói o caminho para o diretório 'logs' de forma robusta
    # Ir um nível acima de 'src', e então entrar em 'logs'
    log_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
    os.makedirs(log_directory, exist_ok=True) # Garante que o diretório 'logs' exista

    log_file_path = os.path.join(log_directory, log_file_name)

    # Cria um logger
    logger = logging.getLogger('minio_datalake_app')
    logger.setLevel(logging.INFO) # Define o nível mínimo de log

    # Cria os handlers
    # Handler para arquivo
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)

    # Handler para console (para desenvolvimento/depuração)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG) # Você pode querer uma saída mais verbosa no console

    # Cria formatadores e os adiciona aos handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Adiciona os handlers ao logger
    if not logger.handlers: # Evita adicionar handlers duplicados se setup_logging for chamado várias vezes
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Você pode chamar setup_logging() aqui se quiser inicializá-lo imediatamente
# Para uma solução mais robusta, você pode querer chamá-lo de main.py