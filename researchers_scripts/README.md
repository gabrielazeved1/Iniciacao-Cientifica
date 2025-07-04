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
# Guia de Acesso ao Data Lake MinIO

Este documento explica as duas principais formas de interagir com o Data Lake MinIO do nosso laboratório: através da interface web visual (MinIO Console) e via linha de comando (terminal) usando scripts Python. Também detalha como configurar seu ambiente para usar os scripts, explicando por que um script shell é essencial para o "login".

---

## 1. Acesso via Interface Web (MinIO Console)

Este modo de acesso permite interagir com o Data Lake de forma visual, usando seu navegador de internet.

* **O que é:** Uma interface gráfica de usuário (GUI) fornecida pelo MinIO para gerenciar seus dados e buckets visualmente.
* **Como Acessar:**
    1.  Abra seu navegador de internet.
    2.  Vá para o endereço: `http://192.168.18.31:9001` (Este é o endereço IP do servidor onde o MinIO está rodando, na porta da interface web).
    3.  Na tela de login, insira suas credenciais (usuário e senha) fornecidas a você.
* **Quando Usar:**
    * Para uma **exploração rápida** do conteúdo dos buckets.
    * Para **uploads ou downloads pontuais** de arquivos, arrastando e soltando.
    * Para **gerenciamento visual** de buckets (se você tiver permissões para isso).
    * Ideal para usuários que preferem uma interface gráfica e não têm conhecimento de linha de comando.
* **Vantagens:** Intuitivo, visual, fácil de usar.
* **Desvantagens:** Não permite automação complexa ou integração direta com fluxos de trabalho de código.

---

## 2. Acesso via Terminal (Scripts Python)

Este modo permite interagir com o Data Lake de forma programática, usando scripts Python na linha de comando.

* **O que é:** Um conjunto de scripts Python (`.py`) localizados na pasta `researchers_scripts/` do projeto, projetados para automatizar e facilitar operações com o MinIO.
* **Como Funciona:** Você executa um comando no terminal que dispara um script Python. Este script usa a biblioteca `minio` (através do `MinioClient`) para se comunicar diretamente com a API do servidor MinIO e realizar tarefas como upload, download, listagem e leitura de dados para análise.
* **Quando Usar:**
    * Para **automação de tarefas repetitivas** (ex: upload de múltiplos arquivos de uma vez).
    * Para **integração com fluxos de trabalho de dados** baseados em código (ex: carregar dados diretamente para um DataFrame do Pandas para análise).
    * Para usuários que preferem controle programático e querem integrar o Data Lake em seus processos de pesquisa e desenvolvimento.
* **Vantagens:** Poderoso, flexível, programável, permite automação, todas as ações são registradas em logs.
* **Desvantagens:** Requer conhecimento básico de linha de comando e Python.

---

## 3. Fazendo o "Login" para os Scripts: Por que `login_datalake.sh` (e não Python)

Para que seus scripts Python possam se conectar ao MinIO, eles precisam de suas credenciais (nome de usuário e senha). A forma mais segura e flexível de fornecer isso é através de **variáveis de ambiente**.

Anteriormente, pedíamos para você usar comandos `export` diretamente no terminal. Agora, temos um script dedicado para isso: `login_datalake.sh`.

* **O Problema (Por que um script Python não serve diretamente para o "login"):**
    * Em sistemas operacionais, quando você executa um script Python (ou qualquer outro programa), ele roda como um "processo filho" do seu terminal (o "processo pai").
    * Um processo filho **não pode alterar as variáveis de ambiente do seu processo pai (o terminal) de forma permanente**. Quando o script Python termina, todas as variáveis que ele definiu internamente "morrem" com ele. Se você tentasse um `export` dentro de um `.py` e depois fechasse o Python, a variável não estaria mais lá para o próximo comando no terminal.

* **Como o Script Shell (`.sh`) Resolve Isso (O Poder do `source`):**
    * Um script shell (`.sh`) é diferente. Quando você o executa com o comando `source` (ex: `source meu_script.sh`), o shell **executa os comandos do script como se você os estivesse digitando diretamente no seu terminal**.
    * Isso significa que qualquer comando `export` dentro do script shell **afeta diretamente o ambiente do seu terminal atual**, e as variáveis de ambiente (`MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`) permanecem definidas até que você feche o terminal ou as altere.

* **Vantagens de Usar `login_datalake.sh`:**
    * **Conveniência:** Um único comando (`source researchers_scripts/login_datalake.sh SEU_USUARIO SUA_SENHA`) em vez de várias linhas `export`.
    * **Padronização:** Garante que as variáveis sejam sempre definidas corretamente.
    * **Extensibilidade:** O administrador pode adicionar mais variáveis (ex: um `MINIO_ENDPOINT` futuro) no script, e você só precisa continuar usando o mesmo comando `source`.
    * **Mensagens Amigáveis:** O script fornece feedback claro de que o login foi bem-sucedido.

**Exemplo de Como Usar o Script de Login:**

Para configurar suas credenciais no terminal:

```bash
source researchers_scripts/login_datalake.sh SEU_USUARIO SUA_SENHA

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

