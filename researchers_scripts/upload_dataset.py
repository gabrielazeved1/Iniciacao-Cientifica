import os
import io
import logging
from minio import Minio
from minio.error import S3Error

# Configuração do logging para registrar informações e erros durante a execução
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def upload_dataset(minio_client, bucket_name, local_path, dataset_folder):
    """
    Realiza o upload de arquivos CSV de um diretório local para um bucket MinIO,
    organizando-os em uma pasta lógica dentro do bucket.

    Parâmetros:
    - minio_client: Instância autenticada do cliente MinIO.
    - bucket_name: Nome do bucket onde os arquivos serão armazenados.
    - local_path: Caminho local contendo os arquivos CSV para upload.
    - dataset_folder: Nome da pasta lógica dentro do bucket para organização dos arquivos.

    O método verifica a existência do bucket, criando-o se necessário, e 
    realiza o upload de cada arquivo CSV, registrando o processo via logs.
    """
    if not os.path.exists(local_path):
        logging.error(f"O caminho local '{local_path}' não foi encontrado.")
        return

    # Verifica se o bucket existe; cria caso não exista
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)
        logging.info(f"Bucket '{bucket_name}' criado com sucesso.")
    else:
        logging.info(f"Bucket '{bucket_name}' já existe.")

    # Itera sobre os arquivos CSV no diretório especificado
    for filename in os.listdir(local_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(local_path, filename)
            try:
                # Abre o arquivo em modo binário para leitura
                with open(file_path, "rb") as file_data:
                    file_bytes = file_data.read()
                    file_size = len(file_bytes)

                # Define o caminho completo do objeto dentro do bucket
                object_name = f"{dataset_folder}/{filename}"

                # Realiza o upload do arquivo para o MinIO
                minio_client.put_object(
                    bucket_name=bucket_name,
                    object_name=object_name,
                    data=io.BytesIO(file_bytes),
                    length=file_size,
                    content_type="text/csv"
                )
                logging.info(f"Arquivo '{filename}' enviado com sucesso para '{object_name}'.")
            except S3Error as error:
                logging.error(f"Falha ao enviar arquivo '{filename}': {error}")

if __name__ == "__main__":
    # Instancia o cliente MinIO com as credenciais e endpoint configurados
    client = Minio(
        "localhost:9000",
        access_key="minio",
        secret_key="miniol23",
        secure=False
    )

    # Definição das variáveis para execução do upload
    bucket = "datalake"
    local_dataset_path = "/Users/gabrielazevedo/Documents/IC/COMFAULDA/Normal_1"
    dataset_folder_name = "Normal_1"

    # Executa o upload dos arquivos CSV para o bucket especificado
    upload_dataset(client, bucket, local_dataset_path, dataset_folder_name)
