#!/bin/bash

# Build script for FLUX.1-dev Custom Faces RunPod Worker

set -e

echo "======================================"
echo "Building FLUX Custom Faces Docker Image"
echo "======================================"
echo ""

# Configuration
IMAGE_NAME="flux-custom-faces"
TAG="latest"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --tag)
      TAG="$2"
      shift 2
      ;;
    --name)
      IMAGE_NAME="$2"
      shift 2
      ;;
    --push)
      PUSH_IMAGE=true
      REGISTRY="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--tag TAG] [--name NAME] [--push REGISTRY]"
      exit 1
      ;;
  esac
done

FULL_IMAGE_NAME="${IMAGE_NAME}:${TAG}"

echo "Building image: ${FULL_IMAGE_NAME}"
echo ""
echo "⚠️  Note: This will download ~20GB of model weights"
echo "⏱️  Estimated build time: 30-60 minutes"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Build cancelled."
    exit 0
fi

echo ""
echo "Starting build..."
echo ""

# Build the Docker image
docker build \
  --tag "${FULL_IMAGE_NAME}" \
  --progress=plain \
  .

echo ""
echo "✓ Build completed successfully!"
echo ""
echo "Image: ${FULL_IMAGE_NAME}"
echo ""

# Push to registry if requested
if [[ "$PUSH_IMAGE" == "true" ]]; then
    echo "Pushing to registry: ${REGISTRY}"
    REGISTRY_IMAGE="${REGISTRY}/${FULL_IMAGE_NAME}"
    
    docker tag "${FULL_IMAGE_NAME}" "${REGISTRY_IMAGE}"
    docker push "${REGISTRY_IMAGE}"
    
    echo ""
    echo "✓ Image pushed to: ${REGISTRY_IMAGE}"
    echo ""
fi

echo "======================================"
echo "Next steps:"
echo "1. Test locally: ./test_local.sh"
echo "2. Push to registry: docker push <registry>/${FULL_IMAGE_NAME}"
echo "3. Deploy to RunPod"
echo "======================================"

