#!/bin/bash

###############################################################################
# cURL examples for FLUX Custom Faces RunPod Worker
###############################################################################

# Configuration - Set these environment variables or replace with your values
ENDPOINT_ID="${RUNPOD_ENDPOINT_ID:-your-endpoint-id}"
API_KEY="${RUNPOD_API_KEY:-your-api-key}"
HF_TOKEN="${HF_TOKEN:-hf_your_token}"

# Base URL
BASE_URL="https://api.runpod.ai/v2/${ENDPOINT_ID}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

###############################################################################
# Example 1: Basic Generation (Minimal Parameters)
###############################################################################
basic_example() {
    echo -e "${GREEN}Example 1: Basic Generation${NC}"
    echo "=================================="
    
    curl -X POST "${BASE_URL}/runsync" \
        -H "Authorization: Bearer ${API_KEY}" \
        -H "Content-Type: application/json" \
        -d '{
            "input": {
                "prompt": "Professional portrait of a person, studio lighting",
                "hf_token": "'"${HF_TOKEN}"'",
                "custom_lora_repo": "ladbhupesh/flux.1-dev-custom-faces"
            }
        }' | jq '.'
    
    echo ""
}

###############################################################################
# Example 2: Advanced Generation (All Parameters)
###############################################################################
advanced_example() {
    echo -e "${GREEN}Example 2: Advanced Generation${NC}"
    echo "=================================="
    
    curl -X POST "${BASE_URL}/runsync" \
        -H "Authorization: Bearer ${API_KEY}" \
        -H "Content-Type: application/json" \
        -d '{
            "input": {
                "prompt": "Portrait of Bhupesh, professional headshot, studio lighting",
                "negative_prompt": "blurry, low quality, distorted",
                "height": 1024,
                "width": 1024,
                "num_inference_steps": 28,
                "guidance_scale": 3.5,
                "num_images": 1,
                "seed": 42,
                "hf_token": "'"${HF_TOKEN}"'",
                "custom_lora_repo": "ladbhupesh/flux.1-dev-custom-faces",
                "custom_lora_weight_name": "lora.safetensors"
            }
        }' | jq '.'
    
    echo ""
}

###############################################################################
# Example 3: With S3 Upload
###############################################################################
s3_upload_example() {
    echo -e "${GREEN}Example 3: With S3 Upload${NC}"
    echo "=================================="
    
    # Check for AWS credentials
    if [ -z "${AWS_ACCESS_KEY_ID}" ] || [ -z "${AWS_SECRET_ACCESS_KEY}" ]; then
        echo -e "${YELLOW}Warning: AWS credentials not set. Skipping S3 example.${NC}"
        return
    fi
    
    curl -X POST "${BASE_URL}/runsync" \
        -H "Authorization: Bearer ${API_KEY}" \
        -H "Content-Type: application/json" \
        -d '{
            "input": {
                "prompt": "Professional portrait, studio lighting",
                "hf_token": "'"${HF_TOKEN}"'",
                "custom_lora_repo": "ladbhupesh/flux.1-dev-custom-faces",
                "aws_access_key_id": "'"${AWS_ACCESS_KEY_ID}"'",
                "aws_secret_access_key": "'"${AWS_SECRET_ACCESS_KEY}"'",
                "aws_region": "ap-south-1",
                "s3_bucket": "'"${S3_BUCKET}"'",
                "s3_prefix": "flux_custom_faces"
            }
        }' | jq '.'
    
    echo ""
}

###############################################################################
# Example 4: Async Generation
###############################################################################
async_example() {
    echo -e "${GREEN}Example 4: Async Generation${NC}"
    echo "=================================="
    
    # Start async job
    echo "Starting async job..."
    RESPONSE=$(curl -s -X POST "${BASE_URL}/run" \
        -H "Authorization: Bearer ${API_KEY}" \
        -H "Content-Type: application/json" \
        -d '{
            "input": {
                "prompt": "Portrait of a person, professional lighting",
                "hf_token": "'"${HF_TOKEN}"'",
                "custom_lora_repo": "ladbhupesh/flux.1-dev-custom-faces"
            }
        }')
    
    JOB_ID=$(echo "$RESPONSE" | jq -r '.id')
    echo "Job ID: $JOB_ID"
    echo ""
    
    # Poll for completion
    echo "Polling for completion..."
    while true; do
        STATUS_RESPONSE=$(curl -s -X GET "${BASE_URL}/status/${JOB_ID}" \
            -H "Authorization: Bearer ${API_KEY}")
        
        STATUS=$(echo "$STATUS_RESPONSE" | jq -r '.status')
        
        if [ "$STATUS" == "COMPLETED" ]; then
            echo -e "${GREEN}✓ Generation completed!${NC}"
            echo "$STATUS_RESPONSE" | jq '.'
            break
        elif [ "$STATUS" == "FAILED" ]; then
            echo -e "${RED}✗ Generation failed${NC}"
            echo "$STATUS_RESPONSE" | jq '.'
            break
        else
            echo "Status: $STATUS, waiting..."
            sleep 2
        fi
    done
    
    echo ""
}

