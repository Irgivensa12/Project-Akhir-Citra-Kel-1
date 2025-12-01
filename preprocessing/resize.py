from PIL import Image

def resize_image(img, size=(299, 299)):
    """
    Melakukan resize gambar ke ukuran yang ditentukan.
    img  : PIL Image
    size : tuple (width, height)
    """
    return img.resize(size)