# Examples

This directory contains code examples for using the FLUX Custom Faces RunPod Worker in different programming languages.

## Prerequisites

Before running any examples, you need:

1. A deployed RunPod endpoint (see [DEPLOYMENT.md](../DEPLOYMENT.md))
2. Your RunPod API key (from RunPod Dashboard → API Keys)
3. Your endpoint ID
4. A Hugging Face token (for accessing custom LoRA models)

## Setting Up Environment Variables

```bash
# Required
export RUNPOD_ENDPOINT_ID="your-endpoint-id"
export RUNPOD_API_KEY="your-api-key"
export HF_TOKEN="hf_your_token"

# Optional (for S3 upload)
export AWS_ACCESS_KEY_ID="your-aws-key"
export AWS_SECRET_ACCESS_KEY="your-aws-secret"
export S3_BUCKET="your-bucket-name"
```

## Python Example

### Installation

```bash
pip install requests
```

### Usage

```bash
# Run the example
python python_example.py

# Or use as a module
python -c "from python_example import FluxCustomFacesClient; print(FluxCustomFacesClient)"
```

### Features

- Synchronous generation
- Asynchronous generation with polling
- Advanced parameters
- S3 upload
- Base64 image saving

## Node.js Example

### Installation

```bash
cd examples
npm install
```

### Usage

```bash
# Run the example
node nodejs_example.js

# Or use npm script
npm start
```

### Features

- Promise-based API
- Synchronous and asynchronous generation
- Full parameter support
- Image file saving

## cURL Example

### Requirements

- `curl` (usually pre-installed)
- `jq` (for JSON formatting, optional but recommended)

Install jq:
```bash
# Ubuntu/Debian
sudo apt-get install jq

# macOS
brew install jq
```

### Usage

```bash
# Make executable
chmod +x curl_example.sh

# Interactive menu
./curl_example.sh

# Or run specific example
./curl_example.sh basic
./curl_example.sh advanced
./curl_example.sh async
./curl_example.sh all
```

### Available Examples

1. **Basic Generation** - Minimal parameters
2. **Advanced Generation** - All parameters
3. **With S3 Upload** - Upload to AWS S3
4. **Async Generation** - Async with polling
5. **Multiple Images** - Generate multiple images
6. **Save Image to File** - Download and save image

## Quick Start

### Python

```python
from examples.python_example import FluxCustomFacesClient

client = FluxCustomFacesClient(
    endpoint_id="your-endpoint-id",
    api_key="your-api-key"
)

result = client.generate_sync(
    prompt="Portrait of a person, professional lighting",
    hf_token="hf_your_token",
    custom_lora_repo="ladbhupesh/flux.1-dev-custom-faces"
)

print(result)
```

### Node.js

```javascript
const FluxCustomFacesClient = require('./nodejs_example');

const client = new FluxCustomFacesClient(
  'your-endpoint-id',
  'your-api-key'
);

const result = await client.generateSync({
  prompt: 'Portrait of a person, professional lighting',
  hf_token: 'hf_your_token',
  custom_lora_repo: 'ladbhupesh/flux.1-dev-custom-faces'
});

console.log(result);
```

### cURL

```bash
curl -X POST "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "prompt": "Portrait of a person, professional lighting",
      "hf_token": "hf_your_token",
      "custom_lora_repo": "ladbhupesh/flux.1-dev-custom-faces"
    }
  }'
```

## Common Use Cases

### Generate with Custom Parameters

```python
result = client.generate_sync(
    prompt="Professional portrait with studio lighting",
    negative_prompt="blurry, low quality",
    height=1024,
    width=1024,
    num_inference_steps=28,
    guidance_scale=3.5,
    seed=42
)
```

### Upload to S3

```python
result = client.generate_sync(
    prompt="Portrait of a person",
    hf_token="hf_token",
    custom_lora_repo="your/repo",
    aws_access_key_id="your-key",
    aws_secret_access_key="your-secret",
    s3_bucket="your-bucket",
    s3_prefix="images"
)

# S3 URLs will be in result['output']['s3_urls']
```

### Generate Multiple Images

```python
result = client.generate_sync(
    prompt="Portrait of a person",
    num_images=4,
    seed=42  # Same seed for consistency
)

# Access all images
for idx, img in enumerate(result['output']['images']):
    client.save_base64_image(img, f"output_{idx}.png")
```

### Async Generation (for long-running jobs)

```python
# Start generation
job = client.generate_async(prompt="...")
job_id = job['id']

# Check status later
status = client.check_status(job_id)
if status['status'] == 'COMPLETED':
    result = status['output']
```

## Error Handling

### Python

```python
try:
    result = client.generate_sync(...)
except Exception as e:
    print(f"Error: {e}")
```

### Node.js

```javascript
try {
  const result = await client.generateSync(...);
} catch (error) {
  console.error('Error:', error.message);
}
```

## Tips

1. **Use environment variables** for credentials (never hardcode)
2. **Start with basic examples** before moving to advanced
3. **Check execution time** in response to optimize parameters
4. **Use seed parameter** for reproducible results
5. **Generate multiple images** with different seeds to get variations

## Troubleshooting

### "Invalid API key"
- Check that your API key is correct
- Ensure you're using the right endpoint ID

### "Timeout"
- Increase timeout in your HTTP client
- First request takes longer (model compilation)

### "Out of memory"
- Reduce image dimensions
- Reduce number of images
- Use fewer inference steps

### "S3 upload failed"
- Verify AWS credentials
- Check bucket permissions
- Ensure bucket exists

## Support

For issues with the examples:
- Check the main [README.md](../README.md)
- Review [DEPLOYMENT.md](../DEPLOYMENT.md)
- Open an issue on GitHub

