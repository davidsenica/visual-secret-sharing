from PIL import Image
import numpy as np


def decrypt_black_white(image1, image2):
    img1 = np.asarray(Image.open(image1).convert('L'))
    img2 = np.asarray(Image.open(image2).convert('L'))
    img = np.zeros(img1.shape, dtype=np.int8)
    img[((img1 == 255) & (img2 == 255))] = 255
    Image.fromarray(img, 'L').save('decrypted.png')


def decrypt_colour(image1, image2):
    img1 = np.asarray(Image.open(image1))
    img2 = np.asarray(Image.open(image2))
    img = np.zeros(img1.shape, dtype=np.int8)
    img[((img1 == 255) | (img2 == 255))] = 255
    Image.fromarray(img.astype(np.int8), 'RGB').save('decrypted.png')
