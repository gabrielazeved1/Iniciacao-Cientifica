#!/bin/bash

# Script para configurar as variáveis de ambiente para acesso ao Data Lake MinIO.
# Este script deve ser executado usando 'source' ou '.' para que as variáveis sejam definidas na sessão atual do terminal.
#
# Uso:
#   source researchers_scripts/login_datalake.sh <usuario> <senha> [endpoint_minio]
#
# Exemplos:
#   1. Para acesso local (na mesma máquina que o MinIO):
#      source researchers_scripts/login_datalake.sh amanda amanda123
#
#   2. Para acesso via rede (para colegas, usando o IP da máquina servidor):
#      source researchers_scripts/login_datalake.sh amanda amanda123 192.168.18.31:9000
#
#   3. Para acesso dentro de outro contêiner Docker (ambiente de simulação):
#      source researchers_scripts/login_datalake.sh amanda amanda123 minio-server:9000

# Verifica se o usuário e a senha foram fornecidos
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Uso: source $0 <usuario> <senha> [endpoint_minio]"
  echo "Exemplo: source $0 amanda amanda123"
  echo "Exemplo: source $0 amanda amanda123 192.168.18.31:9000"
  return 1 # Retorna um código de erro se os argumentos estiverem faltando
fi

# Define as variáveis de ambiente de acesso
export MINIO_ACCESS_KEY="$1"
export MINIO_SECRET_KEY="$2"

# --- LÓGICA CORRIGIDA PARA O ENDPOINT ---
# Verifica se o terceiro argumento (endpoint_minio) foi fornecido
# Se fornecido, verifica se já contém o prefixo 'http://' ou 'https://'
# Se não contiver, adiciona 'http://' como padrão.
# Se não for fornecido, usa o padrão 'http://127.0.0.

if [ -n "$3" ]; then
  # Verifica se o argumento já tem http:// ou https://
  if [[ ! "$3" =~ ^https?:// ]]; then
      export MINIO_ENDPOINT="http://$3"
  else
      export MINIO_ENDPOINT="$3"
  fi
else
  # Usa o padrão local, com o prefixo 'http://' já incluso
  export MINIO_ENDPOINT="http://127.0.0.1:9000"
fi



echo "Credenciais MinIO configuradas para o usuário: $1"
echo "Endpoint MinIO configurado para: $MINIO_ENDPOINT"
echo "Agora você pode usar os scripts do Data Lake (upload, download, list, read)."