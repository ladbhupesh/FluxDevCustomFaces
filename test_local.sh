#!/bin/bash

# Local testing script for FLUX.1-dev Custom Faces RunPod Worker

set -e

echo "======================================"
echo "Testing FLUX Custom Faces Locally"
echo "======================================"
echo ""

# Configuration
IMAGE_NAME="flux-custom-faces:latest"
PORT=8000

# Check if Docker image exists
if ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "❌ Error: Docker image '${IMAGE_NAME}' not found"
    echo "Please build the image first: ./build.sh"
    exit 1
fi

# Check if GPU is available
if ! command -v nvidia-smi &> /dev/null; then
    echo "⚠️  Warning: nvidia-smi not found. GPU may not be available."
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

echo "Starting container..."
echo ""

# Run the container interactively
docker run --rm -it \
  --gpus all \
  -p ${PORT}:${PORT} \
  -e RUNPOD_DEBUG_LEVEL=DEBUG \
  "${IMAGE_NAME}"

echo ""
echo "Container stopped."

