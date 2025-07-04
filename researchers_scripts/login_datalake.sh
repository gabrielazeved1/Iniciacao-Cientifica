#!/bin/bash

# Script para configurar as variáveis de ambiente para acesso ao Data Lake MinIO.
#
# Uso:
#   source researchers_scripts/login_datalake.sh <usuario> <senha>
#
# Exemplo:
#   source researchers_scripts/login_datalake.sh amanda amanda123

# Verifica se os argumentos foram fornecidos
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Uso: source $0 <usuario> <senha>"
  echo "Exemplo: source $0 amanda amanda123"
  return 1 # Retorna um código de erro se os argumentos estiverem faltando
fi

# Define as variáveis de ambiente
export MINIO_ACCESS_KEY="$1"
export MINIO_SECRET_KEY="$2"

echo "Credenciais MinIO configuradas para o usuário: $1"
echo "Agora você pode usar os scripts do Data Lake (upload, download, list, read)."

# Opcional: Verifica se as variáveis foram definidas (para depuração)
# echo "MINIO_ACCESS_KEY: $MINIO_ACCESS_KEY"
# echo "MINIO_SECRET_KEY: $MINIO_SECRET_KEY"