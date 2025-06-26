from flask import Flask, jsonify, request, send_file
from minio import Minio
from io import BytesIO
import os

app = Flask(__name__)

client = Minio("localhost:9000", "minio", "miniol23", secure=False)
bucket_name = "datalake"

@app.route("/listar-arquivos")
def listar_arquivos():
    pasta = request.args.get("pasta", "")  # pasta opcional para prefixo
    try:
        objetos = client.list_objects(bucket_name, prefix=pasta, recursive=True)
        arquivos = [obj.object_name for obj in objetos]
        if not arquivos:
            return jsonify({"mensagem": "Nenhum arquivo encontrado."}), 404
        return jsonify(arquivos)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route("/baixar-arquivo")
def baixar_arquivo():
    object_name = request.args.get("arquivo")
    if not object_name:
        return jsonify({"erro": "Parâmetro 'arquivo' é obrigatório."}), 400

    try:
        response = client.get_object(bucket_name, object_name)
        data = response.read()
        response.close()
        response.release_conn()

        filename = os.path.basename(object_name)
        return send_file(
            BytesIO(data),
            download_name=filename,
            as_attachment=True
        )
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route("/")
def home():
    return "API Flask para listar e baixar arquivos do MinIO funcionando!"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
