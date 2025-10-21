#!/usr/bin/env node
/**
 * Node.js example for using the FLUX Custom Faces RunPod Worker
 */

const axios = require('axios');
const fs = require('fs').promises;

class FluxCustomFacesClient {
  /**
   * Initialize the client
   * @param {string} endpointId - Your RunPod endpoint ID
   * @param {string} apiKey - Your RunPod API key
   */
  constructor(endpointId, apiKey) {
    this.endpointId = endpointId;
    this.apiKey = apiKey;
    this.baseUrl = `https://api.runpod.ai/v2/${endpointId}`;
    this.headers = {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    };
  }

  /**
   * Generate image synchronously (waits for completion)
   * @param {Object} params - Generation parameters
   * @returns {Promise<Object>} Response from RunPod
   */
  async generateSync(params) {
    const url = `${this.baseUrl}/runsync`;
    const payload = { input: params };

    try {
      const response = await axios.post(url, payload, { headers: this.headers });
      return response.data;
    } catch (error) {
      throw new Error(`Generation failed: ${error.message}`);
    }
  }

  /**
   * Generate image asynchronously (returns job ID immediately)
   * @param {Object} params - Generation parameters
   * @returns {Promise<Object>} Job information with ID
   */
  async generateAsync(params) {
    const url = `${this.baseUrl}/run`;
    const payload = { input: params };

    try {
      const response = await axios.post(url, payload, { headers: this.headers });
      return response.data;
    } catch (error) {
      throw new Error(`Failed to start generation: ${error.message}`);
    }
  }

  /**
   * Check status of async job
   * @param {string} jobId - Job ID from generateAsync()
   * @returns {Promise<Object>} Job status and results if completed
   */
  async checkStatus(jobId) {
    const url = `${this.baseUrl}/status/${jobId}`;

    try {
      const response = await axios.get(url, { headers: this.headers });
      return response.data;
    } catch (error) {
      throw new Error(`Failed to check status: ${error.message}`);
    }
  }

  /**
   * Cancel a running job
   * @param {string} jobId - Job ID to cancel
   * @returns {Promise<Object>} Cancellation response
   */
  async cancelJob(jobId) {
    const url = `${this.baseUrl}/cancel/${jobId}`;

    try {
      const response = await axios.post(url, {}, { headers: this.headers });
      return response.data;
    } catch (error) {
      throw new Error(`Failed to cancel job: ${error.message}`);
    }
  }

  /**
   * Save base64 encoded image to file
   * @param {string} base64String - Base64 string (with or without data URI prefix)
   * @param {string} outputPath - Path to save the image
   */
  static async saveBase64Image(base64String, outputPath) {
    // Remove data URI prefix if present
    if (base64String.startsWith('data:image')) {
      base64String = base64String.split(',')[1];
    }

    // Decode and save
    const imageBuffer = Buffer.from(base64String, 'base64');
    await fs.writeFile(outputPath, imageBuffer);

    console.log(`Image saved to: ${outputPath}`);
  }
}

/**
 * Basic example with minimal configuration
 */
async function exampleBasic() {
  // Configuration from environment variables
  const ENDPOINT_ID = process.env.RUNPOD_ENDPOINT_ID || 'your-endpoint-id';
  const API_KEY = process.env.RUNPOD_API_KEY || 'your-api-key';
  const HF_TOKEN = process.env.HF_TOKEN || 'hf_your_token';

  // Initialize client
  const client = new FluxCustomFacesClient(ENDPOINT_ID, API_KEY);

  try {
    // Generate image
    console.log('Generating image...');
    const result = await client.generateSync({
      prompt: 'Professional portrait of a person, studio lighting',
      hf_token: HF_TOKEN,
      custom_lora_repo: 'ladbhupesh/flux.1-dev-custom-faces'
    });

    // Check result
    if (result.status === 'COMPLETED') {
      console.log('✓ Generation completed!');
      console.log(`  Seed: ${result.output.seed}`);
      console.log(`  Execution time: ${result.executionTime}ms`);

      // Save first image
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const outputPath = `output_${timestamp}.png`;
      await FluxCustomFacesClient.saveBase64Image(
        result.output.images[0],
        outputPath
      );
    } else {
      console.error('✗ Generation failed:', result);
    }
  } catch (error) {
    console.error('Error:', error.message);
  }
}

