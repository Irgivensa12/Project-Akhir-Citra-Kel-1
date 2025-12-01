from PIL import ImageOps

def augment_image(img):
    """
    Melakukan augmentasi sederhana:
    - flip horizontal
    - rotate 25 derajat
    """
    img = ImageOps.mirror(img) # flip secara horizontal
    img = img.rotate(25) # merotasi 25 derajat
    return img