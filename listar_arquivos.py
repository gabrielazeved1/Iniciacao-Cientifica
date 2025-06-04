from minio import Minio

client = Minio("localhost:9000", access_key="minio", secret_key="miniol23", secure=False)

bucket_name = "datalake"
prefix = "Normal_1/"  # pasta dentro do bucket principal

# retorna todos os arquivos dentro da pasta prefix
objects = client.list_objects(bucket_name, prefix=prefix, recursive=True)

print("Arquivos disponíveis:")
for obj in objects:
    print(obj.object_name)
