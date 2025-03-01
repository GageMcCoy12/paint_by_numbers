import numpy as np
from sklearn.cluster import KMeans
from collections import Counter

import .image_utils


def get_dominant_colors(image, n_clusters=10, use_gpu=False, plot=True):
    """
    Get dominant colors using KMeans clustering
    
    Args:
        image: Input image (numpy array)
        n_clusters: Number of clusters (colors)
        use_gpu: Whether to use GPU acceleration (ignored, always uses CPU)
        plot: Whether to create a color bar image
        
    Returns:
        Tuple of (centroids, labels, bar_image) if plot=True, else (centroids, labels)
    """
    # Must pass FP32 data to kmeans since scikit-learn works better with float data
    flat_image = image.reshape(
        (image.shape[0] * image.shape[1], 3)).astype(np.float32)

    # Always use CPU version with scikit-learn
    clt = KMeans(n_clusters=n_clusters, n_init=10)
    clt.fit(flat_image)
    centroids = clt.cluster_centers_.astype(np.uint8)
    labels = clt.labels_.astype(np.uint8)

    if plot:
        counts = Counter(labels).most_common()
        centroid_size_tuples = [
            (centroids[k], val / len(labels)) for k, val in counts
        ]
        bar_image = image_utils.bar_colors(centroid_size_tuples)
        return centroids, labels, bar_image

    return centroids, labels 