/**
 * Advanced example with all options
 */
async function exampleAdvanced() {
  const ENDPOINT_ID = process.env.RUNPOD_ENDPOINT_ID;
  const API_KEY = process.env.RUNPOD_API_KEY;
  const HF_TOKEN = process.env.HF_TOKEN;
  const AWS_ACCESS_KEY = process.env.AWS_ACCESS_KEY_ID;
  const AWS_SECRET_KEY = process.env.AWS_SECRET_ACCESS_KEY;
  const S3_BUCKET = process.env.S3_BUCKET;

  const client = new FluxCustomFacesClient(ENDPOINT_ID, API_KEY);

  try {
    console.log('Generating images with advanced options...');
    const result = await client.generateSync({
      prompt: 'Portrait of Bhupesh, professional headshot, studio lighting',
      negative_prompt: 'blurry, low quality, distorted, cartoon',
      height: 1024,
      width: 1024,
      num_inference_steps: 28,
      guidance_scale: 3.5,
      num_images: 2,
      seed: 42,
      hf_token: HF_TOKEN,
      custom_lora_repo: 'ladbhupesh/flux.1-dev-custom-faces',
      custom_lora_weight_name: 'lora.safetensors',
      aws_access_key_id: AWS_ACCESS_KEY,
      aws_secret_access_key: AWS_SECRET_KEY,
      aws_region: 'ap-south-1',
      s3_bucket: S3_BUCKET,
      s3_prefix: 'flux_custom_faces'
    });

    if (result.status === 'COMPLETED') {
      console.log(`✓ Generated ${result.output.num_images} images`);
      console.log(`  Seed: ${result.output.seed}`);
      console.log(`  Execution time: ${result.executionTime}ms`);

      // Save all images
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      for (let idx = 0; idx < result.output.images.length; idx++) {
        const outputPath = `output_${timestamp}_${idx}.png`;
        await FluxCustomFacesClient.saveBase64Image(
          result.output.images[idx],
          outputPath
        );
      }

      // Print S3 URLs if available
      if (result.output.s3_urls) {
        console.log('\nS3 URLs:');
        result.output.s3_urls.forEach(url => console.log(`  - ${url}`));
      }
    } else {
      console.error('✗ Generation failed:', result);
    }
  } catch (error) {
    console.error('Error:', error.message);
  }
}

/**
 * Example using async generation
 */
async function exampleAsync() {
  const ENDPOINT_ID = process.env.RUNPOD_ENDPOINT_ID;
  const API_KEY = process.env.RUNPOD_API_KEY;
  const HF_TOKEN = process.env.HF_TOKEN;

  const client = new FluxCustomFacesClient(ENDPOINT_ID, API_KEY);

  try {
    // Start async generation
    console.log('Starting async generation...');
    const job = await client.generateAsync({
      prompt: 'Portrait of a person, professional lighting',
      hf_token: HF_TOKEN,
      custom_lora_repo: 'ladbhupesh/flux.1-dev-custom-faces'
    });

    const jobId = job.id;
    console.log(`Job ID: ${jobId}`);

    // Poll for completion
    let result;
    while (true) {
      result = await client.checkStatus(jobId);

      if (result.status === 'COMPLETED') {
        console.log('✓ Generation completed!');
        break;
      } else if (result.status === 'FAILED') {
        console.error('✗ Generation failed:', result);
        return;
      } else {
        console.log(`Status: ${result.status}, waiting...`);
        await new Promise(resolve => setTimeout(resolve, 2000));
      }
    }

    // Save result
    if (result.output) {
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const outputPath = `output_${timestamp}.png`;
      await FluxCustomFacesClient.saveBase64Image(
        result.output.images[0],
        outputPath
      );
    }
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// Main execution
if (require.main === module) {
  console.log('='.repeat(60));
  console.log('Basic Example');
  console.log('='.repeat(60));
  exampleBasic().catch(console.error);

  // Uncomment to run other examples:
  // exampleAdvanced().catch(console.error);
  // exampleAsync().catch(console.error);
}

module.exports = FluxCustomFacesClient;

