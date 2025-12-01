import numpy as np
from PIL import Image

def normalize_image(img):
    """
    Normalisasi piksel dari 0-255 ke 0-1,
    lalu dikembalikan ke format tampilan (0-255) agar bisa dipreview.
    """
    arr = np.array(img).astype("float32") / 255.0
    arr = (arr * 255).astype("uint8")  # restore supaya bisa ditampilkan
    return Image.fromarray(arr)