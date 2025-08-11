import os
print('--- Verificando Variaveis de Ambiente MinIO ---')
print('MINIO_ACCESS_KEY:', os.environ.get('MINIO_ACCESS_KEY'))
print('MINIO_SECRET_KEY:', os.environ.get('MINIO_SECRET_KEY'))
print('MINIO_ENDPOINT:', os.environ.get('MINIO_ENDPOINT'))
