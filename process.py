import numpy as np
import cv2


def get_most_frequent_vicinity_value(mat, x, y, xyrange):
    """
    Get the most frequent value in the vicinity of a pixel
    
    Args:
        mat: Input matrix
        x, y: Pixel coordinates
        xyrange: Range to consider around the pixel
        
    Returns:
        Most frequent value in the vicinity
    """
    ymax, xmax = mat.shape
    vicinity_values = mat[max(y - xyrange, 0):min(y + xyrange, ymax),
                          max(x - xyrange, 0):min(x + xyrange, xmax)].flatten()
    counts = np.bincount(vicinity_values)

    return np.argmax(counts)


def smoothen(mat, filter_size=4):
    """
    Smoothen the image by replacing each pixel with the most frequent value in its vicinity
    
    Args:
        mat: Input matrix
        filter_size: Size of the filter to apply
        
    Returns:
        Smoothened matrix
    """
    ymax, xmax = mat.shape
    flat_mat = np.array([
        get_most_frequent_vicinity_value(mat, x, y, filter_size)
        for y in range(0, ymax)
        for x in range(0, xmax)
    ])

    return flat_mat.reshape(mat.shape)


def are_neighbors_same(mat, x, y):
    """
    Check if the neighbors of a pixel have the same value
    
    Args:
        mat: Input matrix
        x, y: Pixel coordinates
        
    Returns:
        True if all neighbors have the same value, False otherwise
    """
    width = len(mat[0])
    height = len(mat)
    val = mat[y][x]
    xRel = [1, 0]
    yRel = [0, 1]
    for i in range(0, len(xRel)):
        xx = x + xRel[i]
        yy = y + yRel[i]
        if xx >= 0 and xx < width and yy >= 0 and yy < height:
            if (mat[yy][xx] != val).all():
                return False
    return True


def outline(mat):
    """
    Create an outline image showing the edges between different colors
    
    Args:
        mat: Input matrix (image)
        
    Returns:
        Outline image (binary)
    """
    ymax, xmax, _ = mat.shape
    line_mat = np.array([
        255 if are_neighbors_same(mat, x, y) else 0
        for y in range(0, ymax)
        for x in range(0, xmax)
    ],
                        dtype=np.uint8)

    return line_mat.reshape((ymax, xmax))


def blur_image(image, blur_d=5):
    """
    Apply bilateral filter to smooth the image while preserving edges
    
    Args:
        image: Input image
        blur_d: Diameter of each pixel neighborhood
        
    Returns:
        Blurred image
    """
    return cv2.bilateralFilter(image, d=blur_d, sigmaColor=200, sigmaSpace=200) 