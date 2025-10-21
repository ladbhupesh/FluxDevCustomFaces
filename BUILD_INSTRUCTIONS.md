# Build Instructions

This guide explains how to build the Docker image with Hugging Face authentication.

## Prerequisites

1. **Docker installed** with GPU support
2. **Hugging Face account** with access to FLUX.1-dev
3. **Hugging Face token** with read permissions

## Get Your Hugging Face Token

1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Name: `flux-custom-faces-build`
4. Type: **Read** (sufficient for building)
5. Click "Generate"
6. Copy your token (starts with `hf_`)

## Accept FLUX.1-dev License

Before building, you must accept the model license:

1. Go to https://huggingface.co/black-forest-labs/FLUX.1-dev
2. Click "Agree and access repository"
3. Wait for approval (usually instant)

## Build Methods

### Method 1: Environment Variable (Recommended)

```bash
# Set HF_TOKEN in your environment
export HF_TOKEN="hf_your_token_here"

# Build the image
./build.sh
```

**Advantages:**
- ✅ Token not visible in command history
- ✅ Can be reused across multiple builds
- ✅ More secure

### Method 2: Command Line Argument

```bash
# Pass token directly to build script
./build.sh --hf-token "hf_your_token_here"
```

**Advantages:**
- ✅ Quick one-off builds
- ✅ No need to export variable

**Disadvantages:**
- ⚠️ Token visible in shell history
- ⚠️ Less secure

### Method 3: Docker Build Directly

```bash
# Build with docker directly
docker build \
  --build-arg HF_TOKEN="hf_your_token_here" \
  --tag flux-custom-faces:latest \
  --progress=plain \
  .
```

## Build Process

Once you run the build command:

1. **Confirmation prompt** - Press `y` to continue
2. **System packages** - Install Python, CUDA, etc. (~5 min)
3. **Python dependencies** - Install PyTorch, Diffusers, etc. (~10 min)
4. **HF Authentication** - Login with your token
5. **Download FLUX.1-dev** - Download base model (~17GB, 15-30 min)
6. **Download uncensored LoRA** - Download LoRA weights (~2GB, 2-5 min)
7. **Finalize image** - Complete build

**Total time: 30-60 minutes** (depends on internet speed)

## Build Output

```bash
Building image: flux-custom-faces:latest
✓ HF_TOKEN: hf_xxxxxxxx...

⚠️  Note: This will download ~20GB of model weights
⏱️  Estimated build time: 30-60 minutes

Continue? (y/n) y

Starting build...

[Docker build logs...]

Authenticating with Hugging Face...
✓ Successfully authenticated with Hugging Face

Downloading FLUX.1-dev base model...
✓ FLUX.1-dev base model downloaded successfully!

Downloading Flux-uncensored LoRA weights...
✓ Flux-uncensored LoRA weights downloaded successfully!

✓ Build completed successfully!
```

## Verify Build

```bash
# Check image was created
docker images | grep flux-custom-faces

# Should show:
# flux-custom-faces    latest    abc123def456    2 minutes ago    25GB
```

## Security Best Practices

### ✅ DO:
- Store tokens in environment variables
- Use read-only tokens for building
- Rotate tokens regularly
- Keep tokens private

### ❌ DON'T:
- Commit tokens to Git
- Share tokens publicly
- Use write tokens for building
- Include tokens in Docker images (they're only used during build)

## Token Security

**Important:** The HF_TOKEN is only used during the Docker build process to download models. It is **NOT** stored in the final Docker image.

You can verify this:

```bash
# Inspect the image - HF_TOKEN should not be present
docker history flux-custom-faces:latest | grep HF_TOKEN
# (Should return nothing)

# Run container and check env
docker run --rm flux-custom-faces:latest env | grep HF_TOKEN
# (Should return nothing)
```

The token is passed as a build argument and used only during the `RUN python3 download_weights.py` step.

## Troubleshooting

### Error: "HF_TOKEN is required!"

**Problem:** No token provided

**Solution:**
```bash
export HF_TOKEN="hf_your_token_here"
./build.sh
```

### Error: "401 Client Error: Unauthorized"

**Problem:** Token is invalid or doesn't have access to FLUX.1-dev

**Solutions:**
1. Check token is correct (starts with `hf_`)
2. Verify you accepted FLUX.1-dev license
3. Generate new token with read permissions
4. Wait a few minutes after accepting license

### Error: "Repository not found"

**Problem:** Haven't accepted FLUX.1-dev license

**Solution:**
1. Go to https://huggingface.co/black-forest-labs/FLUX.1-dev
2. Click "Agree and access repository"
3. Wait for approval
4. Retry build

### Build fails during download

**Problem:** Network interruption or slow connection

**Solutions:**
1. Check internet connection
2. Retry build (Docker caches previous steps)
3. Use a machine with better internet
4. Consider building on RunPod GPU pod

### Out of disk space

**Problem:** Not enough space for models (~25GB needed)

**Solution:**
```bash
# Clean up Docker
docker system prune -a

# Check available space
df -h
```

## Advanced Options

### Build with Custom Tag

```bash
export HF_TOKEN="hf_your_token"
./build.sh --tag v1.0.0
```

### Build and Push to Registry

```bash
export HF_TOKEN="hf_your_token"
./build.sh --push docker.io/yourusername
```

### Build with Custom Name

```bash
export HF_TOKEN="hf_your_token"
./build.sh --name my-flux-worker --tag latest
```

## Alternative: Build on RunPod

If you don't have local GPU or sufficient bandwidth:

1. **Deploy GPU Pod** on RunPod
   - Choose RTX 4090 or A100
   - Select Ubuntu with Docker

2. **Upload project files**
   ```bash
   rsync -avz . root@runpod-pod-ip:/workspace/flux-build/
   ```

3. **SSH into pod and build**
   ```bash
   ssh root@runpod-pod-ip
   cd /workspace/flux-build
   export HF_TOKEN="hf_your_token"
   ./build.sh
   ```

4. **Push to registry from pod**
   ```bash
   docker login
   docker tag flux-custom-faces:latest yourusername/flux-custom-faces:latest
   docker push yourusername/flux-custom-faces:latest
   ```

5. **Terminate pod** (image is now in registry)

## Next Steps

After successful build:

1. **Test locally**: `./test_local.sh`
2. **Push to registry**: See [DEPLOYMENT.md](DEPLOYMENT.md)
3. **Deploy to RunPod**: See [DEPLOYMENT.md](DEPLOYMENT.md)

## Questions?

- Check [README.md](README.md) for general info
- See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment
- Review [QUICKSTART.md](QUICKSTART.md) for quick setup

---

**Remember:** Keep your HF_TOKEN secure and never commit it to version control! 🔒

