# Projeto: Data Lake Local para Pesquisa com MinIO

Este projeto estabelece um ambiente de Data Lake local utilizando o MinIO, um armazenamento de objetos compatível com a API S3. Ele é projetado para oferecer aos pesquisadores um acesso estruturado e controlado aos dados, permitindo operações como upload, download, listagem e leitura direta de datasets, além de um sistema de backup interno para garantir a segurança dos dados.

## Sumário do Conteúdo

1.  [Recursos Principais](#1-recursos-principais)
2.  [Pré-requisitos](#2-pré-requisitos)
3.  [Estrutura do Projeto](#3-estrutura-do-projeto)
4.  [Configuração Inicial do Ambiente](#4-configuração-inicial-do-ambiente)
    * [Iniciar o MinIO](#iniciar-o-minio)
    * [Instalar Dependências Python](#instalar-dependências-python)
    * [Configurar MinIO Client (mc)](#configurar-minio-client-mc)
    * [Inicializar o Data Lake](#inicializar-o-data-lake)
5.  [Uso para o Administrador do Data Lake](#5-uso-para-o-administrador-do-data-lake)
    * [Logs de Administração](#logs-de-administração)
    * [Sistema de Backup Interno](#sistema-de-backup-interno)
6.  [Uso para Pesquisadores](#6-uso-para-pesquisadores)
    * [Configurar Credenciais](#configurar-credenciais)
    * [Scripts de Pesquisadores](#scripts-de-pesquisadores)
7.  [Logs do Sistema](#7-logs-do-sistema)
8.  [Considerações Finais e Próximos Passos](#8-considerações-finais-e-próximos-passos)
9.  [Solução de Problemas Comuns](#9-solução-de-problemas-comuns)

---

### **1. Recursos Principais**

* **MinIO Local:** Servidor de armazenamento de objetos compatível com S3 rodando via Docker Compose.
* **Estrutura de Data Lake:** Buckets essenciais (`datalake`, `backup`) criados automaticamente.
* **Scripts para Pesquisadores:** Ferramentas Python para interagir com o MinIO (upload, download, listagem, leitura).
* **Controle de Acesso (Simplificado):** Utilização de um único conjunto de credenciais para acesso total (para este protótipo).
* **Sistema de Logging:** Registro detalhado de todas as operações em arquivos de log dedicados.
* **Sistema de Backup Interno:** Solução automatizada para backup dos dados do MinIO para o armazenamento local do servidor.

### **2. Pré-requisitos**

Certifique-se de ter os seguintes softwares instalados em seu ambiente (no seu Mac para o protótipo, e no servidor de laboratório para produção):

* **Docker:** Para rodar o MinIO.
    * [Instalação do Docker Desktop](https://docs.docker.com/desktop/)
* **Docker Compose:** Para orquestrar os serviços Docker.
    * Geralmente vem com o Docker Desktop.
* **Python 3.x:** Linguagem de programação para os scripts.
    * [Instalação do Python](https://www.python.org/downloads/)
* **pip:** Gerenciador de pacotes Python (geralmente vem com o Python).
* **MinIO Client (mc):** Ferramenta de linha de comando para interagir com o MinIO e gerenciar políticas.
    * **No Mac (via Homebrew):** `brew install minio/stable/mc`
    * [Outras plataformas](https://min.io/docs/minio/linux/reference/minio-client/mc.html#install-minio-client)

### **3. Estrutura do Projeto**
├── .git/                     # Controle de versão
├── data/                     # Opcional: Pasta para seus dados locais (entrada/saída de scripts)
│   ├── Comfaulda/            # Exemplo de pasta de dataset
│   ├── ensaio_componetes_mecanicos/
│   └── stock_market_data/
├── docs/                     # Documentação (opcional)
├── logs/                     # Diretório para todos os arquivos de log gerados
├── minio_configs/            # Armazena arquivos de configuração do MinIO (como políticas JSON)
│   ├── download_policy.json
│   └── upload_policy.json
├── researchers_scripts/      # Scripts para uso dos pesquisadores
│   ├── download_dataset.py
│   ├── list_bucket_contents.py
│   ├── list_buckets.py
│   ├── read_dataset.py
│   ├── upload_dataset.py
│   └── upload_directory.py   # Script para upload de diretórios inteiros
├── src/                      # Código fonte principal da aplicação
│   ├── init.py
│   ├── backup_datalake.py    # Script para o sistema de backup interno
│   ├── logger.py             # Configuração centralizada de logging
│   ├── main.py               # Script de inicialização e verificação do Data Lake
│   └── minio_client.py       # Cliente Python para interação com MinIO
├── .env                      # Variáveis de ambiente (opcional, para credenciais ou configs)
├── comando.txt               # Anotações de comandos (opcional)
├── docker-compose.yml        # Configuração do MinIO via Docker Compose
├── README.md                 # Este arquivo
└── requirements.txt          # Dependências Python do projeto

### **4. Configuração Inicial do Ambiente**

Siga estas etapas para configurar e iniciar seu Data Lake local.

#### **Iniciar o MinIO**

1.  Navegue até a raiz do seu projeto no terminal (onde está o `docker-compose.yml`).
2.  Inicie o servidor MinIO usando Docker Compose:
    ```bash
    docker-compose up -d
    ```
    *Isso iniciará o MinIO em background. A porta da API será `9000` e a UI (interface web) será `9001`.*
3.  Acesse o painel web do MinIO no seu navegador: `http://localhost:9001`
    * **Usuário Raiz:** `minio`
    * **Senha Raiz:** `miniol23`

#### **Instalar Dependências Python**

1.  Certifique-se de estar na raiz do seu projeto.
2.  Instale as bibliotecas Python necessárias usando `pip`:
    ```bash
    pip install -r requirements.txt
    ```

#### **Configurar MinIO Client (mc)**

Configure um alias para seu servidor MinIO local, o que facilita o uso do `mc` para comandos administrativos:

```bash
mc alias set localminio http://localhost:9000 minio miniol23
```

### **Inicializar o Data Lake**

Este script verificará a conexão com o MinIO e criará os buckets essenciais (`datalake`, `backup`) se eles ainda não existirem.

1.  Certifique-se de que o MinIO esteja rodando (`docker-compose ps` deve mostrar `minio-server` como `Up`).
2.  Execute o script de inicialização:
    ```bash
    python src/main.py
    ```
    *Você verá mensagens no terminal e em `logs/datalake_admin.log` confirmando a conexão e a criação (ou verificação) dos buckets.*

### **5. Uso para o Administrador do Data Lake**

Como administrador do Data Lake, você é responsável pela infraestrutura e pelos backups.

#### **Logs de Administração**

* Todos os logs relacionados à inicialização e manutenção da infraestrutura do MinIO (execução de `src/main.py`) são registrados em:
    `logs/datalake_admin.log`

#### **Sistema de Backup Interno**

O projeto inclui um script Python (`src/backup_datalake.py`) que utiliza o `mc mirror` para criar cópias de segurança dos seus buckets MinIO em um diretório local no servidor.

* **Destino do Backup:**
    Os backups serão armazenados em: `/Users/gabrielazevedo/minio_backups/daily/` (para o protótipo no Mac) ou em `/srv/backups/minio_datalake/daily/` (para o servidor de laboratório). Dentro deste diretório, os backups são organizados por `YYYYMMDD_HHMMSS` (ano/mês/dia_hora/minuto/segundo).

* **Executando o Backup Manualmente (para Teste/Demo):**
    ```bash
    python src/backup_datalake.py
    ```
    *Isso criará uma nova pasta de backup com timestamp no diretório de destino configurado.*
    *Os logs de backup serão registrados em: `logs/datalake_backup.log`.*

* **Configuração de Automação (Cron Job - Linux/macOS):**
    Para automatizar o backup (ex: diariamente à 1h da manhã no servidor de laboratório), você usaria um `cron job`.
    1.  Abra seu crontab: `crontab -e`
    2.  Adicione a linha (ajuste o caminho completo para o script):
        ```bash
        0 1 * * * /usr/bin/python3 /caminho/completo/para/seu/projeto/src/backup_datalake.py >> /var/log/minio_backup_cron.log 2>&1
        ```

* **Estratégia de Restauração (CUIDADO!):**
    A restauração envolve copiar dados de volta do backup local para o MinIO.
    **Sempre teste a restauração em um bucket de teste primeiro!**
    * **Restaurar um bucket inteiro (CUIDADO - SOBRESCREVE TODO O CONTEÚDO DO BUCKET!):**
        ```bash
        mc mirror --overwrite /Users/gabrielazevedo/minio_backups/daily/YYYYMMDD_HHMMSS/datalake localminio/datalake
        ```
        *(Substitua `YYYYMMDD_HHMMSS` pelo timestamp do backup desejado.)*
    * **Restaurar um arquivo específico:**
        ```bash
        mc cp /Users/gabrielazevedo/minio_backups/daily/YYYYMMDD_HHMMSS/datalake/sua_pasta/arquivo.csv localminio/datalake/sua_pasta/arquivo.csv
        ```

### **6. Uso para Pesquisadores**

Os pesquisadores usarão os scripts na pasta `researchers_scripts/` para interagir com o Data Lake.

#### **Configurar Credenciais**

Para este protótipo, os pesquisadores usarão as credenciais de administrador do MinIO (`minio`/`miniol23`) que possuem acesso total aos buckets. Eles precisarão definir essas credenciais como variáveis de ambiente em seu terminal **antes de executar qualquer script**:

```bash
export MINIO_ACCESS_KEY="minio"
export MINIO_SECRET_KEY="miniol23"

# Scripts de Pesquisadores

Todos os scripts devem ser executados a partir da raiz do projeto:  
**`~/projects/src/IC/`** no seu Mac ou o diretório raiz do projeto no servidor.

---

## 📤 `upload_dataset.py` — Upload de um Arquivo

Envia um arquivo local para um bucket, com a opção de especificar uma subpasta.

```bash
# Upload de um arquivo para a raiz do bucket 'datalake'
python researchers_scripts/upload_dataset.py datalake data/meu_arquivo.csv

# Upload de um arquivo para a pasta 'Comfaulda' dentro do bucket 'datalake'
python researchers_scripts/upload_dataset.py datalake data/meu_arquivo.csv Comfaulda
```

---

## 📁 `upload_directory.py` — Upload de um Diretório Completo

Envia todos os arquivos de um diretório local (mantendo a estrutura de subpastas) para um bucket.

```bash
# Upload da pasta 'data/Comfaulda' para o bucket 'datalake' sob o prefixo 'Comfaulda/'
python researchers_scripts/upload_directory.py datalake data/Comfaulda Comfaulda

# Upload da pasta 'data/stock_market_data' para 'datalake/financeiro/'
python researchers_scripts/upload_directory.py datalake data/stock_market_data financeiro
```

---

## 📥 `download_dataset.py` — Download de um Arquivo

Baixa um arquivo do MinIO para a pasta **Downloads** do usuário.

```bash
# Baixar 'meu_arquivo.csv' da raiz do bucket 'datalake'
python researchers_scripts/download_dataset.py datalake meu_arquivo.csv

# Baixar 'documento.pdf' da pasta 'relatorios' no bucket 'datalake'
python researchers_scripts/download_dataset.py datalake relatorios/documento.pdf
```

---

## 📦 `list_buckets.py` — Listar Buckets

Lista todos os buckets disponíveis no MinIO.

```bash
python researchers_scripts/list_buckets.py
```

---

## 📂 `list_bucket_contents.py` — Listar Conteúdo de um Bucket/Pasta

Lista os objetos e subpastas dentro de um bucket ou de um prefixo específico.

```bash
# Listar todo o conteúdo do bucket 'datalake'
python researchers_scripts/list_bucket_contents.py datalake

# Listar o conteúdo da pasta 'Comfaulda' dentro do bucket 'datalake'
python researchers_scripts/list_bucket_contents.py datalake Comfaulda/
```

---

## 📊 `read_dataset.py` — Ler Dataset com Pandas

Lê diretamente um arquivo CSV do MinIO para um DataFrame do Pandas.  
Útil para análise imediata sem necessidade de download.

```bash
# Ler 'dados_vendas.csv' da raiz do bucket 'datalake'
python researchers_scripts/read_dataset.py datalake dados_vendas.csv

# Ler 'relatorio_mensal.csv' da pasta 'analises/2025' no bucket 'datalake'
python researchers_scripts/read_dataset.py datalake analises/2025/relatorio_mensal.csv
```

---

## 📝 Logs do Sistema

Todos os logs detalhados das operações são salvos na pasta `logs/`:

| Caminho do Log                                 | Descrição                                                  |
|------------------------------------------------|------------------------------------------------------------|
| `logs/datalake_admin.log`                      | Logs da inicialização do Data Lake (`src/main.py`)         |
| `logs/datalake_backup.log`                     | Logs do script de backup (`src/backup_datalake.py`)        |
| `logs/pesquisadores_download.log`              | Logs de downloads de arquivos pelos pesquisadores          |
| `logs/pesquisadores_upload.log`                | Logs de uploads de arquivos pelos pesquisadores            |
| `logs/pesquisadores_upload_diretorio.log`      | Logs de uploads de diretórios pelos pesquisadores          |
| `logs/pesquisadores_list_buckets.log`          | Logs da listagem de buckets                                |
| `logs/pesquisadores_list_contents.log`         | Logs da listagem de conteúdo de buckets                    |
| `logs/pesquisadores_read_dataset.log`          | Logs das leituras de datasets com Pandas                   |

---

> Para dúvidas ou contribuições, entre em contato com a equipe de desenvolvimento do projeto.

