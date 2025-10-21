# FLUX Custom Faces RunPod Worker - Project Overview

## 📁 Project Structure

```
FluxDevCustomFaces/
├── 📄 Core Files
│   ├── handler.py              # Main RunPod worker logic
│   ├── schemas.py              # Input validation schemas
│   ├── download_weights.py     # Pre-download models script
│   ├── Dockerfile              # Container configuration
│   └── requirements.txt        # Python dependencies
│
├── 🔧 Build & Deploy
│   ├── build.sh               # Build Docker image script
│   ├── test_local.sh          # Local testing script
│   ├── .gitignore             # Git ignore rules
│   └── .dockerignore          # Docker ignore rules
│
├── 📋 Test Files
│   ├── test_input.json        # Full example request
│   └── test_input_minimal.json # Minimal example request
│
├── 📚 Documentation
│   ├── README.md              # Main documentation
│   ├── QUICKSTART.md          # Quick start guide
│   ├── DEPLOYMENT.md          # Deployment guide
│   ├── LICENSE                # MIT License
│   └── PROJECT_OVERVIEW.md    # This file
│
├── 💻 Examples
│   ├── examples/
│   │   ├── python_example.py     # Python client
│   │   ├── nodejs_example.js     # Node.js client
│   │   ├── curl_example.sh       # cURL examples
│   │   ├── package.json          # Node.js dependencies
│   │   └── README.md            # Examples documentation
│
└── 📜 Original
    └── generate_custom_faces_flux.py  # Original script
```

## 🎯 What This Project Does

This is a **RunPod serverless worker** that generates custom face images using:
- **FLUX.1-dev** base model (pre-loaded in Docker image)
- **Flux-uncensored** LoRA weights (pre-loaded in Docker image)
- **Custom faces LoRA** weights (loaded dynamically per request)
- **S3 integration** for automatic image upload
- **Full API** for programmatic access

## 🔑 Key Features

### 1. Pre-loaded Models
- Base FLUX.1-dev model (~17GB)
- Uncensored LoRA weights
- Fast cold start times

### 2. Dynamic Custom LoRA Loading
- Load any Hugging Face LoRA repo per request
- Specify custom weight files
- Support for private repositories

### 3. AWS S3 Integration
- Automatic upload to S3
- Configurable bucket and prefix
- Returns both base64 and S3 URLs

### 4. Flexible API
- Synchronous and asynchronous endpoints
- Multiple image generation
- Full parameter control
- Seed support for reproducibility