###############################################################################
# Example 5: Multiple Images
###############################################################################
multiple_images_example() {
    echo -e "${GREEN}Example 5: Generate Multiple Images${NC}"
    echo "======================================="
    
    curl -X POST "${BASE_URL}/runsync" \
        -H "Authorization: Bearer ${API_KEY}" \
        -H "Content-Type: application/json" \
        -d '{
            "input": {
                "prompt": "Portrait of a person, professional lighting",
                "num_images": 2,
                "seed": 42,
                "hf_token": "'"${HF_TOKEN}"'",
                "custom_lora_repo": "ladbhupesh/flux.1-dev-custom-faces"
            }
        }' | jq '.'
    
    echo ""
}

###############################################################################
# Example 6: Save Image to File
###############################################################################
save_image_example() {
    echo -e "${GREEN}Example 6: Save Image to File${NC}"
    echo "=================================="
    
    # Generate image
    RESPONSE=$(curl -s -X POST "${BASE_URL}/runsync" \
        -H "Authorization: Bearer ${API_KEY}" \
        -H "Content-Type: application/json" \
        -d '{
            "input": {
                "prompt": "Portrait of a person, professional lighting",
                "hf_token": "'"${HF_TOKEN}"'",
                "custom_lora_repo": "ladbhupesh/flux.1-dev-custom-faces"
            }
        }')
    
    # Extract base64 image
    BASE64_IMAGE=$(echo "$RESPONSE" | jq -r '.output.images[0]' | cut -d',' -f2)
    
    # Save to file
    OUTPUT_FILE="output_$(date +%Y%m%d_%H%M%S).png"
    echo "$BASE64_IMAGE" | base64 -d > "$OUTPUT_FILE"
    
    echo -e "${GREEN}✓ Image saved to: $OUTPUT_FILE${NC}"
    echo ""
}

###############################################################################
# Main Menu
###############################################################################
show_menu() {
    echo ""
    echo "FLUX Custom Faces RunPod Worker - cURL Examples"
    echo "================================================"
    echo ""
    echo "1) Basic Generation"
    echo "2) Advanced Generation"
    echo "3) With S3 Upload"
    echo "4) Async Generation"
    echo "5) Multiple Images"
    echo "6) Save Image to File"
    echo "7) Run All Examples"
    echo "0) Exit"
    echo ""
}

run_all() {
    basic_example
    advanced_example
    s3_upload_example
    async_example
    multiple_images_example
    save_image_example
}

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}Warning: 'jq' is not installed. Output will not be formatted.${NC}"
    echo "Install jq: apt-get install jq (Ubuntu) or brew install jq (macOS)"
    echo ""
fi

# Check configuration
if [ "$ENDPOINT_ID" == "your-endpoint-id" ] || [ "$API_KEY" == "your-api-key" ]; then
    echo -e "${RED}Error: Please set RUNPOD_ENDPOINT_ID and RUNPOD_API_KEY environment variables${NC}"
    echo ""
    echo "Example:"
    echo "  export RUNPOD_ENDPOINT_ID='your-endpoint-id'"
    echo "  export RUNPOD_API_KEY='your-api-key'"
    echo "  export HF_TOKEN='hf_your_token'"
    echo ""
    exit 1
fi

# Run based on argument or show menu
if [ $# -eq 0 ]; then
    # Interactive mode
    while true; do
        show_menu
        read -p "Select an option: " choice
        case $choice in
            1) basic_example ;;
            2) advanced_example ;;
            3) s3_upload_example ;;
            4) async_example ;;
            5) multiple_images_example ;;
            6) save_image_example ;;
            7) run_all ;;
            0) echo "Goodbye!"; exit 0 ;;
            *) echo -e "${RED}Invalid option${NC}" ;;
        esac
    done
else
    # Command line argument mode
    case $1 in
        basic) basic_example ;;
        advanced) advanced_example ;;
        s3) s3_upload_example ;;
        async) async_example ;;
        multiple) multiple_images_example ;;
        save) save_image_example ;;
        all) run_all ;;
        *) echo "Usage: $0 [basic|advanced|s3|async|multiple|save|all]" ;;
    esac
fi

