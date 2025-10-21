# Deployment Guide

This guide walks you through deploying the FLUX.1-dev Custom Faces worker to RunPod.

## Prerequisites

- RunPod account ([Sign up](https://runpod.io))
- Docker installed locally
- Docker Hub or other container registry account
- GPU available for building (optional but recommended)

## Step 1: Build the Docker Image

### Option A: Build Locally (Recommended)

```bash
# Make scripts executable (if not already)
chmod +x build.sh test_local.sh

# Build the image
./build.sh

# This will:
# - Download ~20GB of model weights
# - Take 30-60 minutes depending on internet speed
# - Create a Docker image with all base models
```

### Option B: Build with Custom Tag

```bash
./build.sh --tag v1.0.0 --name my-custom-flux
```

## Step 2: Test Locally (Optional but Recommended)

Before deploying to RunPod, test the image locally:

```bash
# Start the worker locally
./test_local.sh
```

In another terminal, test with curl:

```bash
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d @test_input_minimal.json
```

## Step 3: Push to Container Registry

### Docker Hub

```bash
# Login to Docker Hub
docker login

# Tag the image
docker tag flux-custom-faces:latest yourusername/flux-custom-faces:latest

# Push to Docker Hub
docker push yourusername/flux-custom-faces:latest
```

### Other Registries (GitHub, AWS ECR, etc.)

```bash
# Example for GitHub Container Registry
docker login ghcr.io
docker tag flux-custom-faces:latest ghcr.io/yourusername/flux-custom-faces:latest
docker push ghcr.io/yourusername/flux-custom-faces:latest
```

## Step 4: Deploy to RunPod

### Create Serverless Endpoint

1. Go to [RunPod Dashboard](https://www.runpod.io/console/serverless)
2. Click **"+ New Endpoint"**
3. Fill in the details:

#### Basic Settings
- **Endpoint Name**: `flux-custom-faces`
- **Template Type**: Select **"Custom"**
- **Container Image**: `yourusername/flux-custom-faces:latest`
- **Container Disk**: `30 GB` (minimum)

#### GPU Configuration
Select one of:
- **RTX 4090** (recommended for cost/performance)
- **RTX A6000**
- **A100 40GB**
- **A100 80GB** (best performance)

#### Advanced Settings
- **Max Workers**: `3` (adjust based on budget)
- **Idle Timeout**: `5 seconds`
- **Execution Timeout**: `300 seconds`
- **GPUs per Worker**: `1`

#### Environment Variables (Optional)
You can set default values (can be overridden per request):
```
HF_TOKEN=hf_your_default_token
```

4. Click **"Deploy"**

### Wait for Deployment

- Initial deployment may take 5-10 minutes
- RunPod will pull your Docker image
- The endpoint will show as "Ready" when complete

## Step 5: Get Your Endpoint Details

After deployment:

1. Click on your endpoint
2. Note down:
   - **Endpoint ID**: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
   - **API Key**: Found in Account Settings → API Keys

## Step 6: Test Your Endpoint

### Using cURL

```bash
ENDPOINT_ID="your-endpoint-id"
API_KEY="your-runpod-api-key"

curl -X POST "https://api.runpod.ai/v2/${ENDPOINT_ID}/runsync" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "prompt": "Portrait of a person, professional studio lighting",
      "hf_token": "hf_your_token",
      "custom_lora_repo": "ladbhupesh/flux.1-dev-custom-faces",
      "num_inference_steps": 28,
      "guidance_scale": 3.5
    }
  }'
```

### Using Python

```python
import requests
import json

ENDPOINT_ID = "your-endpoint-id"
API_KEY = "your-runpod-api-key"

url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "input": {
        "prompt": "Professional portrait, studio lighting",
        "hf_token": "hf_your_token",
        "custom_lora_repo": "ladbhupesh/flux.1-dev-custom-faces",
        "aws_access_key_id": "your_aws_key",
        "aws_secret_access_key": "your_aws_secret",
        "s3_bucket": "your-bucket",
        "s3_prefix": "generated_images"
    }
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()

print(json.dumps(result, indent=2))
```

## Step 7: Monitor and Scale

### View Logs

1. Go to your endpoint in RunPod dashboard
2. Click "Logs" tab
3. Monitor for any errors or issues

### Scale Workers

Based on demand:
- Increase **Max Workers** for higher throughput
- Decrease for cost savings during low usage

### Monitor Costs

- Check RunPod dashboard for usage statistics
- Set up budget alerts in RunPod settings

## Updating Your Worker

When you make changes:

```bash
# Rebuild the image
./build.sh --tag v1.1.0

# Push to registry
docker tag flux-custom-faces:v1.1.0 yourusername/flux-custom-faces:v1.1.0
docker push yourusername/flux-custom-faces:v1.1.0

# Update endpoint in RunPod
# 1. Go to endpoint settings
# 2. Update Container Image to new tag
# 3. Click "Update Endpoint"
```

## Troubleshooting

### Build Issues

**Problem**: Out of disk space during build
```bash
# Clean up Docker
docker system prune -a
```

**Problem**: Download timeout
```bash
# Increase Docker timeout
export DOCKER_CLIENT_TIMEOUT=300
export COMPOSE_HTTP_TIMEOUT=300
```

### Deployment Issues

**Problem**: Container fails to start
- Check logs in RunPod dashboard
- Verify image was pushed correctly
- Ensure GPU is available

**Problem**: Endpoint always timing out
- Increase execution timeout in endpoint settings
- Check if GPU is being utilized (view logs)

### Runtime Issues

**Problem**: "CUDA out of memory"
- Reduce image dimensions in request
- Reduce `num_images`
- Use GPU with more VRAM

**Problem**: Slow generation times
- First request will be slower (model compilation)
- Subsequent requests should be faster
- Consider using faster GPU

**Problem**: S3 upload fails
- Verify AWS credentials
- Check bucket permissions
- Ensure bucket exists in specified region

## Cost Optimization

### Tips to Reduce Costs

1. **Use Spot Instances**: Enable in RunPod settings (cheaper but can be interrupted)
2. **Reduce Idle Time**: Lower idle timeout to 1-2 seconds
3. **Right-size GPU**: RTX 4090 offers best value for most workloads
4. **Batch Requests**: Generate multiple images in one request (`num_images`)
5. **Optimize Parameters**: Lower `num_inference_steps` (25-30 is usually sufficient)

### Expected Costs (approximate)

- **RTX 4090**: ~$0.40/hour
- **A100 40GB**: ~$1.50/hour
- **A100 80GB**: ~$2.50/hour

Per-image cost (at 30 steps, 1024x1024):
- **RTX 4090**: ~$0.002-0.003 per image
- **A100**: ~$0.005-0.008 per image

## Security Best Practices

1. **Never hardcode credentials** in Docker image
2. **Rotate API keys** regularly
3. **Use IAM roles** for AWS access when possible
4. **Monitor endpoint logs** for suspicious activity
5. **Set up alerts** for unusual usage patterns

## Support

- **RunPod Documentation**: https://docs.runpod.io/
- **RunPod Discord**: https://discord.gg/runpod
- **Open an Issue**: GitHub repository

---

**Ready to deploy? Start with Step 1!** 🚀

