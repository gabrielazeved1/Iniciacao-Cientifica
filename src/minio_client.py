from minio import Minio
from minio.error import S3Error

class MinioClient:
    def __init__(self, endpoint, access_key, secret_key):
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=False)

    def upload_file(self, bucket_name, object_name, file_path):
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
        self.client.fput_object(bucket_name, object_name, file_path)

    def download_file(self, bucket_name, object_name, file_path):
        self.client.fget_object(bucket_name, object_name, file_path)

    def list_buckets(self):
        return self.client.list_buckets()

    def list_objects(self, bucket_name):
        return self.client.list_objects(bucket_name)
"""
Papel do módulo minio_client.py
Esse módulo será o responsável por toda a comunicação direta com o servidor MinIO, ou seja:

Conectar ao MinIO com as credenciais corretas

Fazer upload de arquivos para buckets/pastas

Fazer download de arquivos do MinIO para a máquina local

Listar buckets e objetos disponíveis no MinIO

Criar buckets, se necessário

Outras operações básicas com objetos (deletar, copiar, etc.)

Por que centralizar isso?
Facilita a manutenção: só precisa mudar um lugar se a forma de conexão mudar.

Evita duplicação: os scripts de upload, download, listagem usam essas funções.

Abstrai detalhes do SDK: os usuários finais (pesquisadores) não precisam mexer diretamente no SDK.

Facilita testes unitários: você pode testar as funções isoladamente.

Possibilita implementar logs, tratamento de erros e reconexões de forma centralizada.
"""