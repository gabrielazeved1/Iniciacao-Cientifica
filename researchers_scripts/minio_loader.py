import os
import sys
import pandas as pd
import logging
from dotenv import load_dotenv
import matplotlib.pyplot as plt

# --- config logging ---
# esta parte e pra configurar o sistema de log do script
logging.basicConfig(
    level=logging.INFO,  # o nivel de log e INFO entao vai registrar informacoes e erros
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("minio_loader.log"),  # aqui eu digo pra salvar o log em um arquivo
        logging.StreamHandler(sys.stdout)         # e aqui eu digo pra mostrar o log tambem no terminal
    ]
)
logger = logging.getLogger()


def load_dataset(bucket, path, key=None, secret=None, endpoint=None):
    """
    o objetivo é carregar um arquivo CSV do MinIO diretamente para um 
    DataFrame pandas na memória (download -> RAM)
    """
    key = key or os.getenv("MINIO_ACCESS_KEY")
    secret = secret or os.getenv("MINIO_SECRET_KEY")
    endpoint = endpoint or os.getenv("MINIO_ENDPOINT")

    if not key or not secret or not endpoint:
        raise ValueError("Credenciais MinIO (key, secret, endpoint) devem ser configuradas ou passadas como argumento.")

    s3_path = f"s3://{bucket}/{path}"
    storage_options = {
        "key": key,
        "secret": secret,
        "client_kwargs": {"endpoint_url": endpoint},
    }

    try:
        logger.info(f"Lendo arquivo '{path}' do bucket '{bucket}' no Minio...")
        df = pd.read_csv(s3_path, storage_options=storage_options)
        logger.info(f"Arquivo lido com sucesso, {len(df)} linhas carregadas.")
        return df
    except Exception as e:
        logger.error(f"Erro ao ler arquivo: {e}", exc_info=True)
        raise


def mostrar_info_basica(df):
    # mostra as primeiras 5 linhas do DataFrame
    print("\n=== Primeiras 5 linhas ===")
    print(df.head())

    # mostra estatísticas descritivas (contagem, média, desvio, etc)
    print("\n=== Estatísticas descritivas ===")
    print(df.describe(include='all'))


def verificar_qualidade_dados(df):
    print("\n=== Verificação de Qualidade dos Dados ===")

    # mostra quantos valores ausentes tem em cada coluna
    print("\n--- Valores Ausentes por Coluna ---")
    print(df.isnull().sum())

    # mostra quantos valores únicos existem em cada coluna
    print("\n--- Contagem de Valores Únicos por Coluna ---")
    print(df.nunique())


def calcular_correlacao(df):
    print("\n--- Matriz de Correlação ---")
    try:
        # pega só colunas numéricas
        df_numeric = df.select_dtypes(include=['number'])
        if not df_numeric.empty:
            print(df_numeric.corr())  # mostra a matriz de correlação
        else:
            print("Nenhuma coluna numérica encontrada para calcular correlação.")
    except Exception as e:
        logger.error(f"Erro ao calcular correlação: {e}")
        print("Erro ao calcular correlação.")


def gerar_histogramas(df):
    print("\n--- Histograma das Colunas Numéricas ---")
    try:
        df_numeric = df.select_dtypes(include=['number'])
        if not df_numeric.empty:
            # figsize=(15, 12) cria uma figura maior, dando mais espaço para cada histograma.
            df_numeric.hist(figsize=(15, 12)) 
            plt.suptitle('Distribuição das Colunas Numéricas', x=0.5, y=0.97, fontsize=16) # Posiciona o titulo
            plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Ajusta o layout para evitar sobreposicao
            
            # salvar foto/teste. acho que vou so mostrar a foto mesmo!!!
            print("preciso mudar isso aqui depois")
            nome_do_arquivo = "histograma_datalake.png"
            plt.savefig(nome_do_arquivo)
            
            plt.close() 
            
            print(f"Histogramas gerados e salvos no arquivo '{nome_do_arquivo}'.")
            logger.info(f"Histogramas salvos em '{nome_do_arquivo}'.")

        else:
            print("Nenhuma coluna numérica encontrada para gerar histogramas.")

    except Exception as e:
        logger.error(f"Erro ao gerar histogramas: {e}")
        print("Erro ao gerar histogramas.")
def aplicar_filtro_interativo(df):
    # pergunta pro usuário se ele quer filtrar alguma coluna
    col = input("\nDigite o nome da coluna para filtrar (ou ENTER para pular): ").strip()

    # se a coluna existir, pede o valor e aplica o filtro
    if col and col in df.columns:
        val = input(f"Digite o valor para filtrar na coluna '{col}': ").strip()
        df_filtrado = df[df[col].astype(str) == val]

        # mostra o resultado do filtro
        print(f"\n=== Linhas filtradas onde {col} == '{val}' ===")
        print(df_filtrado)
    else:
        print("Nenhum filtro aplicado.")


def main():
    # carrega variáveis do .env se existirem
    load_dotenv()

    if len(sys.argv) < 3:
        print("Uso: python minio_loader.py <bucket> <caminho_arquivo>")
        sys.exit(1)

    bucket = sys.argv[1]
    path = sys.argv[2]

    try:
        # carrega o dataset
        df = load_dataset(bucket, path)

        # analises basicas
        mostrar_info_basica(df)

        # verifica dados ausentes, valores unicos
        verificar_qualidade_dados(df)

        # calcula a correlacao entre colunas numericas
        calcular_correlacao(df)

        # gera graficos de distribuicao (histogramas)
        gerar_histogramas(df)

        # permite aplicar um filtro interativo no terminal
        aplicar_filtro_interativo(df)

    except Exception as e:
        print(f"Erro: {e}")


# aqui é onde o script começa de verdade quando você roda: python minio_loader.py ...
if __name__ == "__main__":
    main()