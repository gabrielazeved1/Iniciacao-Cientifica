from .minio_client import MinioClient

class ListService:
    def __init__(self):
        self.client = get_minio_client()

    def list_buckets(self):
        """Lista todos os buckets no MinIO"""
        try:
            buckets = self.client.list_buckets()
            return [bucket.name for bucket in buckets]
        except Exception as e:
            logger.error(f"Falha ao listar buckets: {e}")
            raise