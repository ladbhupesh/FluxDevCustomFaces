# Use NVIDIA CUDA base image with Ubuntu
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY handler.py .
COPY schemas.py .
COPY download_weights.py .

# Create models directory
RUN mkdir -p /workspace/models

# Download base model and uncensored LoRA weights during build
# This ensures they're baked into the image
RUN python3 download_weights.py

# Set the entrypoint to run the handler
CMD ["python3", "handler.py"]

