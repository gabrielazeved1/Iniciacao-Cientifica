import os
import logging 
from minio import Minio
from minio.error import S3Error

"""
minio_client.py
aqui tem a classe do Minio_Client que sera instanciada e as funcoes principais do codigo
upload(diretorio e arquivos), downloads (diretorio e arquivos), list (diretorio e arquivos)


"""
logger = logging.getLogger('minio_datalake_app')

#classe que sera instancianda no main.py(aqui esta o ip, e login)
class MinioClient:
    def __init__(self, endpoint="127.0.0.1:9000", access_key="minio", secret_key="miniol23", secure=False):
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        logger.info("MinioClient inicializado com endpoint: %s", endpoint)



    def upload_file(self, bucket_name: str, local_path: str, object_name: str = None, object_prefix: str = "") -> bool:
        """
        faz o upload de um arquivo local para um bucket no MinIO.
        -bucket_name: O nome do bucket de destino no MinIO.
        -local_path: O caminho completo do arquivo local a ser upado.
        - object_name:O nome do objeto no MinIO. Se None, usa o nome base do arquivo local. (Opcional)
        - object_prefix:Um prefixo para adicionar ao nome do objeto no MinIO (simula pastas). (Opcional)
        -return: True se o upload for bem-sucedido, False caso contrário.
        primeiro verifica se o arquivo local para upload existe
        depois verifica se o bucket existe
        se nao ha especificacao do nome do objeto -> objeto=nomearquivo
        """
        #verifica o se existe o arquivo local
        if not os.path.isfile(local_path):
            logger.error(f"Arquivo '{local_path}' não encontrado para upload.")
            return False
        #verifica se existe o buckt, no qual estou tentando mandar
        if not self.client.bucket_exists(bucket_name):
            logger.info(f"Bucket '{bucket_name}' não existe. Tentando criar...")
            try:
                self.client.make_bucket(bucket_name)
                logger.info(f"Bucket '{bucket_name}' criado com sucesso.") 
            except S3Error as err:
                logger.error(f"Erro S3 ao tentar criar o bucket '{bucket_name}': {err}")
                return False
            except Exception as e:
                logger.error(f"Erro inesperado ao criar o bucket '{bucket_name}': {e}")
                return False
        #mudar nome do arquivo, (opcional)
        if object_name is None:
            object_name = os.path.basename(local_path)

        #colocar prefixo (opcional) ->simulacao de subpastas
        
        if object_prefix:
            object_prefix = object_prefix.strip('/')
            object_name = f"{object_prefix}/{object_name}"
       

        try:
            # Mensagem de INFO no log para o início da operação de upload do arquivo específico.
            logger.info(f"Iniciando upload de '{local_path}' para '{bucket_name}/{object_name}'.")
            with open(local_path, "rb") as file_data:
                file_size = os.path.getsize(local_path)
                self.client.put_object(
                    bucket_name=bucket_name,
                    object_name=object_name, 
                    data=file_data,
                    length=file_size,
                    content_type="application/octet-stream"
                )
            # Log de sucesso final do upload do arquivo (INFO - vai para o arquivo)
            logger.info(f"Upload de '{local_path}' como '{object_name}' no bucket '{bucket_name}' realizado com sucesso.")
            return True
        except S3Error as err:
            logger.error(f"Erro S3 no upload de '{local_path}' para '{bucket_name}/{object_name}': {err}", exc_info=True)
            return False
        except Exception as err:
            logger.error(f"Erro inesperado no upload de '{local_path}': {err}", exc_info=True)
            return False

    def download_file(self, bucket_name: str, object_name: str, local_filename: str = None) -> bool:
        """
        faz o download de um objeto=arquivo do MinIO para um arquivo local

        bucket_name: O nome do bucket onde o objeto está.
        object_name: O nome do objeto no MinIO a ser baixado. -> nome do arquivo que deseja baixar
        local_filename: O nome do arquivo local a ser salvo. Se None, usa o object_name (Opcional.)
        return: True se o download for bem-sucedido, False caso contrário.
        """
        try:
            # define o caminho para a pasta 'Downloads' do usuário.
            # os.path.expanduser("~") expande para o diretório home do usuário.
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            if not os.path.exists(downloads_path):
                os.makedirs(downloads_path)
                # Log quando o diretório de Downloads é criado (INFO - vai para o arquivo)
                logger.info(f"Diretório de Downloads '{downloads_path}' criado.")

            # define o nome do arquivo local.
            if local_filename is None:
                local_filename = object_name
            # combina o caminho da pasta Downloads com o nome do arquivo local.
            local_path = os.path.join(downloads_path, local_filename)

            # Log para o início da tentativa de download 
            logger.info(f"Tentando baixar '{object_name}' do bucket '{bucket_name}' para '{local_path}'.")

            # verifica se o objeto existe no MinIO antes de tentar baixá-lo.
            try:
                self.client.stat_object(bucket_name, object_name)
            except S3Error as err:
                # se o erro for "NoSuchKey", significa que o objeto não existe.
                if err.code == "NoSuchKey":
                    logger.error(f"Objeto '{object_name}' não encontrado no bucket '{bucket_name}'.")
                else:
                    # Outros erros S3 ao verificar o objeto.
                    logger.error(f"Erro S3 ao verificar objeto '{object_name}': {err}")
                return False # Indica falha porque o objeto não foi encontrado ou houve outro erro.

            # obtém o objeto do MinIO.
            # data será um objeto de fluxo (stream) do qual você pode ler os dados do arquivo.
            data = self.client.get_object(bucket_name, object_name)

            # salva os dados do objeto no arquivo local.
            with open(local_path, "wb") as file_data:
                # itera sobre o fluxo de dados em blocos de 32KB para economizar memória e lidar com arquivos grandes de forma eficiente.
                for chunk in data.stream(32*1024):
                    file_data.write(chunk)

            # registra sucesso no log. (INFO - vai para o arquivo)
            logger.info(f"Arquivo '{object_name}' do bucket '{bucket_name}' baixado em '{local_path}'.")
            return True 

        except S3Error as err:
            # captura erros específicos da API S3 durante o download.
            logger.error(f"Erro S3 no download de '{object_name}' do bucket '{bucket_name}': {err}", exc_info=True)
            return False # indica falha no download.
        except Exception as e:
            # captura outros erros inesperados durante o download.
            logger.error(f"Erro inesperado no download de '{object_name}': {e}", exc_info=True)
            return False # indica falha no download.

    def list_buckets(self):
        """
        lista todos os buckets existentes na instância do MinIO.

        return: uma lista de objetos Bucket (do SDK do MinIO) se a operação for bem-sucedida,
                 ou uma lista vazia em caso de erro.
        """
        try:
            # Log para o início da consulta (INFO - vai para o arquivo)
            logger.info("Consultando buckets existentes no MinIO.")
            buckets = self.client.list_buckets() 
            # Log dos buckets encontrados (INFO - vai para o arquivo)
            logger.info("Buckets encontrados:") 
            for bucket in buckets:
                logger.info(f" - {bucket.name} (Criado em: {bucket.creation_date})")
            return buckets 
        except S3Error as err:
            # captura erros específicos da API S3 ao listar buckets.
            logger.error(f"Erro S3 ao listar buckets: {err}", exc_info=True)
            return [] # retorna lista vazia em caso de erro.
        except Exception as e:
            # captura outros erros inesperados ao listar buckets.
            logger.error(f"Erro inesperado ao listar buckets: {e}", exc_info=True)
            return [] # retorna lista vazia em caso de erro.

    def list_objects_and_prefixes(self, bucket_name: str, prefix: str = "", recursive: bool = False) -> tuple[list, list]:
        """
        lista objetos e prefixos (pastas) dentro de um bucket.

        bucket_name: Nome do bucket.
        prefix: Prefixo para filtrar os objetos (simula subpastas).
        recursive: Se True, lista recursivamente todo o conteúdo do prefixo.
        :return: Uma tupla contendo duas listas: (pastas, arquivos).
        """
        folders = set() # nao armaenar a mesma pasta 2x
        files = []

        # Log para o início da operação (INFO - vai para o arquivo)
        logger.info(f"Listando conteúdo do bucket '{bucket_name}' com prefixo '{prefix}', recursivo={recursive}.")

        try:
            # Verifica se o bucket existe antes de tentar listar
            if not self.client.bucket_exists(bucket_name):
                logger.warning(f"O bucket '{bucket_name}' não existe. Não é possível listar o conteúdo.")
                return ([], [])

            # O método list_objects do MinIO já retorna objetos com 'is_dir=True' para pastas (common prefixes)
            # quando recursive=False.
            objects = self.client.list_objects(bucket_name, prefix=prefix, recursive=recursive)

            for obj in objects:
                if obj.is_dir: # Se for um diretório (prefixo comum)
                    folders.add(obj.object_name)
                else: # Se for um arquivo
                    files.append(obj.object_name)

            logger.info(f"Conteúdo encontrado para prefixo '{prefix}': Pastas={len(folders)}, Arquivos={len(files)}.") 
            return (sorted(list(folders)), sorted(files))

        except Exception as e:
            logger.error(f"Erro ao listar conteúdo do bucket '{bucket_name}' com prefixo '{prefix}': {e}", exc_info=True)
            return ([], [])

    def upload_directory(self, bucket_name: str, local_directory: str, minio_base_prefix: str = "") -> bool:
        """
        faz o upload recursivo de um diretório local para um bucket no MinIO.
        isso significa que ele percorre todas as subpastas e arquivos dentro do diretório local
        e os envia para o MinIO, mantendo a estrutura de "pastas" (prefixos).

        bucket_name: Nome do bucket no MinIO onde os arquivos serão upados.
        local_directory: caminho completo do diretório local a ser upado.
        minio_base_prefix:  o prefixo (caminho virtual de pasta) no MinIO para os arquivos.(opcional.)
        return: True se TODOS os uploads forem bem-sucedidos, False caso um ou mais arquivos falhem.
        """
        # verifica se o caminho local é um diretório válido.
        if not os.path.isdir(local_directory):
            logger.error(f"Diretório local '{local_directory}' não encontrado para upload de diretório.")
            return False

        # verifica se o bucket existe. se não, tenta criá-lo (mesma lógica do upload_file).
        if not self.client.bucket_exists(bucket_name):
            logger.info(f"Bucket '{bucket_name}' não existe. Tentando criar...")
            try:
                self.client.make_bucket(bucket_name)
                logger.info(f"Bucket '{bucket_name}' criado com sucesso para upload de diretório.")
            except S3Error as err:
                logger.error(f"Erro S3 ao tentar criar o bucket '{bucket_name}': {err}")
                return False
            except Exception as e:
                logger.error(f"Erro inesperado ao criar o bucket '{bucket_name}': {e}")
                return False

        all_successful = True # flag para controlar se todos os uploads individuais foram bem-sucedidos.
        num_files_uploaded = 0 # contador de arquivos upados com sucesso.
        num_files_failed = 0 # contador de arquivos que falharam.

        # define o prefixo base no MinIO.
        # se minio_base_prefix não for fornecido, usa o nome do diretório local
        if not minio_base_prefix:
            minio_base_prefix = os.path.basename(os.path.normpath(local_directory)) + "/"

        logger.info(f"Iniciando upload recursivo do diretório '{local_directory}' para '{bucket_name}/{minio_base_prefix}'.")
        # percorre recursivamente o diretório local.
        # os.walk() gera tuplas (root, dirs, files) para cada diretório na árvore.
        for root, dirs, files in os.walk(local_directory):
            for file_name in files: # itera sobre cada arquivo no diretório atual (root).
                local_file_path = os.path.join(root, file_name) # caminho completo do arquivo local.

                # calcula o nome do objeto no MinIO, mantendo a estrutura de diretórios.
                # os.path.relpath calcula o caminho do arquivo relativo ao diretório base.
                relative_path = os.path.relpath(local_file_path, local_directory)
                # combina o prefixo base do MinIO com o caminho relativo e substitui '\' por '/'
                # para garantir a formatação correta de caminhos no MinIO (que usa '/')
                minio_object_name = os.path.join(minio_base_prefix, relative_path).replace("\\", "/")

                # Log detalhado POR ARQUIVO, usando DEBUG para não poluir o INFO
                logger.debug(f"Processando arquivo para upload: '{local_file_path}' como '{minio_object_name}'.") 
                try:
                    with open(local_file_path, "rb") as file_data:
                        file_size = os.path.getsize(local_file_path)
                        self.client.put_object(
                            bucket_name=bucket_name,
                            object_name=minio_object_name,
                            data=file_data,
                            length=file_size,
                            content_type="application/octet-stream"
                        )
                    # Log de sucesso por arquivo (também em DEBUG)
                    logger.debug(f"Upload de '{local_file_path}' bem-sucedido.") 
                    num_files_uploaded += 1 
                except S3Error as err:
                    #loga erro S3 para o arquivo específico e marca o upload geral como não totalmente bem-sucedido.
                    logger.error(f"Erro S3 ao fazer upload de '{local_file_path}' para '{bucket_name}/{minio_object_name}': {err}", exc_info=True)
                    all_successful = False
                    num_files_failed += 1 
                except Exception as e:
                    # loga outros erros para o arquivo específico e marca o upload geral como não totalmente bem-sucedido.
                    logger.error(f"Erro inesperado ao fazer upload de '{local_file_path}': {e}", exc_info=True)
                    all_successful = False
                    num_files_failed += 1 

        
        if all_successful:
            logger.info(f"Upload do diretório '{local_directory}' para '{bucket_name}/{minio_base_prefix}' concluído com sucesso. ({num_files_uploaded} arquivos upados).")
        else:
            logger.error(f"Upload do diretório '{local_directory}' para '{bucket_name}/{minio_base_prefix}' finalizado com erros. ({num_files_uploaded} arquivos upados, {num_files_failed} falharam).")
        return all_successful 