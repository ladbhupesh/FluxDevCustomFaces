INPUT_SCHEMA = {
    "prompt": {
        "type": str,
        "required": True,
        "description": "The main text prompt describing the desired image"
    },
    "negative_prompt": {
        "type": str,
        "required": False,
        "default": None,
        "description": "Text prompt specifying concepts to exclude from the image"
    },
    "height": {
        "type": int,
        "required": False,
        "default": 1024,
        "description": "The height of the generated image in pixels",
        "constraints": lambda x: 256 <= x <= 2048
    },
    "width": {
        "type": int,
        "required": False,
        "default": 1024,
        "description": "The width of the generated image in pixels",
        "constraints": lambda x: 256 <= x <= 2048
    },
    "num_inference_steps": {
        "type": int,
        "required": False,
        "default": 28,
        "description": "Number of denoising steps",
        "constraints": lambda x: 1 <= x <= 100
    },
    "guidance_scale": {
        "type": float,
        "required": False,
        "default": 3.5,
        "description": "Classifier-Free Guidance scale",
        "constraints": lambda x: 0.0 <= x <= 20.0
    },
    "num_images": {
        "type": int,
        "required": False,
        "default": 1,
        "description": "Number of images to generate per prompt",
        "constraints": lambda x: 1 <= x <= 4
    },
    "seed": {
        "type": int,
        "required": False,
        "default": None,
        "description": "Random seed for reproducibility"
    },
    "aws_access_key_id": {
        "type": str,
        "required": False,
        "default": None,
        "description": "AWS access key ID for S3 upload"
    },
    "aws_secret_access_key": {
        "type": str,
        "required": False,
        "default": None,
        "description": "AWS secret access key for S3 upload"
    },
    "aws_region": {
        "type": str,
        "required": False,
        "default": "ap-south-1",
        "description": "AWS region for S3"
    },
    "s3_bucket": {
        "type": str,
        "required": False,
        "default": None,
        "description": "S3 bucket name for uploading generated images"
    },
    "s3_prefix": {
        "type": str,
        "required": False,
        "default": "runpods_custom_faces",
        "description": "S3 key prefix for uploaded images"
    },
    "hf_token": {
        "type": str,
        "required": False,
        "default": None,
        "description": "Hugging Face token for accessing private repositories"
    },
    "custom_lora_repo": {
        "type": str,
        "required": False,
        "default": None,
        "description": "Hugging Face repository ID for custom faces LoRA weights"
    },
    "custom_lora_weight_name": {
        "type": str,
        "required": False,
        "default": "lora.safetensors",
        "description": "Filename of the LoRA weights in the repository"
    }
}

