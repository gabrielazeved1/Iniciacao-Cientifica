from fastapi import FastAPI
from . import routes
import uvicorn

app = FastAPI(
    title="API de Teste de Conexão com MinIO",
    description="Endpoint para verificar a conexão e credenciais com o MinIO.",
    version="1.0.0"
)

app.include_router(routes.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
