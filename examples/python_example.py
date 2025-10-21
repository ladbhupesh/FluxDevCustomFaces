#!/usr/bin/env python3
"""
Python example for using the FLUX Custom Faces RunPod Worker
"""

import requests
import json
import base64
import os
from datetime import datetime


class FluxCustomFacesClient:
    """Client for FLUX Custom Faces RunPod Worker"""
    
    def __init__(self, endpoint_id: str, api_key: str):
        """
        Initialize the client
        
        Args:
            endpoint_id: Your RunPod endpoint ID
            api_key: Your RunPod API key
        """
        self.endpoint_id = endpoint_id
        self.api_key = api_key
        self.base_url = f"https://api.runpod.ai/v2/{endpoint_id}"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_sync(self, **kwargs):
        """
        Generate image synchronously (waits for completion)
        
        Args:
            prompt (str): Main text prompt
            negative_prompt (str, optional): Negative prompt
            height (int, optional): Image height (default: 1024)
            width (int, optional): Image width (default: 1024)
            num_inference_steps (int, optional): Number of steps (default: 28)
            guidance_scale (float, optional): CFG scale (default: 3.5)
            num_images (int, optional): Number of images (default: 1)
            seed (int, optional): Random seed
            hf_token (str, optional): Hugging Face token
            custom_lora_repo (str, optional): Custom LoRA repository
            custom_lora_weight_name (str, optional): LoRA weight filename
            aws_access_key_id (str, optional): AWS access key
            aws_secret_access_key (str, optional): AWS secret key
            aws_region (str, optional): AWS region
            s3_bucket (str, optional): S3 bucket name
            s3_prefix (str, optional): S3 key prefix
            
        Returns:
            dict: Response from RunPod
        """
        url = f"{self.base_url}/runsync"
        payload = {"input": kwargs}
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def generate_async(self, **kwargs):
        """
        Generate image asynchronously (returns job ID immediately)
        
        Args: Same as generate_sync()
        
        Returns:
            dict: Job information with ID
        """
        url = f"{self.base_url}/run"
        payload = {"input": kwargs}
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def check_status(self, job_id: str):
        """
        Check status of async job
        
        Args:
            job_id: Job ID from generate_async()
            
        Returns:
            dict: Job status and results if completed
        """
        url = f"{self.base_url}/status/{job_id}"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def cancel_job(self, job_id: str):
        """
        Cancel a running job
        
        Args:
            job_id: Job ID to cancel
            
        Returns:
            dict: Cancellation response
        """
        url = f"{self.base_url}/cancel/{job_id}"
        
        response = requests.post(url, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    @staticmethod
    def save_base64_image(base64_string: str, output_path: str):
        """
        Save base64 encoded image to file
        
        Args:
            base64_string: Base64 string (with or without data URI prefix)
            output_path: Path to save the image
        """
        # Remove data URI prefix if present
        if base64_string.startswith('data:image'):
            base64_string = base64_string.split(',')[1]
        
        # Decode and save
        image_data = base64.b64decode(base64_string)
        with open(output_path, 'wb') as f:
            f.write(image_data)
        
        print(f"Image saved to: {output_path}")


def example_basic():
    """Basic example with minimal configuration"""
    
    # Configuration
    ENDPOINT_ID = os.getenv("RUNPOD_ENDPOINT_ID", "your-endpoint-id")
    API_KEY = os.getenv("RUNPOD_API_KEY", "your-api-key")
    HF_TOKEN = os.getenv("HF_TOKEN", "hf_your_token")
    
    # Initialize client
    client = FluxCustomFacesClient(ENDPOINT_ID, API_KEY)
    
    # Generate image
    print("Generating image...")
    result = client.generate_sync(
        prompt="Professional portrait of a person, studio lighting",
        hf_token=HF_TOKEN,
        custom_lora_repo="ladbhupesh/flux.1-dev-custom-faces"
    )
    
    # Check result
    if result['status'] == 'COMPLETED':
        print(f"✓ Generation completed!")
        print(f"  Seed: {result['output']['seed']}")
        print(f"  Execution time: {result['executionTime']}ms")
        
        # Save first image
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"output_{timestamp}.png"
        client.save_base64_image(result['output']['images'][0], output_path)
    else:
        print(f"✗ Generation failed: {result}")


def example_advanced():
    """Advanced example with all options"""
    
    # Configuration
    ENDPOINT_ID = os.getenv("RUNPOD_ENDPOINT_ID")
    API_KEY = os.getenv("RUNPOD_API_KEY")
    HF_TOKEN = os.getenv("HF_TOKEN")
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    S3_BUCKET = os.getenv("S3_BUCKET")
    
    client = FluxCustomFacesClient(ENDPOINT_ID, API_KEY)
    
    # Generate with all options
    print("Generating images with advanced options...")
    result = client.generate_sync(
        prompt="Portrait of Bhupesh, professional headshot, studio lighting",
        negative_prompt="blurry, low quality, distorted, cartoon",
        height=1024,
        width=1024,
        num_inference_steps=28,
        guidance_scale=3.5,
        num_images=2,
        seed=42,
        hf_token=HF_TOKEN,
        custom_lora_repo="ladbhupesh/flux.1-dev-custom-faces",
        custom_lora_weight_name="lora.safetensors",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        aws_region="ap-south-1",
        s3_bucket=S3_BUCKET,
        s3_prefix="flux_custom_faces"
    )
    
    # Process result
    if result['status'] == 'COMPLETED':
        print(f"✓ Generated {result['output']['num_images']} images")
        print(f"  Seed: {result['output']['seed']}")
        print(f"  Execution time: {result['executionTime']}ms")
        
        # Save all images
        for idx, image_base64 in enumerate(result['output']['images']):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"output_{timestamp}_{idx}.png"
            client.save_base64_image(image_base64, output_path)
        
        # Print S3 URLs if available
        if 's3_urls' in result['output']:
            print("\nS3 URLs:")
            for url in result['output']['s3_urls']:
                print(f"  - {url}")
    else:
        print(f"✗ Generation failed: {result}")


def example_async():
    """Example using async generation"""
    
    ENDPOINT_ID = os.getenv("RUNPOD_ENDPOINT_ID")
    API_KEY = os.getenv("RUNPOD_API_KEY")
    HF_TOKEN = os.getenv("HF_TOKEN")
    
    client = FluxCustomFacesClient(ENDPOINT_ID, API_KEY)
    
    # Start async generation
    print("Starting async generation...")
    job = client.generate_async(
        prompt="Portrait of a person, professional lighting",
        hf_token=HF_TOKEN,
        custom_lora_repo="ladbhupesh/flux.1-dev-custom-faces"
    )
    
    job_id = job['id']
    print(f"Job ID: {job_id}")
    
    # Poll for completion
    import time
    while True:
        status = client.check_status(job_id)
        
        if status['status'] == 'COMPLETED':
            print("✓ Generation completed!")
            result = status
            break
        elif status['status'] == 'FAILED':
            print(f"✗ Generation failed: {status}")
            return
        else:
            print(f"Status: {status['status']}, waiting...")
            time.sleep(2)
    
    # Save result
    if 'output' in result:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"output_{timestamp}.png"
        client.save_base64_image(result['output']['images'][0], output_path)


if __name__ == "__main__":
    # Run basic example
    print("=" * 60)
    print("Basic Example")
    print("=" * 60)
    example_basic()
    
    # Uncomment to run other examples:
    # example_advanced()
    # example_async()

