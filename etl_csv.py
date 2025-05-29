import os
import io
import logging
from minio import Minio

# configuração do logging: console + arquivo
log_file = "envio_minio.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file),logging.StreamHandler()]
)

# instancia o cliente MinIO
client = Minio("localhost:9000", "minio", "miniol23", secure=False)
bucket_name = "datalake"

# cria o bucket se ele não existir
if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)
    logging.info(f"Bucket '{bucket_name}' criado.")
else:
    logging.info(f"Bucket '{bucket_name}' já existe.")

# caminho local dos arquivos
local_dir = "/Users/gabrielazevedo/Documents/IC/COMFAULDA/Normal_1"

# envia os arquivos CSV
for filename in os.listdir(local_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(local_dir, filename)

        # lê o arquivo em modo binário
        with open(file_path, "rb") as f:
            file_data = f.read()
            file_size = len(file_data)

        # envia para o bucket criando pasta lógica
        client.put_object(
            bucket_name=bucket_name,
            object_name=f"Normal_1/{filename}",
            data=io.BytesIO(file_data),
            length=file_size,
            content_type="text/csv"
        )

        logging.info(f"Arquivo '{filename}' enviado com sucesso para o MinIO.")

logging.info("Todos os arquivos foram enviados para o MinIO.")
