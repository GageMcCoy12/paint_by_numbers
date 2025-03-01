# Paint by Numbers Generator v2

This Appwrite function converts an image into a paint-by-numbers style image using the algorithm from [PaintingByNumbersIFY](https://github.com/CoderHam/PaintingByNumbersIFY).

## Input

The function expects a JSON payload with the following structure:

```json
{
  "image": "base64_encoded_image_string",
  "numColors": 15,
  "includeOutline": true
}
```

- `image`: A base64-encoded string of the image to convert
- `numColors`: (Optional) The number of colors to use in the paint-by-numbers image (default: 15)
- `includeOutline`: (Optional) Whether to include the outline image in the response (default: true)

## Output

The function returns a JSON response with the following structure:

```json
{
  "success": true,
  "image": "base64_encoded_combined_image",
  "plainImage": "base64_encoded_plain_image",
  "outlineImage": "base64_encoded_outline_image",
  "paletteImage": "base64_encoded_palette_image"
}
```

- `image`: The main paint-by-numbers image with outlines
- `plainImage`: The paint-by-numbers image without outlines
- `outlineImage`: Just the outlines
- `paletteImage`: Color palette used in the image

Or in case of an error:

```json
{
  "success": false,
  "message": "Error message"
}
```

## How It Works

1. The function decodes the base64 image
2. Applies bilateral filtering to smooth the image while preserving edges
3. Uses K-means clustering to reduce the number of colors
4. Smoothens the image by replacing each pixel with the most frequent value in its vicinity
5. Creates outlines between different color regions
6. Returns the paint-by-numbers image as a base64-encoded string

## Dependencies

- numpy
- opencv-python-headless
- scikit-learn
- Pillow 

## Testing Tools

This function comes with two testing tools to help you test the paint-by-numbers functionality:

### run_test.py

A Python script that allows you to test the function in three different modes:

1. **Local Mode**: Tests the function locally using the `index.py` file directly
2. **Console Mode**: Prepares a JSON payload for testing in the Appwrite console
3. **API Mode**: Tests the function via the Appwrite API

Usage:
```bash
# Interactive mode (recommended for first-time users)
python run_test.py

# Command-line mode
python run_test.py --mode local --image test_image.jpg --colors 8
python run_test.py --mode console --image test_image.jpg --colors 12
python run_test.py --mode api --image test_image.jpg --colors 10 --project-id YOUR_PROJECT_ID --function-id YOUR_FUNCTION_ID --api-key YOUR_API_KEY
```

### run_all.sh

A shell script that provides an interactive menu to run the test script with different options:

1. Run local test
2. Prepare console test payload
3. Run API test

Usage:
```bash
# Make sure the script is executable
chmod +x run_all.sh

# Run the script
./run_all.sh
```

The script automatically:
- Creates a virtual environment if it doesn't exist
- Activates the virtual environment
- Installs required packages
- Runs the selected test mode

## Deployment

For deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md). 