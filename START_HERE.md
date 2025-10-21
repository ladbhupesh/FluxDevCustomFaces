# 🚀 START HERE - Quick Build Guide

Follow these steps to build your FLUX Custom Faces worker with HF token authentication.

## Step 1: Get Your Hugging Face Token (2 minutes)

### 1.1 Accept FLUX.1-dev License
Visit: https://huggingface.co/black-forest-labs/FLUX.1-dev
- Click **"Agree and access repository"**
- Wait for instant approval

### 1.2 Create Token
Visit: https://huggingface.co/settings/tokens
- Click **"New token"**
- Name: `flux-build`
- Type: **Read**
- Click **"Generate"**
- Copy your token (starts with `hf_`)

## Step 2: Set Environment Variable (30 seconds)

```bash
# Set your HF token
export HF_TOKEN="hf_your_actual_token_here"

# Verify it's set
echo $HF_TOKEN
```

## Step 3: Build the Docker Image (30-60 minutes)

```bash
# Navigate to project directory
cd /home/Projects/FluxDevCustomFaces

# Start the build
./build.sh

# When prompted, press 'y' to continue
```

The build will:
1. ✓ Authenticate with Hugging Face
2. ✓ Download FLUX.1-dev (~17GB)
3. ✓ Download uncensored LoRA (~2GB)
4. ✓ Create Docker image (~25GB)

## Step 4: Test Locally (Optional)

```bash
# Start the worker
./test_local.sh

# In another terminal, test it
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d @test_input_minimal.json
```

## Step 5: Push to Registry

```bash
# Login to Docker Hub
docker login

# Tag your image
docker tag flux-custom-faces:latest ladbhupesh/flux-custom-faces:latest

# Push to registry
docker push ladbhupesh/flux-custom-faces:latest
```

## Step 6: Deploy to RunPod

1. Go to https://www.runpod.io/console/serverless
2. Click **"+ New Endpoint"**
3. Settings:
   - Name: `flux-custom-faces`
   - Container Image: `ladbhupesh/flux-custom-faces:latest`
   - Container Disk: `30 GB`
   - GPU: Select **RTX 4090**
   - Max Workers: `3`
4. Click **"Deploy"**
5. Wait 5-10 minutes
6. Copy your **Endpoint ID**

## Done! 🎉

Your worker is now deployed and ready to use!

## Test Your Endpoint

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
  }'
```

---

## Quick Reference

| File | Purpose |
|------|---------|
| `START_HERE.md` | This file - quick build guide |
| `BUILD_INSTRUCTIONS.md` | Detailed build documentation |
| `QUICKSTART.md` | Complete quick start guide |
| `DEPLOYMENT.md` | Full deployment guide |
| `README.md` | Project overview |

## Common Issues

### "HF_TOKEN is required!"
```bash
export HF_TOKEN="hf_your_token"
```

### "401 Unauthorized"
- Accept FLUX.1-dev license
- Check token is correct
- Generate new token

### "Out of disk space"
```bash
docker system prune -a
```

---

**Need help?** Read [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) for detailed troubleshooting.

**Ready to build?** Run `export HF_TOKEN="hf_xxx" && ./build.sh` 🚀