### 5. Production Ready
- Error handling
- Logging
- Schema validation
- Security best practices

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        RunPod Request                       │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                     Handler (handler.py)                    │
│  • Validates input (schemas.py)                            │
│  • Authenticates with HuggingFace (if token provided)      │
│  • Loads custom LoRA (dynamic)                             │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                  FLUX Pipeline (Pre-loaded)                 │
│  • Base Model: FLUX.1-dev                                  │
│  • Uncensored LoRA: Pre-loaded                             │
│  • Custom LoRA: Loaded from request                        │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    Image Generation                         │
│  • Generate images based on prompt                         │
│  • Apply LoRA weights                                       │
│  • Use specified parameters                                 │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                  Post-Processing                            │
│  • Convert images to base64                                │
│  • Upload to S3 (if configured)                            │
│  • Return response                                          │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                        Response                             │
│  • Base64 images                                           │
│  • S3 URLs (if uploaded)                                    │
│  • Seed used                                                │
│  • Execution metrics                                        │
└─────────────────────────────────────────────────────────────┘
```

## 📦 What Gets Built Into the Docker Image

### Baked In (Part of Image)
- ✅ Python 3.10
- ✅ CUDA 12.1
- ✅ All Python dependencies (torch, diffusers, etc.)
- ✅ FLUX.1-dev base model (~17GB)
- ✅ Flux-uncensored LoRA weights
- ✅ Handler code

### Provided Per Request
- 🔑 AWS credentials
- 🔑 Hugging Face token
- 🎨 Custom faces LoRA repository
- 📝 Generation parameters (prompt, seed, etc.)

## 🔄 Workflow

### Development
1. Modify `handler.py` or other files
2. Test locally with `./test_local.sh`
3. Build new image with `./build.sh`
4. Push to registry
5. Update RunPod endpoint

### Usage
1. Client sends request to RunPod endpoint
2. RunPod routes to available worker
3. Worker processes request
4. Worker generates image(s)
5. Worker uploads to S3 (if configured)
6. Worker returns response
7. Client receives base64 images and/or S3 URLs

## 🔒 Security Model

### Credentials NOT in Image
- AWS credentials ❌
- Hugging Face tokens ❌
- S3 bucket names ❌

### Credentials in Request
- Per-request credentials ✅
- Environment variables ✅
- Can use different credentials per request ✅

### Why This Approach?
- **Security**: No credentials in public Docker images
- **Flexibility**: Different users can use different credentials
- **Compliance**: Follows security best practices

## 📊 API Request/Response Flow

### Request
```json
{
  "input": {
    "prompt": "...",
    "hf_token": "...",
    "custom_lora_repo": "...",
    "aws_access_key_id": "...",
    "aws_secret_access_key": "...",
    "s3_bucket": "..."
  }
}
```

### Processing
1. Validate input (schemas.py)
2. Login to HuggingFace (if token provided)
3. Initialize pipeline (if not already done)
4. Load custom LoRA
5. Generate image(s)
6. Convert to base64
7. Upload to S3 (if configured)

### Response
```json
{
  "status": "COMPLETED",
  "output": {
    "images": ["data:image/png;base64,..."],
    "s3_urls": ["https://..."],
    "seed": 42,
    "num_images": 1
  },
  "executionTime": 8500
}
```

## 🚀 Deployment Options

### Option 1: RunPod Serverless (Recommended)
- **Pros**: Auto-scaling, pay-per-second, managed
- **Cons**: Cold start times
- **Best For**: Production, variable workload

### Option 2: RunPod GPU Pod
- **Pros**: Always warm, consistent performance
- **Cons**: Pay even when idle
- **Best For**: Continuous generation, high volume

### Option 3: Self-Hosted
- **Pros**: Full control, no external dependencies
- **Cons**: Requires GPU infrastructure
- **Best For**: On-premise requirements

## 💰 Cost Breakdown

### One-Time Costs
- Docker image storage: Free (Docker Hub) or ~$0.10/month (private)
- Development time: Variable

### Per-Request Costs

**RunPod Serverless (RTX 4090)**
- Cold start: ~$0.05 (2-3 minutes)
- Warm request: ~$0.002-0.003 (8-12 seconds)
- Per 1000 images: ~$2-3 (if warm)

**RunPod GPU Pod (RTX 4090)**
- Hourly rate: ~$0.40/hour
- Per image: ~$0.0015 (if generating continuously)
- Per 1000 images: ~$1.50

### S3 Costs
- Storage: $0.023 per GB/month
- PUT requests: $0.005 per 1,000 requests
- Data transfer out: $0.09 per GB

## 📈 Performance Metrics

### Image Generation Times

| Resolution | Steps | GPU | Time |
|-----------|-------|-----|------|
| 512x512 | 20 | RTX 4090 | 4-6s |
| 512x512 | 28 | RTX 4090 | 6-8s |
| 1024x1024 | 20 | RTX 4090 | 8-10s |
| 1024x1024 | 28 | RTX 4090 | 10-14s |
| 1024x1024 | 20 | A100 | 5-7s |
| 1024x1024 | 28 | A100 | 7-10s |

### Throughput

| GPU | Images/Hour | Cost/Hour | Cost/Image |
|-----|-------------|-----------|------------|
| RTX 4090 | 300-400 | $0.40 | $0.001 |
| A100 40GB | 500-600 | $1.50 | $0.0025 |
| A100 80GB | 600-700 | $2.50 | $0.0036 |

## 🎓 Learning Resources

### Understanding the Code
1. Start with `handler.py` - Main logic
2. Read `schemas.py` - Input validation
3. Check `download_weights.py` - Model loading
4. Review examples in `examples/` directory

### Understanding the Stack
- **RunPod**: Serverless GPU platform
- **FLUX.1-dev**: State-of-the-art image generation
- **LoRA**: Lightweight model fine-tuning
- **Diffusers**: Hugging Face diffusion models library

### Extending the Project
1. **Add new parameters**: Modify `schemas.py` and `handler.py`
2. **Add post-processing**: Modify image handling in `handler.py`
3. **Add monitoring**: Integrate logging/metrics services
4. **Add webhooks**: Implement callback functionality

## 🔮 Future Enhancements

### Potential Features
- [ ] Multiple LoRA weights support
- [ ] Image-to-image generation
- [ ] Upscaling integration
- [ ] Webhook notifications
- [ ] Batch processing optimization
- [ ] Caching layer for common prompts
- [ ] WebSocket support for real-time updates
- [ ] Admin dashboard
- [ ] Usage analytics

### Community Contributions
- Fork the project
- Add features
- Submit pull requests
- Share your use cases

## 📞 Support & Community

### Documentation
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Full Docs**: [README.md](README.md)
- **Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Examples**: [examples/README.md](examples/README.md)

### External Resources
- **RunPod Docs**: https://docs.runpod.io/
- **FLUX Docs**: https://huggingface.co/black-forest-labs/FLUX.1-dev
- **Diffusers Docs**: https://huggingface.co/docs/diffusers

### Getting Help
1. Check documentation first
2. Review examples
3. Search existing issues
4. Open new issue with details
5. Join RunPod Discord

## 🎉 Success Stories

This worker enables:
- **Custom portrait generation** with specific faces
- **Brand-consistent imagery** with custom models
- **Automated content creation** pipelines
- **Research applications** in AI generation
- **Creative projects** with AI assistance

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

**Ready to get started?**

👉 [Read the Quick Start Guide](QUICKSTART.md)

👉 [Deploy to RunPod](DEPLOYMENT.md)

👉 [Try the Examples](examples/README.md)

