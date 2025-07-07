# Projeto: Data Lake Local para Pesquisa com MinIO

Este projeto estabelece um ambiente de Data Lake local utilizando o MinIO — um armazenamento de objetos compatível com a API S3. Ele fornece aos pesquisadores e ao administrador um acesso estruturado e seguro aos dados, com suporte a operações como upload, download, leitura direta e backup automatizado.

---

## Sumário do Conteúdo

1. [Recursos Principais](#1-recursos-principais)  
2. [Pré-requisitos](#2-pré-requisitos)  
3. [Estrutura do Projeto](#3-estrutura-do-projeto)  
4. [Configuração Inicial do Ambiente](#4-configuração-inicial-do-ambiente)  
5. [Uso para Administradores](#5-uso-para-administradores)  
6. [Uso para Pesquisadores](#6-uso-para-pesquisadores)  
7. [Logs do Sistema](#7-logs-do-sistema)  
8. [Considerações Finais e Melhorias Futuras](#8-considerações-finais-e-melhorias-futuras)  
9. [Solução de Problemas Comuns](#9-solução-de-problemas-comuns)

---

## 1. Recursos Principais

- MinIO via Docker Compose  
- Buckets essenciais pré-configurados: `datalake` e `backup`  
- Scripts Python para pesquisadores: upload, download, leitura e listagem  
- Autenticação simplificada por variáveis de ambiente  
- Sistema completo de logging  
- Backup automático com restauração fácil  

---

## 2. Pré-requisitos

### Para todos os usuários

- Python 3.x  
- pip (gerenciador de pacotes do Python)  

### Adicional para administradores

- Docker e Docker Compose  
- MinIO Client (mc)

Instalação no macOS (via Homebrew):

```bash
brew install minio/stable/mc
```

---

## 3. Estrutura do Projeto

```
├── data/                       # Dados locais (entrada/saída)
│   └── Comfaulda/, ensaios/, etc.
├── docs/                       # Documentação 
├── logs/                       # Arquivos de log (gerados automaticamente)
├── researchers_scripts/        # Scripts de uso dos pesquisadores
│   ├── upload_file.py
│   ├── upload_directory.py
│   ├── download_file.py
│   ├── read_file.py
│   ├── read_dataset.py
│   └── list_datalake.py
├── src/                        # Scripts administrativos
│   ├── main.py                 # Inicialização do Data Lake
│   ├── backup_datalake.py      # Sistema de backup
│   ├── logger.py
│   └── minio_client.py         # Wrapper Python para MinIO
├── docker-compose.yml          # Serviço do MinIO
├── requirements.txt            # Dependências Python
└── README.md                   # Este arquivo
```

---

## 4. Configuração Inicial do Ambiente

### 4.1 Iniciar o MinIO

```bash
docker-compose up -d
```

Acesse a interface Web: [http://localhost:9001](http://localhost:9001)  
Credenciais padrão:
- Usuário: `minio`
- Senha: `miniol23`

---

### 4.2 Instalar Dependências Python

```bash
pip install -r requirements.txt
```

---

### 4.3 Configurar MinIO Client (mc)

```bash
mc alias set localminio http://localhost:9000 minio miniol23
```

---

### 4.4 Inicializar o Data Lake

```bash
python src/main.py
```

Isso criará os buckets principais e configurações iniciais.

---

## 5. Uso para Administradores

### 5.1 Executar Backup Manualmente

```bash
python src/backup_datalake.py
```

---

### 5.2 Restaurar Backup

```bash
# Restaurar bucket completo
mc mirror --overwrite /caminho/do/backup/YYYYMMDD_HHMMSS/datalake localminio/datalake

# Restaurar arquivo específico
mc cp /caminho/do/backup/YYYYMMDD_HHMMSS/datalake/pasta/arquivo.csv localminio/datalake/pasta/arquivo.csv
```

---

## 6. Uso para Pesquisadores

### 6.1 Autenticação

Autenticar manualmente:

```bash
export MINIO_ACCESS_KEY="minio"
export MINIO_SECRET_KEY="miniol23"
```

Ou utilize o script de login:

```bash
source researchers_scripts/login_datalake.sh SEU_USUARIO SUA_SENHA
```

---

### 6.2 Scripts Disponíveis

Execute sempre da raiz do projeto.

#### Listar Buckets e Conteúdo: `list_datalake.py`

```bash
# Listar buckets
python researchers_scripts/list_datalake.py

# Listar conteúdo de um bucket
python researchers_scripts/list_datalake.py datalake

# Listar conteúdo de uma pasta
python researchers_scripts/list_datalake.py datalake Comfaulda/

# Listar recursivamente
python researchers_scripts/list_datalake.py datalake Comfaulda/ --recursive
```

---

#### Uploads

```bash
# Upload de arquivo
python researchers_scripts/upload_file.py datalake data/arquivo.csv

# Upload com destino específico
python researchers_scripts/upload_file.py datalake data/arquivo.csv Comfaulda

# Upload de diretório
python researchers_scripts/upload_directory.py datalake data/Comfaulda Comfaulda
```

---

#### Downloads

```bash
# Baixar arquivo da raiz
python researchers_scripts/download_file.py datalake meu_arquivo.csv

# Baixar arquivo de subpasta
python researchers_scripts/download_file.py datalake relatorios/2025/analise_final.csv
```

---

#### Leitura com Pandas

```bash
# Ler CSV da raiz
python researchers_scripts/read_file.py datalake arquivo.csv

# Ler CSV de subpasta
python researchers_scripts/read_dataset.py datalake relatorios/2025/analise.csv
```

---

## 7. Logs do Sistema

| Caminho                                     | Descrição                                        |
|--------------------------------------------|--------------------------------------------------|
| `logs/datalake_admin.log`                  | Inicialização do Data Lake (`src/main.py`)       |
| `logs/datalake_backup.log`                 | Backup automatizado (`backup_datalake.py`)       |
| `logs/pesquisadores_upload.log`            | Uploads de arquivos                              |
| `logs/pesquisadores_upload_diretorio.log`  | Uploads de diretórios                            |
| `logs/pesquisadores_download.log`          | Downloads realizados                             |
| `logs/pesquisadores_list_datalake.log`     | Listagens de buckets e conteúdos (`list_datalake.py`) |
| `logs/pesquisadores_read_dataset.log`      | Leitura de arquivos com Pandas                   |

---

## 8. Solução de Problemas Comuns

**Erro de autenticação no MinIO**  
Verifique se as variáveis de ambiente estão definidas corretamente.

**Bucket não encontrado**  
Execute `python src/main.py` para inicializar os buckets.

**Porta em uso ao iniciar o Docker**  
Altere as portas no `docker-compose.yml` ou pare o processo que está ocupando a porta.
