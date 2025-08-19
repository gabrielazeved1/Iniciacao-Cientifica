from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from .models.auth import MinioCredentials
from .utils.session import get_current_user, create_session_token, session_store
from .minio_client import MinioClient
from .upload import Upload
from .list import List
from .download import Download


app = FastAPI()

# Simulação de banco de usuários
fake_db = {
    "minio": "miniol23",
    "amanda": "amanda123",
    "pedro": "pedro456"
}

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do Datalake MinIO!"}

@app.post("/login")
def login(credentials: MinioCredentials):
    if not (credentials.access_key in fake_db and fake_db[credentials.access_key] == credentials.secret_key):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_session_token(credentials.access_key)
    session_store[token] = {
        "access_key": credentials.access_key,
        "secret_key": credentials.secret_key
    }
    return {"session_token": token}

# Dependências
def get_upload_instance(token: str = Depends(get_current_user)) -> Upload:
    session = session_store.get(token)
    if not session:
        raise HTTPException(status_code=401, detail="Sessão inválida ou expirada")
    client = MinioClient(access_key=session["access_key"], secret_key=session["secret_key"])
    return Upload(client)

def get_list_instance(token: str = Depends(get_current_user)) -> List:
    session = session_store.get(token)
    if not session:
        raise HTTPException(status_code=401, detail="Sessão inválida ou expirada")
    client = MinioClient(access_key=session["access_key"], secret_key=session["secret_key"])
    return List(client)

def get_download_instance(token: str = Depends(get_current_user)) -> Download:
    session = session_store.get(token)
    if not session:
        raise HTTPException(status_code=401, detail="Sessão inválida ou expirada")
    client = MinioClient(access_key=session["access_key"], secret_key=session["secret_key"])
    return Download(client)



# Rotas de listagem
@app.get("/buckets")
def list_buckets(list_service: List = Depends(get_list_instance)):
    return list_service.list_all_buckets()

@app.get("/buckets/{bucket_name}")
def list_buckets_content(bucket_name: str, prefix: str = "", list_service: List = Depends(get_list_instance)):
    return list_service.list_content(bucket_name, prefix)

# Rotas de upload
@app.post("/upload/file")
async def upload_file_api(bucket_name: str, file: UploadFile = File(...), prefix: str = "", upload_service: Upload = Depends(get_upload_instance)):
    result = upload_service.upload_file(bucket_name, file, prefix)
    if not result:
        raise HTTPException(status_code=500, detail="Falha no upload do arquivo")
    return {"message": "Arquivo enviado com sucesso", "object_name": result}

@app.post("/upload/directory")
def upload_directory_api(bucket_name: str, local_directory: str, prefix: str = "", upload_service: Upload = Depends(get_upload_instance)):
    success = upload_service.upload_directory(bucket_name, local_directory, prefix)
    if not success:
        raise HTTPException(status_code=500, detail="Falha no upload do diretório")
    return {"message": "Diretório enviado com sucesso"}

# Rotas de download
@app.get("/download/file")
def download_file_api(bucket_name: str, object_name: str, local_filename: str = None, download_service: Download = Depends(get_download_instance)):
    success = download_service.download_file(bucket_name, object_name, local_filename)
    if not success:
        raise HTTPException(status_code=500, detail="Falha ao baixar arquivo")
    return {"message": f"Arquivo '{object_name}' baixado com sucesso"}

@app.get("/download/directory")
def download_directory_api(bucket_name: str, prefix: str, local_directory: str = None, download_service: Download = Depends(get_download_instance)):
    success = download_service.download_directory(bucket_name, prefix, local_directory)
    if not success:
        raise HTTPException(status_code=500, detail="Falha ao baixar diretório")
    return {"message": f"Diretório '{prefix}' baixado com sucesso"}

