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