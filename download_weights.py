#!/usr/bin/env python3
"""
Script to pre-download FLUX.1-dev base model and uncensored LoRA weights
This runs during Docker image build to cache the models
"""

import torch
from diffusers import FluxPipeline
from huggingface_hub import snapshot_download
import os


def download_base_model():
    """Download FLUX.1-dev base model"""
    print("=" * 80)
    print("Downloading FLUX.1-dev base model...")
    print("=" * 80)
    
    cache_dir = "/workspace/models"
    os.makedirs(cache_dir, exist_ok=True)
    
    try:
        # Download the base model
        pipe = FluxPipeline.from_pretrained(
            "black-forest-labs/FLUX.1-dev",
            cache_dir=cache_dir,
            torch_dtype=torch.bfloat16
        )
        print("✓ FLUX.1-dev base model downloaded successfully!")
        
        # Clean up to save memory
        del pipe
        
    except Exception as e:
        print(f"✗ Error downloading base model: {e}")
        raise


def download_uncensored_lora():
    """Download uncensored LoRA weights"""
    print("=" * 80)
    print("Downloading Flux-uncensored LoRA weights...")
    print("=" * 80)
    
    cache_dir = "/workspace/models"
    os.makedirs(cache_dir, exist_ok=True)
    
    try:
        # Download the uncensored LoRA
        snapshot_download(
            repo_id="enhanceaiteam/Flux-uncensored",
            cache_dir=cache_dir,
            local_dir=f"{cache_dir}/enhanceaiteam--Flux-uncensored",
            local_dir_use_symlinks=False
        )
        print("✓ Flux-uncensored LoRA weights downloaded successfully!")
        
    except Exception as e:
        print(f"✗ Error downloading uncensored LoRA: {e}")
        raise


def main():
    """Main download function"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "FLUX.1-dev Weights Download" + " " * 31 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")
    
    # Check if CUDA is available
    if torch.cuda.is_available():
        print(f"✓ CUDA available: {torch.cuda.get_device_name(0)}")
    else:
        print("⚠ CUDA not available, using CPU")
    
    print("\n")
    
    # Download base model
    download_base_model()
    
    print("\n")
    
    # Download uncensored LoRA
    download_uncensored_lora()
    
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 25 + "Download Complete!" + " " * 32 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")


if __name__ == "__main__":
    main()

