# Deploying the Paint by Numbers Function to Appwrite

This guide explains how to deploy the improved Paint by Numbers function to your Appwrite project.

## Prerequisites

- Appwrite CLI installed (`npm install -g appwrite-cli`)
- Appwrite CLI logged in to your Appwrite instance (`appwrite login`)
- An Appwrite project created

## Deployment Steps

1. Navigate to the function directory:

```bash
cd appwrite_function/paint_by_numbers_v2
```

2. Deploy the function using the Appwrite CLI:

```bash
appwrite functions create \
  --projectId YOUR_PROJECT_ID \
  --name "Paint by Numbers" \
  --runtime python-3.10 \
  --entrypoint index.py \
  --execute any \
  --timeout 120
```

3. Deploy the function code:

```bash
appwrite functions createDeployment \
  --projectId YOUR_PROJECT_ID \
  --functionId YOUR_FUNCTION_ID \
  --entrypoint index.py \
  --code .
```

4. Activate the deployment:

```bash
appwrite functions updateDeployment \
  --projectId YOUR_PROJECT_ID \
  --functionId YOUR_FUNCTION_ID \
  --deploymentId YOUR_DEPLOYMENT_ID \
  --activate true
```

## Testing the Function

You can test the function using the Appwrite Console:

1. Go to your Appwrite Console
2. Navigate to Functions
3. Select the "Paint by Numbers" function
4. Click on "Execute"
5. Enter a JSON payload with the image data:

```json
{
  "image": "YOUR_BASE64_ENCODED_IMAGE",
  "numColors": 15,
  "includeOutline": true
}
```

6. Click "Execute" and check the response

## Response Format

The function returns a JSON response with the following fields:

```json
{
  "success": true,
  "image": "base64_encoded_combined_image",
  "plainImage": "base64_encoded_plain_image",
  "outlineImage": "base64_encoded_outline_image",
  "paletteImage": "base64_encoded_palette_image"
}
```

## Troubleshooting

- If you encounter memory issues, try reducing the image size or the number of colors
- Check the function logs in the Appwrite Console for detailed error messages
- Ensure all dependencies are correctly installed
- If the function times out, consider increasing the timeout value in the function settings 