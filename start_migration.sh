#!/bin/bash

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 \"migration name\""
  exit 1
fi

MIGRATION_NAME="$1"

echo "Creating migration: $MIGRATION_NAME"

alembic revision --autogenerate -m "$MIGRATION_NAME"
alembic upgrade head

echo "Migration completed successfully."
