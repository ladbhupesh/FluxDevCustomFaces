#!/bin/bash

# Quick build script with HF token check

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║       FLUX.1-dev Custom Faces - Quick Build with HF Token      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if HF_TOKEN is set
if [ -z "$HF_TOKEN" ]; then
    echo "❌ HF_TOKEN not found!"
    echo ""
    echo "Please set your Hugging Face token:"
    echo ""
    echo "  export HF_TOKEN='hf_your_token_here'"
    echo ""
    echo "Get your token from: https://huggingface.co/settings/tokens"
    echo "Accept FLUX license: https://huggingface.co/black-forest-labs/FLUX.1-dev"
    echo ""
    exit 1
fi

echo "✓ HF_TOKEN found: ${HF_TOKEN:0:10}..."
echo ""
echo "Starting build process..."
echo ""

# Run the main build script
./build.sh "$@"
