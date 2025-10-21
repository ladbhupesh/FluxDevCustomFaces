import runpod
import torch
from diffusers import FluxPipeline
import boto3
import base64
import io
import os
from datetime import datetime
from schemas import INPUT_SCHEMA
from huggingface_hub import login


# Global pipeline variable
pipe = None


def initialize_pipeline():
    """Initialize the Flux pipeline with base model and uncensored LoRA"""
    global pipe
    
    if pipe is not None:
        return pipe
    
    print("Initializing Flux pipeline...")
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    
    # Load base model from cache
    pipe = FluxPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-dev",
        cache_dir='/workspace/models',
        torch_dtype=torch.bfloat16
    ).to(device)
    
    # Load uncensored LoRA (pre-downloaded)
    print("Loading uncensored LoRA weights...")
    pipe.load_lora_weights("enhanceaiteam/Flux-uncensored")
    
    print("Pipeline initialized successfully!")
    return pipe


def generate_image(job):
    """
    Main handler function for RunPod worker
    """
    try:
        job_input = job['input']
        
        # Extract AWS credentials
        aws_access_key_id = job_input.get('aws_access_key_id')
        aws_secret_access_key = job_input.get('aws_secret_access_key')
        aws_region = job_input.get('aws_region', 'ap-south-1')
        s3_bucket = job_input.get('s3_bucket')
        s3_prefix = job_input.get('s3_prefix', 'runpods_custom_faces')
        
        # Extract Hugging Face credentials
        hf_token = job_input.get('hf_token')
        
        # Extract custom faces LoRA details
        custom_lora_repo = job_input.get('custom_lora_repo')
        custom_lora_weight_name = job_input.get('custom_lora_weight_name', 'lora.safetensors')
        
        # Extract image generation parameters
        prompt = job_input['prompt']
        negative_prompt = job_input.get('negative_prompt', None)
        height = job_input.get('height', 1024)
        width = job_input.get('width', 1024)
        num_inference_steps = job_input.get('num_inference_steps', 28)
        guidance_scale = job_input.get('guidance_scale', 3.5)
        num_images = job_input.get('num_images', 1)
        seed = job_input.get('seed', None)
        
        # Login to Hugging Face if token provided
        if hf_token:
            print("Logging in to Hugging Face...")
            login(token=hf_token, add_to_git_credential=False)
        
        # Initialize pipeline
        global pipe
        pipe = initialize_pipeline()
        
        # Load custom faces LoRA if provided
        if custom_lora_repo:
            print(f"Loading custom faces LoRA from {custom_lora_repo}...")
            pipe.load_lora_weights(custom_lora_repo, weight_name=custom_lora_weight_name)
        
        # Set seed for reproducibility
        if seed is not None:
            generator = torch.Generator(device=pipe.device).manual_seed(seed)
        else:
            generator = None
            seed = torch.randint(0, 2**32, (1,)).item()
        
        # Clear CUDA cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        print(f"Generating {num_images} image(s) with prompt: '{prompt}'")
        
        # Generate images
        output = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            height=height,
            width=width,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            num_images_per_prompt=num_images,
            generator=generator
        )
        
        images = output.images
        image_urls = []
        s3_urls = []
        
        # Initialize S3 client if credentials provided
        s3_client = None
        if aws_access_key_id and aws_secret_access_key and s3_bucket:
            print("Initializing S3 client...")
            s3_client = boto3.client(
                's3',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=aws_region
            )
        
        # Process each generated image
        for idx, image in enumerate(images):
            # Convert image to base64
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            image_url = f"data:image/png;base64,{img_str}"
            image_urls.append(image_url)
            
            # Upload to S3 if configured
            if s3_client:
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                filename = f"{timestamp}_{idx}.png"
                s3_key = f"{s3_prefix}/{filename}"
                
                print(f"Uploading image {idx + 1} to S3...")
                buffered.seek(0)
                s3_client.put_object(
                    Bucket=s3_bucket,
                    Key=s3_key,
                    Body=buffered.getvalue(),
                    ContentType='image/png'
                )
                
                s3_url = f"https://{s3_bucket}.s3.{aws_region}.amazonaws.com/{s3_key}"
                s3_urls.append(s3_url)
                print(f"Image uploaded to: {s3_url}")
        
        # Prepare response
        result = {
            "images": image_urls,
            "seed": seed,
            "num_images": len(images)
        }
        
        if s3_urls:
            result["s3_urls"] = s3_urls
        
        # Add the first image as legacy 'image_url' field
        if image_urls:
            result["image_url"] = image_urls[0]
        
        print("Image generation completed successfully!")
        return result
        
    except Exception as e:
        print(f"Error during image generation: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}


print("Starting RunPod Serverless Worker...")
runpod.serverless.start({"handler": generate_image})

