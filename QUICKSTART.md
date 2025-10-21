# Quick Start Guide

Get your FLUX Custom Faces worker up and running in 5 steps!

## 📋 Prerequisites

- [x] Docker installed
- [x] RunPod account ([Sign up](https://runpod.io))
- [x] Hugging Face token ([Get token](https://huggingface.co/settings/tokens))
- [x] GPU with 16GB+ VRAM (for building) or use RunPod for building

## 🚀 5-Minute Setup

### Step 1: Clone and Review

```bash
cd /home/Projects/FluxDevCustomFaces
ls -la

# You should see:
# - handler.py        (Main worker logic)
# - Dockerfile        (Container configuration)
# - requirements.txt  (Python dependencies)
# - build.sh         (Build script)
# - test_input.json  (Example request)
```

### Step 2: Build the Docker Image

```bash
# Build with included script
./build.sh

# This will:
# ✓ Download FLUX.1-dev model (~20GB)
# ✓ Download uncensored LoRA weights
# ✓ Install all dependencies
# ⏱️ Takes 30-60 minutes
```

**Alternative: Build on RunPod GPU Cloud**

If you don't have a local GPU, build on RunPod:

1. Go to RunPod → Pods
2. Deploy a GPU pod (RTX 4090 recommended)
3. Upload project files
4. Run `./build.sh` in the pod
5. Push to Docker Hub from the pod

### Step 3: Test Locally (Optional)

```bash
# Start the worker
./test_local.sh

# In another terminal, test with curl:
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d @test_input_minimal.json
```

### Step 4: Push to Registry

```bash
# Login to Docker Hub
docker login

# Tag and push
docker tag flux-custom-faces:latest YOUR_USERNAME/flux-custom-faces:latest
docker push YOUR_USERNAME/flux-custom-faces:latest
```

### Step 5: Deploy to RunPod

1. Go to [RunPod Serverless](https://www.runpod.io/console/serverless)
2. Click **+ New Endpoint**
3. Configure:
   - **Name**: `flux-custom-faces`
   - **Type**: Custom
   - **Image**: `YOUR_USERNAME/flux-custom-faces:latest`
   - **GPU**: RTX 4090 (recommended)
   - **Container Disk**: 30GB
   - **Max Workers**: 3
4. Click **Deploy**
5. Wait 5-10 minutes for deployment
6. Copy your **Endpoint ID**

## ✨ First API Call

### Using cURL

```bash
export RUNPOD_ENDPOINT_ID="your-endpoint-id"
export RUNPOD_API_KEY="your-api-key"
export HF_TOKEN="hf_your_token"

curl -X POST "https://api.runpod.ai/v2/${RUNPOD_ENDPOINT_ID}/runsync" \
  -H "Authorization: Bearer ${RUNPOD_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "prompt": "Professional portrait of a person, studio lighting",
      "hf_token": "'"${HF_TOKEN}"'",
      "custom_lora_repo": "ladbhupesh/flux.1-dev-custom-faces"
    }
  }' | jq '.output.s3_urls'
```

### Using Python

```bash
# Install dependencies
pip install requests

# Run example
cd examples
python python_example.py
```

### Using Node.js

```bash
# Install dependencies
cd examples
npm install

# Run example
node nodejs_example.js
```

## 🎯 Common Use Cases

### 1. Basic Generation

```json
{
  "input": {
    "prompt": "Portrait of a person with professional lighting",
    "hf_token": "hf_your_token",
    "custom_lora_repo": "ladbhupesh/flux.1-dev-custom-faces"
  }
}
```

### 2. With S3 Upload

```json
{
  "input": {
    "prompt": "Portrait of a person",
    "hf_token": "hf_your_token",
    "custom_lora_repo": "ladbhupesh/flux.1-dev-custom-faces",
    "aws_access_key_id": "YOUR_AWS_KEY",
    "aws_secret_access_key": "YOUR_AWS_SECRET",
    "s3_bucket": "your-bucket",
    "s3_prefix": "generated_images"
  }
}
```

### 3. Multiple Images

```json
{
  "input": {
    "prompt": "Portrait of a person",
    "num_images": 4,
    "seed": 42,
    "hf_token": "hf_your_token",
    "custom_lora_repo": "ladbhupesh/flux.1-dev-custom-faces"
  }
}
```

### 4. Custom Parameters

```json
{
  "input": {
    "prompt": "Professional portrait with studio lighting",
    "negative_prompt": "blurry, low quality, distorted",
    "height": 1024,
    "width": 1024,
    "num_inference_steps": 28,
    "guidance_scale": 3.5,
    "seed": 42,
    "hf_token": "hf_your_token",
    "custom_lora_repo": "ladbhupesh/flux.1-dev-custom-faces"
  }
}
```

## 📊 Expected Performance

| GPU | Cold Start | Warm Request | Cost/Image |
|-----|------------|--------------|------------|
| RTX 4090 | 2-3 min | 8-12 sec | ~$0.002 |
| A100 40GB | 1-2 min | 5-8 sec | ~$0.005 |
| A100 80GB | 1-2 min | 4-6 sec | ~$0.008 |

*Times for 1024x1024, 28 steps*

## 🔧 Optimization Tips

1. **Reduce Inference Steps**: Try 20-25 instead of 28
   - Faster generation
   - Minimal quality loss

2. **Batch Multiple Images**: Use `num_images` instead of separate requests
   - More efficient
   - Lower cost per image

3. **Use Consistent Seeds**: For reproducible results
   - Same seed = same output
   - Good for testing

4. **Right-size GPU**: 
   - RTX 4090: Best value for 1024x1024
   - A100: For larger batches or faster generation

5. **Set Idle Timeout Low**: 1-2 seconds
   - Workers shut down when idle
   - Save costs

## 🐛 Troubleshooting

### Build fails with "Out of space"
```bash
# Clean Docker
docker system prune -a -f
```

### "CUDA out of memory" during generation
- Reduce image dimensions: `"height": 768, "width": 768`
- Reduce num_images: `"num_images": 1`
- Use GPU with more VRAM

### S3 upload fails
- Verify AWS credentials are correct
- Check bucket permissions (must allow PutObject)
- Ensure bucket exists in specified region

### First request times out
- First request takes 2-3 minutes (model compilation)
- Increase timeout in RunPod settings to 300 seconds
- Subsequent requests will be much faster

### "Invalid HF token"
- Check token has read access
- For private repos, ensure token has correct permissions
- Get token from: https://huggingface.co/settings/tokens

## 📚 Next Steps

1. **Explore Examples**: Check out `examples/` directory
   - Python client
   - Node.js client
   - cURL scripts

2. **Read Full Documentation**:
   - [README.md](README.md) - Full feature list
   - [DEPLOYMENT.md](DEPLOYMENT.md) - Detailed deployment guide
   - [examples/README.md](examples/README.md) - Code examples

3. **Customize**:
   - Modify `handler.py` for custom logic
   - Add your own LoRA models
   - Integrate with your application

4. **Monitor**:
   - Check RunPod dashboard for usage
   - View logs for debugging
   - Set up alerts for errors

## 💡 Tips for Production

1. **Security**:
   - Never hardcode credentials
   - Use environment variables
   - Rotate keys regularly

2. **Cost Management**:
   - Use spot instances for 50% savings
   - Set max workers based on demand
   - Monitor usage daily

3. **Performance**:
   - Keep workers warm with health checks
   - Use async endpoints for batching
   - Cache common prompts

4. **Reliability**:
   - Implement retry logic
   - Handle errors gracefully
   - Log all requests

## 🆘 Need Help?

- **Documentation**: See [README.md](README.md)
- **Deployment Issues**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Code Examples**: See [examples/README.md](examples/README.md)
- **RunPod Docs**: https://docs.runpod.io/
- **Discord**: https://discord.gg/runpod

## 🎉 Success!

You now have a fully functional FLUX Custom Faces worker!

Try generating your first image:

```bash
./examples/curl_example.sh basic
```

Or explore the interactive menu:

```bash
./examples/curl_example.sh
```

Happy generating! 🎨✨

