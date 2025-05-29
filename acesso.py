from minio import Minio

client = Minio("ip_servidor:9000", access_key="minio", secret_key="miniol23", secure=False)

data = client.get_object("datalake", "Normal_1/arquivo.csv")

# salvar localmente 
with open("arquivo.csv", "wb") as f: # o modo "wb" significa "write binary"
    for chunk in data.stream(32*1024):
        f.write(chunk)
