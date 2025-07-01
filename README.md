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
```
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
```

### **4. Configuração Inicial do Ambiente**

#### **Iniciar o MinIO**

```bash
# Navegue até a raiz do seu projeto
docker-compose up -d
```

Acesse o painel web: [http://localhost:9001](http://localhost:9001)  
Credenciais padrão:
- Usuário: `minio`
- Senha: `miniol23`

#### **Instalar Dependências Python**

```bash
pip install -r requirements.txt
```

#### **Configurar MinIO Client (mc)**

```bash
mc alias set localminio http://localhost:9000 minio miniol23
```

#### **Inicializar o Data Lake**

```bash
python src/main.py
```

---

### **5. Uso para o Administrador do Data Lake**

#### **Logs de Administração**

- `logs/datalake_admin.log`

#### **Sistema de Backup Interno**

Executar manualmente:

```bash
python src/backup_datalake.py
```

Automatizar via cron:

```bash
0 1 * * * /usr/bin/python3 /caminho/do/projeto/src/backup_datalake.py >> /var/log/minio_backup_cron.log 2>&1
```

Restaurar dados (⚠️ cuidado):

```bash
# Restaurar bucket inteiro
mc mirror --overwrite /caminho/do/backup/YYYYMMDD_HHMMSS/datalake localminio/datalake

# Restaurar arquivo específico
mc cp /caminho/do/backup/YYYYMMDD_HHMMSS/datalake/pasta/arquivo.csv localminio/datalake/pasta/arquivo.csv
```

---

### **6. Uso para Pesquisadores**

#### **Configurar Credenciais**

```bash
export MINIO_ACCESS_KEY="minio"
export MINIO_SECRET_KEY="miniol23"
```

---

### **Scripts de Pesquisadores**

Todos os scripts devem ser executados a partir da raiz do projeto (`~/projects/src/IC/`).

#### 📤 `upload_dataset.py`

```bash
python researchers_scripts/upload_dataset.py datalake data/meu_arquivo.csv
python researchers_scripts/upload_dataset.py datalake data/meu_arquivo.csv Comfaulda
```

#### 📁 `upload_directory.py`

```bash
python researchers_scripts/upload_directory.py datalake data/Comfaulda Comfaulda
python researchers_scripts/upload_directory.py datalake data/stock_market_data financeiro
```

#### 📥 `download_dataset.py`

```bash
python researchers_scripts/download_dataset.py datalake meu_arquivo.csv
python researchers_scripts/download_dataset.py datalake relatorios/documento.pdf
```

#### 📦 `list_buckets.py`

```bash
python researchers_scripts/list_buckets.py
```

#### 📂 `list_bucket_contents.py`

```bash
python researchers_scripts/list_bucket_contents.py datalake
python researchers_scripts/list_bucket_contents.py datalake Comfaulda/
```

#### 📊 `read_dataset.py`

```bash
python researchers_scripts/read_dataset.py datalake dados_vendas.csv
python researchers_scripts/read_dataset.py datalake analises/2025/relatorio_mensal.csv
```

---

### **7. Logs do Sistema**

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

### **8. Considerações Finais e Próximos Passos**

- Validar os scripts em diferentes sistemas operacionais.
- Automatizar testes de integridade dos dados após backup.
- Implementar controle de acesso mais refinado por políticas.
- Expandir para múltiplos usuários com isolamento de dados.

---

### **9. Solução de Problemas Comuns**

**Problema:** Erro de autenticação no MinIO  
**Solução:** Verifique se as variáveis de ambiente estão exportadas corretamente.

**Problema:** Bucket não encontrado  
**Solução:** Certifique-se de rodar `main.py` para criar os buckets antes do uso.

**Problema:** Porta em uso ao iniciar o Docker  
**Solução:** Altere as portas no `docker-compose.yml` ou pare o processo em uso.

---

> Para dúvidas ou contribuições, entre em contato com a equipe de desenvolvimento do projeto.
