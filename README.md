# FLUX.1-dev Custom Faces RunPod Worker

A RunPod serverless worker for generating custom face images using FLUX.1-dev with uncensored LoRA and dynamic custom faces LoRA weights.

## Features

- 🚀 **Pre-loaded Models**: Base FLUX.1-dev model and uncensored LoRA weights are baked into the Docker image
- 🎭 **Dynamic Custom Faces**: Load custom faces LoRA weights dynamically from any Hugging Face repository
- ☁️ **S3 Integration**: Automatic upload of generated images to AWS S3
- 🔐 **Secure**: AWS credentials and Hugging Face tokens are passed per request, not baked into the image
- ⚡ **Fast**: Models are pre-cached for quick startup times
- 🎨 **Flexible**: Support for multiple images, custom seeds, and full parameter control

## Architecture

### Pre-loaded in Docker Image
- `black-forest-labs/FLUX.1-dev` - Base model
- `enhanceaiteam/Flux-uncensored` - Uncensored LoRA weights

### Loaded Dynamically per Request
- Custom faces LoRA weights (from specified Hugging Face repository)

## Getting Started

### Prerequisites

- RunPod account
- Hugging Face account with access token
- AWS account with S3 bucket (optional, for image upload)

### Building the Docker Image

```bash
docker build -t flux-custom-faces:latest .
```

**Note**: The build process will download ~20GB of model weights, so it may take some time.

### Deploying to RunPod

1. Push your Docker image to a container registry:
   ```bash
   docker tag flux-custom-faces:latest your-registry/flux-custom-faces:latest
   docker push your-registry/flux-custom-faces:latest
   ```

2. Create a new Serverless Endpoint in RunPod:
   - Go to RunPod Dashboard → Serverless → Deploy
   - Select "Custom" template
   - Enter your Docker image URL
   - Configure GPU (recommended: RTX 4090 or A100)
   - Set environment variables if needed

3. Wait for the endpoint to be ready

## API Usage

### Request Format

```json
{
  "input": {
    "prompt": "Portrait of a person, professional lighting",
    "negative_prompt": "blurry, low quality",
    "height": 1024,
    "width": 1024,
    "num_inference_steps": 28,
    "guidance_scale": 3.5,
    "num_images": 1,
    "seed": 42,
    "aws_access_key_id": "YOUR_AWS_ACCESS_KEY",
    "aws_secret_access_key": "YOUR_AWS_SECRET_KEY",
    "aws_region": "ap-south-1",
    "s3_bucket": "your-bucket-name",
    "s3_prefix": "runpods_custom_faces",
    "hf_token": "hf_YOUR_TOKEN",
    "custom_lora_repo": "ladbhupesh/flux.1-dev-custom-faces",
    "custom_lora_weight_name": "lora.safetensors"
  }
}
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | **Yes** | - | The main text prompt describing the desired image |
| `negative_prompt` | string | No | None | Text prompt specifying concepts to exclude |
| `height` | integer | No | 1024 | Image height in pixels (256-2048) |
| `width` | integer | No | 1024 | Image width in pixels (256-2048) |
| `num_inference_steps` | integer | No | 28 | Number of denoising steps (1-100) |
| `guidance_scale` | float | No | 3.5 | CFG scale (0.0-20.0) |
| `num_images` | integer | No | 1 | Number of images to generate (1-4) |
| `seed` | integer | No | random | Random seed for reproducibility |
| `aws_access_key_id` | string | No | None | AWS access key for S3 upload |
| `aws_secret_access_key` | string | No | None | AWS secret key for S3 upload |
| `aws_region` | string | No | ap-south-1 | AWS region for S3 |
| `s3_bucket` | string | No | None | S3 bucket name |
| `s3_prefix` | string | No | runpods_custom_faces | S3 key prefix |
| `hf_token` | string | No | None | Hugging Face token for private repos |
| `custom_lora_repo` | string | No | None | Hugging Face repo ID for custom LoRA |
| `custom_lora_weight_name` | string | No | lora.safetensors | LoRA weight filename |

### Response Format

```json
{
  "delayTime": 2500,
  "executionTime": 8500,
  "id": "unique-job-id",
  "output": {
    "image_url": "data:image/png;base64,...",
    "images": [
      "data:image/png;base64,..."
    ],
    "s3_urls": [
      "https://bucket.s3.region.amazonaws.com/path/image.png"
    ],
    "seed": 42,
    "num_images": 1
  },
  "status": "COMPLETED"
}
```

## Example Usage

### Python

```python
import requests
import json

