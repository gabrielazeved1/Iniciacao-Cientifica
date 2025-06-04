from minio import Minio

client = Minio("localhost:9000", access_key="minio", secret_key="miniol23", secure=False)
bucket_name = "datalake"

# lista de arquivos para baixar
arquivos_escolhidos = [
    "Normal_1/12.82.csv",
    "Normal_1/14.70.csv"
]

# download de arquivos escolhidos
for arquivo in arquivos_escolhidos:
    response = client.get_object(bucket_name, arquivo)
    
    with open(arquivo.split("/")[-1], "wb") as f:
        for chunk in response.stream(32 * 1024):
            f.write(chunk)
    
    print(f"{arquivo} baixado com sucesso.")
