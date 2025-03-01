import numpy as np
import cv2
import base64
from PIL import Image
from io import BytesIO


def load_image_from_base64(base64_string):
    """
    Load image from base64 string
    
    Args:
        base64_string: Base64-encoded image string
        
    Returns:
        Image as numpy array (RGB)
    """
    image_data = base64.b64decode(base64_string)
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # Convert from BGR to RGB (OpenCV loads as BGR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def save_image_to_base64(image):
    """
    Save image to base64 string
    
    Args:
        image: Image as numpy array (RGB)
        
    Returns:
        Base64-encoded image string
    """
    # Convert from RGB to BGR for OpenCV
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    _, buffer = cv2.imencode('.png', image)
    return base64.b64encode(buffer).decode('utf-8')


def bar_colors(centroid_size_tuples):
    """
    Create a bar of colors showing the palette
    
    Args:
        centroid_size_tuples: List of (color, percentage) tuples
        
    Returns:
        Color bar image
    """
    bar = np.zeros((50, 300, 3), dtype="uint8")
    x_start = 0
    for (color, percent) in centroid_size_tuples:
        x_end = x_start + (percent * 300)
        cv2.rectangle(bar, (int(x_start), 0), (int(x_end), 50),
                      color.astype("uint8").tolist(), -1)
        x_start = x_end
    return bar 