# Guia do Pesquisador: Acessando o Data Lake Local

Bem-vindo ao Data Lake local! Este guia irá ajudá-lo a configurar seu ambiente, conectar-se ao sistema MinIO e utilizar os scripts fornecidos para interagir com os dados de forma simples e eficiente.

---

## Sumário do Conteúdo

1. [Introdução](#1-introdução)  
2. [Pré-requisitos](#2-pré-requisitos)  
3. [Configuração Inicial](#3-configuração-inicial)  
4. [Acessando o Data Lake](#4-acessando-o-data-lake)  
    - [Via Interface Web (MinIO Console)](#acesso-via-interface-web-minio-console)  
    - [Via Terminal (Scripts Python)](#acesso-via-terminal-scripts-python)  
5. [Utilizando os Scripts do Data Lake](#5-utilizando-os-scripts-do-data-lake)  
6. [Suporte e Dúvidas](#6-suporte-e-dúvidas)  

---

## **1. Introdução**

Nosso Data Lake local é um repositório centralizado para armazenar, processar e analisar dados de pesquisa. Ele é construído com o **MinIO**, um sistema de armazenamento de objetos compatível com Amazon S3.

Este guia detalha como você pode:

- se conectar ao Data Lake;
- carregar seus dados;
- explorar e baixar datasets;
- usar a interface web e scripts Python.

---

## **2. Pré-requisitos**

Certifique-se de que sua máquina tenha os seguintes softwares:

- **Python 3.x** (recomendado 3.8+):  
  [Instalação do Python](https://www.python.org/downloads/)

- **pip:** O gerenciador de pacotes do Python (geralmente já vem com o Python).

- **Git:** Caso você vá clonar o projeto do GitHub.  
  [Instalação do Git](https://git-scm.com/downloads)

---

## **3. Configuração Inicial**

1. **Clone o Projeto:**

```bash
git clone git@github.com:gabrielazeved1/Iniciacao-Cientifica.git
cd Iniciacao-Cientifica
```

> Caso tenha recebido os arquivos de outra forma, apenas navegue até a pasta raiz do projeto no terminal.

2. **Instale as dependências Python:**

```bash
pip install -r requirements.txt
```

---

## **4. Acessando o Data Lake**

O Data Lake MinIO está hospedado no IP `127.0.0.1:9001`. Você pode acessá-lo por:

### ### **Acesso via Interface Web (MinIO Console)**

1. Acesse pelo navegador:  
   `http://127.0.0.1:9001`

2. Insira suas credenciais fornecidas.

**Ideal para:**
- Uploads/downloads pontuais  
- Navegação visual  
- Usuários não técnicos

---

### **Acesso via Terminal (Scripts Python)**

#### **Por que usar `login_datalake.sh` para login**

Para autenticar os scripts, é necessário configurar variáveis de ambiente. O script `login_datalake.sh` automatiza esse processo de forma segura:

```bash
source researchers_scripts/login_datalake.sh SEU_USUARIO SUA_SENHA
```

Isso define:

```bash
export MINIO_ACCESS_KEY="SEU_USUARIO"
export MINIO_SECRET_KEY="SUA_SENHA"
```

> Essas variáveis duram enquanto o terminal estiver aberto.

**Ideal para:**
- Automação de uploads/downloads  
- Integração com scripts de análise (ex: Pandas)  
- Usuários com conhecimento básico de terminal

---

## **5. Utilizando os Scripts do Data Lake**

Execute sempre da raiz do projeto. Todos os scripts estão em `researchers_scripts/`.

### ** Listar buckets e conteúdo: `list_datalake.py`**

```bash
# Lista todos os buckets
python researchers_scripts/list_datalake.py

# Lista conteúdo da raiz de um bucket
python researchers_scripts/list_datalake.py datalake

# Lista conteúdo de uma pasta dentro de um bucket
python researchers_scripts/list_datalake.py datalake Comfaulda/

# Lista conteúdo recursivo de uma pasta
python researchers_scripts/list_datalake.py datalake Comfaulda/ --recursive
```

---
### **Análise de Dados Interativa com Pandas (Estilo Kaggle): `minio_loader.py`**

Este é o script mais completo para análise de dados. Ele não apenas lê arquivos CSV do Data Lake diretamente para a memória RAM, sem ocupar espaço no disco, mas também te coloca em um **ambiente interativo** para trabalhar com os dados.

O script executa uma série de análises iniciais (estatísticas, qualidade dos dados e gráficos) e, em seguida, inicia um terminal Python ao vivo (IPython). Nele, você pode usar **qualquer comando do Pandas** na variável `df` para explorar os dados.

```bash
# Ler de uma subpasta específica
python researchers_scripts/minio_loader.py datalake pasta1/pasta2/arquivo.csv

# Para iniciar a análise interativa com o arquivo de vendas
python researchers_scripts/minio_loader.py datalake data/analise_vendas.csv

# Para iniciar a análise interativa com um arquivo da sua pasta 'Comfaulda'
python researchers_scripts/minio_loader.py datalake "Comfaulda/Combined Faults/Unbalance_Horizontal_misalignment/Unbalance_30_g+Hor. Misalignment_0.5_mm/12.97.csv"
```
O script irá pausar em um prompt interativo do IPython (`In [1]:`). A partir daí, a variável `df` com o seu DataFrame estará disponível, e você pode rodar os comandos abaixo:

#### **Exemplos de Interação com o DataFrame:**

```python
# Python
# Ver as primeiras linhas do DataFrame
In [1]: df.head()

# Calcular a média da coluna 'Vendas'
In [2]: df['Vendas'].mean()

# Filtrar os dados por uma condição
In [3]: df_filtrado = df.loc[df['Regiao'] == 'Sudeste']

# Obter um resumo estatístico das colunas
In [4]: df.describe()
```

### **Upload de Arquivos**

```bash
# Enviar um único arquivo
python researchers_scripts/upload_file.py datalake data/meu_arquivo.csv
```

```bash
# Enviar um diretório completo
python researchers_scripts/upload_directory.py datalake data/Comfaulda Comfaulda_nome_novo.
```

---

### **Download de Arquivos**

```bash
# Baixar da raiz do bucket
python researchers_scripts/download_file.py datalake nome_arquivo.csv

# Baixar de uma subpasta
python researchers_scripts/download_file.py datalake pasta1/pasta2/nome_arquivo.csv
```

---

### **Ler Dataset com Pandas**

```bash
# Ler diretamente do bucket para um DataFrame
python researchers_scripts/read_file.py datalake nome_arquivo.csv

# Ler de uma subpasta específica
python researchers_scripts/read_dataset.py datalake pasta1/pasta2/arquivo.csv
```

---

## **6. Suporte e Dúvidas**

Caso encontre problemas, entre em contato com:

**Administrador do Data Lake**  
Gabriel Azevedo  

---

*Todas as operações feitas por scripts são registradas automaticamente na pasta `logs/` do projeto para facilitar o diagnóstico de erros.*
