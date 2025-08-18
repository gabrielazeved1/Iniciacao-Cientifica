from fastapi import HTTPException, status
from minio.error import S3Error

class List:
    def __init__(self, minio_client):
        self.client = minio_client.client

    def list_all_buckets(self):
        try:
            return {"buckets": [b.name for b in self.client.list_buckets()]}
        except S3Error as err:
            raise HTTPException(status_code=500, detail=f"Erro ao listar buckets: {err}")

    def list_content(self, bucket_name: str, prefix: str = ""):
        try:
            return {"objects": [o.object_name for o in self.client.list_objects(bucket_name, prefix=prefix, recursive=False)]}
        except S3Error as err:
            raise HTTPException(status_code=500, detail=f"Erro ao listar conteúdo: {err}")
