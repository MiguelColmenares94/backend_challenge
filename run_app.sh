#!/bin/bash

set -e

echo "Running Docker container: lexmax-api..."

sudo docker run \
  -p 8000:8000 \
  -e DATABASE_URL=sqlite:///lexmax.db \
  lexmax-api

echo "Container stopped."
