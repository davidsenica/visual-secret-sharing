from PIL import Image
import numpy as np


def decrypt_black_white(image1: str, image2: str) -> np.ndarray:
    """
    Decrypts black and white shares
    :param image1: Location to share 1
    :param image2: Location to share 2
    :return: Decrypted image as numpy array
    """
    img1 = np.asarray(Image.open(image1).convert('L'))
    img2 = np.asarray(Image.open(image2).convert('L'))
    img = np.zeros(img1.shape, dtype=np.uint8)
    img[((img1 == 255) & (img2 == 255))] = 255
    return img


def decrypt_colour(image1: str, image2: str) -> np.ndarray:
    """
    Decrypts colour shares
    :param image1: Location to share 1
    :param image2: Location to share 2
    :return: Decrypted image as numpy array
    """
    img1 = np.asarray(Image.open(image1))
    img2 = np.asarray(Image.open(image2))
    img = np.zeros(img1.shape, dtype=np.uint8)
    img[((img1 == 255) | (img2 == 255))] = 255
    return img
