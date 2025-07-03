# Guia do Pesquisador: Acessando o Data Lake Local

Bem-vindo ao Data Lake local do nosso laboratório! Este guia irá ajudá-lo a configurar seu ambiente e utilizar as ferramentas fornecidas para interagir com o Data Lake MinIO, que é o nosso sistema de armazenamento de dados.

-----

## Sumário do Conteúdo

1.  Introdução
2.  Pré-requisitos
3.  Configuração Inicial
4.  Acessando o Data Lake
      Via Terminal (Scripts Python)
      Via Interface Web (MinIO Console)
5.  Utilizando os Scripts do Data Lake
      Listar Buckets
      Listar Conteúdo de um Bucket/Pasta
      Upload de um Arquivo
      Upload de um Diretório Completo
      Download de um Arquivo
      Ler Dataset com Pandas
6.  Suporte e Dúvidas

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
  [Instalação do Git]

### **3. Configuração Inicial**

1.  **Obtenha o Código do Projeto:**

```bash
git clone git@github.com:gabrielazeved1/Iniciacao-Cientifica.git
cd Iniciacao-Cientifica
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
python researchers_scripts/upload_file.py datalake data/meu_arquivo.csv
python researchers_scripts/upload_file.py datalake pasta/nome_arquivo
```

```bash
#Upload de um Diretório Completo
python researchers_scripts/upload_directory.py datalake data/Comfaulda Comfaulda
python researchers_scripts/upload_directory.py datalake data/dataset dataset 
```

#### **Download de um Arquivo**

```bash
# Baixar da raiz do bucket
python researchers_scripts/download_file.py datalake nome_arquivo.tipo

# Baixar da pasta 'projeto_X'
python researchers_scripts/download_file.py datalake subpasta1/subpasta2/nome_arquivo.tipo
```

#### **Ler Dataset com Pandas**

```bash
# Ler CSV da raiz do bucket
python researchers_scripts/read_file.py datalake nome_arquivo.tipo

# Ler CSV em subpasta
python researchers_scripts/read_dataset.py datalake subpasta01/subpasta02/arquivo.tipo
```

### **6. Suporte e Dúvidas**

Se você tiver qualquer dúvida, encontrar algum erro ou precisar de ajuda com as credenciais, entre em contato com:

**Administrador do Data Lake:**  
📧 Gabriel Azevedo

-----

📝 *Todas as operações feitas por scripts são registradas automaticamente na pasta `logs/` do projeto. Isso ajuda a diagnosticar qualquer problema.*

