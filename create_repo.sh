#!/usr/bin/env bash
# Script para criar o repositório local e (opcional) publicar no GitHub usando gh CLI.
# Uso:
#   ./create_repo.sh               # cria estrutura, inicializa git, commit
#   ./create_repo.sh --push       # além disso, cria repositório remoto com gh e faz push
#
set -e
REPO_NAME="cyber-defense-demo"
AUTHOR="${GIT_AUTHOR_NAME:-$(git config user.name)}"
PUSH_REMOTE=0
if [ "$1" = "--push" ]; then
  PUSH_REMOTE=1
fi

# Cria árvore de diretórios
mkdir -p "$REPO_NAME"/src
mkdir -p "$REPO_NAME"/data
mkdir -p "$REPO_NAME"/output

# Copia arquivos a partir deste script: assume que os arquivos foram salvos manualmente.
echo "Por favor salve os arquivos do repositório nos paths correspondentes antes de rodar o restante do script."
echo "Se já salvou, prossiga."

cd "$REPO_NAME"

# Inicializa git
git init
git add .
git commit -m "Initial commit: cyber-defense-demo example"
echo "Commit criado localmente."

if [ $PUSH_REMOTE -eq 1 ]; then
  if ! command -v gh >/dev/null 2>&1; then
    echo "gh CLI não encontrado. Instale e autentique (gh auth login) para criar repositório remoto automaticamente."
    exit 1
  fi
  # cria repositório público; altere para --private se quiser privado
  gh repo create "$REPO_NAME" --public --source=. --remote=origin --push
  echo "Repositório remoto criado e push realizado."
else
  echo "Se quiser publicar no GitHub, execute: gh repo create ${USER:-<username>}/${REPO_NAME} --public --source=. --remote=origin --push"
fi