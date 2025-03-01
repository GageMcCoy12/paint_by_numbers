import os
import json
import base64
import numpy as np
from PIL import Image
from io import BytesIO
import cv2
from typing import Dict, Any

# Import the repository modules
from pbnify import PBNify
from image_utils import save_image_to_base64, load_image_from_base64, bar_colors

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
        print(f"Raw body content: {body_str}")
        
        # Parse the JSON string - handle Appwrite's quirky string handling
        try:
            # Try multiple approaches to parse the body
            body_data = None
            
            # Approach 1: Direct JSON parsing
            try:
                body_data = json.loads(body_str)
                print("Parsed using direct JSON loading")
            except json.JSONDecodeError:
                pass
                
            # Approach 2: Handle string-encoded JSON
            if body_data is None:
                try:
                    # Remove any escape characters that might be causing issues
                    cleaned_str = body_str.replace('\\', '').replace('"{', '{').replace('}"', '}')
                    body_data = json.loads(cleaned_str)
                    print("Parsed using cleaned string approach")
                except json.JSONDecodeError:
                    pass
            
            # Approach 3: Try parsing as a raw string
            if body_data is None:
                try:
                    # Sometimes Appwrite sends the body as a raw string without quotes
                    body_data = {}
                    # Extract image using regex pattern matching
                    import re
                    image_match = re.search(r'"image"\s*:\s*"([^"]+)"', body_str)
                    if image_match:
                        body_data['image'] = image_match.group(1)
                        
                    # Extract numColors
                    num_colors_match = re.search(r'"numColors"\s*:\s*(\d+)', body_str)
                    if num_colors_match:
                        body_data['numColors'] = int(num_colors_match.group(1))
                    
                    # Extract includeOutline
                    include_outline_match = re.search(r'"includeOutline"\s*:\s*(true|false)', body_str)
                    if include_outline_match:
                        body_data['includeOutline'] = include_outline_match.group(1).lower() == 'true'
                        
                    print("Parsed using regex pattern matching")
                except Exception as e:
                    print(f"Regex parsing failed: {str(e)}")
                    
            # If we still couldn't parse the body, raise an error
            if body_data is None:
                raise ValueError("Could not parse request body using any method")
                
            print(f"Parsed body data: {body_data}")
            
            base64_image = body_data.get('image')
            num_colors = body_data.get('numColors', 15)  # Default to 15 colors if not specified
            include_outline = body_data.get('includeOutline', True)  # Whether to include outline image
            
            print(f"Number of colors: {num_colors}")
            
            if not base64_image:
                return context.res.json({
                    "success": False,
                    "message": "No image provided"
                })
                
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Failed to parse body as JSON: {str(e)}")
            return context.res.json({
                "success": False,
                "message": f"Failed to parse request body: {str(e)}"
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
