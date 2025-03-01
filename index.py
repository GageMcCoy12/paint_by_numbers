import os
import json
import base64
import numpy as np
from PIL import Image
from io import BytesIO
import cv2
from typing import Dict, Any

# Import the repository modules
from .pbnify import PBNify
from .image_utils import save_image_to_base64, load_image_from_base64, bar_colors

def main(context):
    """
    Generate a paint-by-numbers image from an input image
    
    Args:
        context: The Appwrite function context containing the request data
        
    Returns:
        A dictionary with the base64-encoded paint-by-numbers image or an error message
    """
    try:
        print("Starting paint-by-numbers conversion")
        
        # Access the request body from the context
        body_str = context.req.body
        print(f"Raw body type: {type(body_str)}")
        print(f"Raw body content length: {len(body_str) if body_str else 0} characters")
        
        # Parse the string payload - format: base64_image|numColors|includeOutline
        try:
            # Split the payload by the pipe character
            if not body_str:
                return context.res.json({
                    "success": False,
                    "message": "No data provided"
                })
                
            parts = body_str.split('|')
            if len(parts) < 1:
                return context.res.json({
                    "success": False,
                    "message": "Invalid payload format"
                })
                
            # Extract the parts
            base64_image = parts[0]
            
            # Get numColors (default to 15 if not provided)
            num_colors = 15
            if len(parts) > 1 and parts[1].isdigit():
                num_colors = int(parts[1])
                
            # Get includeOutline (default to True if not provided)
            include_outline = True
            if len(parts) > 2:
                include_outline = parts[2].lower() == 'true'
                
            print(f"Parsed payload: numColors={num_colors}, includeOutline={include_outline}")
            
            if not base64_image:
                return context.res.json({
                    "success": False,
                    "message": "No image provided"
                })
                
        except Exception as e:
            print(f"Failed to parse payload: {str(e)}")
            return context.res.json({
                "success": False,
                "message": f"Failed to parse payload: {str(e)}"
            })
        
        # Process the image
        try:
            # Load image from base64
            image = load_image_from_base64(base64_image)
            
            if image is None:
                return context.res.json({
                    "success": False,
                    "message": "Failed to decode image"
                })
                
            print(f"Image shape: {image.shape}")
            
            # Convert to paint by numbers using the repository code
            pbn_image, outline_image, combined_image, palette_image = PBNify(
                image, clusters=num_colors, pre_blur=True)
            
            # Convert results back to base64
            pbn_base64 = save_image_to_base64(pbn_image)
            combined_base64 = save_image_to_base64(combined_image)
            palette_base64 = save_image_to_base64(palette_image)
            
            # Convert outline to RGB for consistent encoding
            outline_rgb = cv2.cvtColor(outline_image, cv2.COLOR_GRAY2RGB)
            outline_base64 = save_image_to_base64(outline_rgb)
            
            print("Successfully created paint-by-numbers image")
            
            # Return the result
            return context.res.json({
                "success": True,
                "image": combined_base64,  # The main PBN image with outlines
                "plainImage": pbn_base64,  # The PBN image without outlines
                "outlineImage": outline_base64,  # Just the outlines
                "paletteImage": palette_base64  # Color palette used
            })
            
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            import traceback
            traceback.print_exc()
            return context.res.json({
                "success": False,
                "message": f"Error processing image: {str(e)}"
            })
            
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return context.res.json({
            "success": False,
            "message": f"Unexpected error: {str(e)}"
        }) 