endpoint_url = "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync"
headers = {
    "Authorization": "Bearer YOUR_RUNPOD_API_KEY",
    "Content-Type": "application/json"
}

payload = {
    "input": {
        "prompt": "Professional portrait of Bhupesh, studio lighting",
        "height": 1024,
        "width": 1024,
        "num_inference_steps": 28,
        "guidance_scale": 3.5,
        "seed": 42,
        "aws_access_key_id": "YOUR_AWS_KEY",
        "aws_secret_access_key": "YOUR_AWS_SECRET",
        "s3_bucket": "your-bucket",
        "hf_token": "hf_YOUR_TOKEN",
        "custom_lora_repo": "ladbhupesh/flux.1-dev-custom-faces"
    }
}

response = requests.post(endpoint_url, headers=headers, json=payload)
result = response.json()

print(f"Status: {result['status']}")
if result['status'] == 'COMPLETED':
    print(f"S3 URLs: {result['output']['s3_urls']}")
```

### cURL

```bash
curl -X POST https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync \
  -H "Authorization: Bearer YOUR_RUNPOD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "prompt": "Portrait of a person",
      "hf_token": "hf_YOUR_TOKEN",
      "custom_lora_repo": "ladbhupesh/flux.1-dev-custom-faces"
    }
  }'
```

## Local Testing

You can test the worker locally using the provided test input:

```bash
# Build the image
docker build -t flux-custom-faces:latest .

# Run locally
docker run --gpus all -v $(pwd)/test_input.json:/test_input.json flux-custom-faces:latest
```

## Configuration

### Environment Variables

You can optionally set these environment variables in the RunPod endpoint configuration:

- `HF_TOKEN` - Default Hugging Face token (can be overridden per request)
- `AWS_ACCESS_KEY_ID` - Default AWS access key (can be overridden per request)
- `AWS_SECRET_ACCESS_KEY` - Default AWS secret key (can be overridden per request)

## Performance Notes

- **First Request**: May take 2-3 minutes for model compilation
- **Subsequent Requests**: Typically 5-15 seconds depending on parameters
- **Recommended GPU**: RTX 4090, A100, or better
- **VRAM Requirements**: Minimum 16GB, recommended 24GB+

## Security Best Practices

⚠️ **Important Security Notes:**

1. **Never hardcode credentials** in your code or Docker image
2. Pass AWS credentials and HF tokens as **request parameters**
3. Use **IAM roles** with minimal required permissions for S3
4. Store tokens securely using environment variables or secrets management
5. Rotate credentials regularly

## Troubleshooting

### Out of Memory Errors
- Reduce `height` and `width`
- Reduce `num_images`
- Use a GPU with more VRAM

### Slow Generation
- Reduce `num_inference_steps` (try 20-25)
- Use smaller image dimensions
- Upgrade to a faster GPU

### LoRA Loading Errors
- Verify the Hugging Face repository is accessible
- Check that the `custom_lora_weight_name` matches the actual file
- Ensure your HF token has the correct permissions

### S3 Upload Failures
- Verify AWS credentials are correct
- Check S3 bucket permissions
- Ensure the bucket exists and is in the specified region

## Project Structure

```
.
├── Dockerfile                 # Docker image configuration
├── handler.py                # Main RunPod worker handler
├── schemas.py                # Input validation schemas
├── download_weights.py       # Script to pre-download models
├── requirements.txt          # Python dependencies
├── test_input.json          # Example request for testing
└── README.md                # This file
```

## License

MIT License - See LICENSE file for details

## Credits

- Based on [PrunaAI/runpod-worker-FLUX.1-dev](https://github.com/PrunaAI/runpod-worker-FLUX.1-dev)
- Uses [FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev) by Black Forest Labs
- Uncensored LoRA by [enhanceaiteam](https://huggingface.co/enhanceaiteam/Flux-uncensored)

## Support

For issues and questions:
- Open an issue on GitHub
- Check RunPod documentation: https://docs.runpod.io/
- Hugging Face documentation: https://huggingface.co/docs

---

**Built with ❤️ for flexible custom face generation**

