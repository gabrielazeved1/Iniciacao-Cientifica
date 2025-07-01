# Guia do Pesquisador: Acessando o Data Lake Local

Bem-vindo ao Data Lake local do nosso laboratório! Este guia irá ajudá-lo a configurar seu ambiente e utilizar as ferramentas fornecidas para interagir com o Data Lake MinIO, que é o nosso sistema de armazenamento de dados.

-----

## Sumário do Conteúdo

1.  [Introdução]
2.  [Pré-requisitos]
3.  [Configuração Inicial]
4.  [Acessando o Data Lake](https://www.google.com/search?q=%234-acessando-o-data-lake)
      * [Via Terminal (Scripts Python)](https://www.google.com/search?q=%23via-terminal-scripts-python)
      * [Via Interface Web (MinIO Console)](https://www.google.com/search?q=%23via-interface-web-minio-console)
5.  [Utilizando os Scripts do Data Lake](https://www.google.com/search?q=%235-utilizando-os-scripts-do-data-lake)
      * [Listar Buckets](https://www.google.com/search?q=%23listar-buckets)
      * [Listar Conteúdo de um Bucket/Pasta](https://www.google.com/search?q=%23listar-conte%C3%BAdo-de-um-bucketpasta)
      * [Upload de um Arquivo](https://www.google.com/search?q=%23upload-de-um-arquivo)
      * [Upload de um Diretório Completo](https://www.google.com/search?q=%23upload-de-um-diret%C3%B3rio-completo)
      * [Download de um Arquivo](https://www.google.com/search?q=%23download-de-um-arquivo)
      * [Ler Dataset com Pandas](https://www.google.com/search?q=%23ler-dataset-com-pandas)
6.  [Suporte e Dúvidas](https://www.google.com/search?q=%236-suporte-e-d%C3%BAvidas)

-----

### **1. Introdução**

Nosso Data Lake local é um repositório centralizado para armazenar, processar e analisar dados de pesquisa. Ele é construído com o MinIO, que oferece uma interface de armazenamento de objetos compatível com Amazon S3.

Este guia detalha como você pode se conectar, carregar seus dados, baixar datasets existentes e explorar o conteúdo do Data Lake usando scripts Python e a interface web.

### **2. Pré-requisitos**

Para começar, certifique-se de que sua máquina tenha os seguintes softwares instalados:

* **Python 3.x:** (Recomendado versão 3.8 ou superior).  
  [Instalação do Python](https://www.python.org/downloads/)

* **pip:** O gerenciador de pacotes do Python (geralmente vem com o Python).

* **Git:** Se você clonar o projeto do GitHub.  
  [Instalação do Git](https://git-scm.com/downloads)

### **3. Configuração Inicial**

1.  **Obtenha o Código do Projeto:**

```bash
git clone <URL_DO_REPOSITORIO_DO_PROJETO>
cd <nome_da_pasta_do_projeto>
```

> Se você recebeu os arquivos de outra forma, apenas navegue até a pasta raiz do projeto no terminal.

2.  **Instale as Dependências Python:**

```bash
pip install -r requirements.txt
```

### **4. Acessando o Data Lake**

O Data Lake MinIO está rodando no servidor de laboratório (IP: `192.168.18.31`). Você pode acessá-lo de duas maneiras principais: via scripts Python no terminal ou diretamente pela interface web.

#### **Via Terminal (Scripts Python)**

1.  **Defina Suas Credenciais:**

```bash
export MINIO_ACCESS_KEY="SEU_USUARIO"
export MINIO_SECRET_KEY="SUA_SENHA"
```

> Substitua `SEU_USUARIO` e `SUA_SENHA` pelas credenciais fornecidas (ex: `amanda`/`amanda123`, `marcio`/`marcio123`).

⚠️ Essas variáveis só duram durante a sessão do terminal. Fechou o terminal? Rode novamente os comandos acima.

2.  **Localização dos Scripts:**

Todos os scripts estão em `researchers_scripts/`.  
**Execute sempre a partir da raiz do projeto.**

#### **Via Interface Web (MinIO Console)**

1.  Abra o navegador e acesse:  
    `http://192.168.18.31:9001`

2.  Faça login com suas credenciais (`SEU_USUARIO` e `SUA_SENHA`).

### **5. Utilizando os Scripts do Data Lake**

#### **Listar Buckets**

```bash
python researchers_scripts/list_buckets.py
```

#### **Listar Conteúdo de um Bucket/Pasta**

```bash
# Lista tudo dentro do bucket 'datalake'
python researchers_scripts/list_bucket_contents.py datalake

# Lista a pasta 'Comfaulda' dentro do bucket 'datalake'
python researchers_scripts/list_bucket_contents.py datalake Comfaulda/
```

#### **Upload de um Arquivo**

```bash
# Envia para raiz do bucket
python researchers_scripts/upload_dataset.py datalake data/meu_relatorio.pdf

# Envia para subpasta
python researchers_scripts/upload_dataset.py datalake data/dados_coletados.csv meu_projeto/dados_brutos
```

#### **Upload de um Diretório Completo**

```bash
# Upload completo da pasta com nome igual ao diretório
python researchers_scripts/upload_directory.py datalake data/meus_dados_coletados

# Upload para subpasta específica
python researchers_scripts/upload_directory.py datalake data/resultados_finais analises/2024
```

#### **Download de um Arquivo**

```bash
# Baixar da raiz do bucket
python researchers_scripts/download_dataset.py datalake analise_final.xlsx

# Baixar da pasta 'projeto_X'
python researchers_scripts/download_dataset.py datalake projeto_X/imagens/grafico_A.png
```

#### **Ler Dataset com Pandas**

```bash
# Ler CSV da raiz do bucket
python researchers_scripts/read_dataset.py datalake dados_experimento.csv

# Ler CSV em subpasta
python researchers_scripts/read_dataset.py datalake projeto_Y/resultados_modelo/teste_1.csv
```

### **6. Suporte e Dúvidas**

Se você tiver qualquer dúvida, encontrar algum erro ou precisar de ajuda com as credenciais, entre em contato com:

**Administrador do Data Lake:**  
📧 Gabriel Azevedo

-----

📝 *Todas as operações feitas por scripts são registradas automaticamente na pasta `logs/` do projeto. Isso ajuda a diagnosticar qualquer problema.*

