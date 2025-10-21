# RunPod Configuration

This directory contains RunPod-specific configuration files.

## hub.json

The `hub.json` file contains metadata for displaying this worker in the RunPod Hub template marketplace.

### What it includes:

- **Template Information**: Name, description, version, tags
- **Requirements**: GPU, disk, memory specifications
- **Input/Output Schema**: Complete API documentation
- **Examples**: Multiple usage examples
- **Documentation Links**: Links to guides and examples
- **Features & Use Cases**: What the worker can do
- **Optimization Tips**: How to get best performance
- **Troubleshooting**: Common issues and solutions

### Usage

When you publish this worker to RunPod Hub, the platform will read this file to:

1. Display template information in the marketplace
2. Show example inputs and outputs
3. Provide documentation links
4. Display pricing estimates
5. Show GPU requirements

### Publishing to RunPod Hub

1. **Build and push your Docker image**:
   ```bash
   ./build.sh
   docker push yourusername/flux-custom-faces:latest
   ```

2. **Create endpoint in RunPod**:
   - Go to RunPod Dashboard → Serverless
   - Click "New Endpoint"
   - Select "Custom" template
   - Enter your Docker image URL

3. **Submit to RunPod Hub** (optional):
   - Go to RunPod Hub
   - Click "Submit Template"
   - Provide your GitHub repository URL
   - RunPod will read `.runpod/hub.json` automatically

### Customizing

Before publishing, update these fields in `hub.json`:

1. **Container image**:
   ```json
   "container": {
     "image": "yourusername/flux-custom-faces:latest"
   }
   ```

2. **Author information**:
   ```json
   "author": {
     "name": "Your Name",
     "url": "https://github.com/yourusername"
   }
   ```

3. **Links**:
   ```json
   "links": {
     "github": "https://github.com/yourusername/FluxDevCustomFaces",
     "docker_hub": "https://hub.docker.com/r/yourusername/flux-custom-faces"
   }
   ```

4. **Documentation URLs**:
   ```json
   "documentation": {
     "readme_url": "https://github.com/yourusername/FluxDevCustomFaces/blob/main/README.md",
     ...
   }
   ```

### Schema Validation

The input and output schemas in `hub.json` should match your actual implementation in `handler.py` and `schemas.py`.

If you modify the API:
1. Update `schemas.py`
2. Update `handler.py`
3. Update `hub.json` schemas
4. Update examples in `hub.json`

### Testing

Before publishing, validate your `hub.json`:

```bash
# Check JSON syntax
python -m json.tool .runpod/hub.json > /dev/null && echo "Valid JSON" || echo "Invalid JSON"

# Or use jq
jq empty .runpod/hub.json && echo "Valid JSON" || echo "Invalid JSON"
```

### Reference

- **RunPod Documentation**: https://docs.runpod.io/
- **Template Submission**: https://docs.runpod.io/serverless/templates
- **Hub Guidelines**: https://runpod.io/hub

---

**Note**: The `hub.json` file is optional. You can deploy your worker without it, but it's required if you want to share your template on RunPod Hub.

