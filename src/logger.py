import logging
import os
from datetime import datetime

def setup_logging(log_file_name="app.log"):
    log_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
    os.makedirs(log_directory, exist_ok=True)

    log_file_path = os.path.join(log_directory, log_file_name)

    logger = logging.getLogger('minio_datalake_app')
    logger.setLevel(logging.INFO) # O nível geral do logger pode permanecer INFO (para o arquivo)

    if not logger.handlers:
        # File handler: Para registrar TUDO (INFO e acima) no arquivo de log
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.INFO) # Salva INFO, WARNING, ERROR, CRITICAL no arquivo
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING) # só WARNING, ERROR, CRITICAL no console
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger
