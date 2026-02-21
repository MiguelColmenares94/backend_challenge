#!/bin/bash

set -e

echo "Building Docker image: lexmax-api..."
sudo docker build -t lexmax-api .

echo "Build completed successfully."
