import numpy as np
import cv2

import .dominant_cluster
import .image_utils
import .process


def simple_matrix_to_image(mat, palette):
    simple_mat_flat = np.array(
        [[col for col in palette[index]] for index in mat.flatten()])
    return simple_mat_flat.reshape(mat.shape + (3,))


def PBNify(image, clusters=20, pre_blur=True):
    """
    Convert an image to a paint-by-numbers style image
    
    Args:
        image: Input image (numpy array)
        clusters: Number of color clusters to use
        pre_blur: Whether to apply blur preprocessing
        
    Returns:
        Tuple of (pbn_image, outline_image, combined_image, palette_image)
    """
    # Resize image if too large
    h, w = image.shape[:2]
    max_dim = 1024
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        new_h, new_w = int(h * scale), int(w * scale)
        image = cv2.resize(image, (new_w, new_h))
    
    # Apply blur if requested
    if pre_blur:
        image = process.blur_image(image)

    # Get dominant colors - use CPU version
    dominant_colors, quantized_labels, bar_image = dominant_cluster.get_dominant_colors(
        image, n_clusters=clusters, use_gpu=False, plot=True)

    # Create final PBN image
    smooth_labels = process.smoothen(quantized_labels.reshape(image.shape[:-1]))
    pbn_image = dominant_colors[smooth_labels].reshape(image.shape)

    # Create outline image
    outline_image = process.outline(pbn_image)
    
    # Create combined image with outlines
    combined_image = pbn_image.copy()
    # Make the outlines black
    for y in range(outline_image.shape[0]):
        for x in range(outline_image.shape[1]):
            if outline_image[y, x] == 0:
                combined_image[y, x] = [0, 0, 0]

    return pbn_image, outline_image, combined_image, bar_image 
