import numpy as np
from PIL import Image
import random
from .halftone import ordered_dithering


def binary_image(image: str):
    """
    Function encrypts binary image (image contains only black and only white pixels)

    :param image: Location of the image
    :return:
    """
    img = np.asarray(Image.open(image).convert('L'))
    e1, e2 = _encrypt(img)
    tokens = image.split('.')
    output = '.'.join(tokens[:-1])
    Image.fromarray(e1, 'L').save(output + "-1." + tokens[-1])
    Image.fromarray(e2, 'L').save(output + "-2." + tokens[-1])


def gray_image(image: str, halftone_alg=ordered_dithering, kernel=None, alg='standard'):
    """
    Function encrypts gray image

    :param image: Location of the image
    :param halftone_alg: Algorithm used for halftone
    :param kernel: Kernel passed to halftone algorithm
    :param alg: Algorithm used for encryption: standard (same as binary) or multilevel
    :return:
    """
    if alg != 'standard' or alg != 'multilevel':
        raise Exception
    img = np.asarray(Image.open(image).convert('L'))
    if alg == 'standard':
        e1, e2 = _encrypt(halftone_alg(img, kernel=kernel))
    elif alg == 'multilevel':
        e1, e2 = _multi_level_encoding(img)
    else:
        raise Exception
    tokens = image.split('.')
    output = '.'.join(tokens[:-1])
    Image.fromarray(e1, 'L').save(output + "-1." + tokens[-1])
    Image.fromarray(e2, 'L').save(output + "-2." + tokens[-1])


def colour_image(image: str, halftone_alg=ordered_dithering, kernel=None):
    """
    Function encrypts color images

    :param image: Location of the image
    :param halftone_alg: Algorithm used for halftone
    :param kernel: Kernel passed to halftone algorithm
    :return:
    """
    img = np.asarray(Image.open(image))
    img = halftone_alg(img, kernel=kernel)
    encrypted1 = []
    encrypted2 = []
    cmy = _rgb_cmy(img)
    for i in range(3):
        e1, e2 = _encrypt(cmy[:, :, i], full_pixel=255)
        encrypted1.append(e1)
        encrypted2.append(e2)
    i1 = Image.fromarray(_rgb_cmy(np.stack(encrypted1, axis=2)).astype(np.int8), 'RGB')
    i2 = Image.fromarray(_rgb_cmy(np.stack(encrypted2, axis=2)).astype(np.int8), 'RGB')

    tokens = image.split('.')
    output = '.'.join(tokens[:-1])
    i1.save(output + "-1.png")
    i2.save(output + "-2.png")


def _encrypt(img: np.ndarray, full_pixel: int = 0) -> (np.ndarray, np.ndarray):
    height, width = img.shape

    full_pixel_share1 = [[[0, 255],[255, 0]], [[255, 0], [0, 255]], [[255, 0], [255, 0]], [[0, 255], [0, 255]]]
    full_pixel_share2 = [[[255, 0], [0, 255]], [[0, 255],[255, 0]], [[0, 255], [0, 255]], [[255, 0], [255, 0]]]

    empty_pixel_share1 = [[[0, 255],[255, 0]], [[255, 0], [0, 255]], [[255, 0], [255, 0]], [[0, 255], [0, 255]]]
    empty_pixel_share2 = [[[0, 255],[255, 0]], [[255, 0], [0, 255]], [[255, 0], [255, 0]], [[0, 255], [0, 255]]]

    encrypted1 = np.zeros((height * 2, width * 2), dtype=np.uint8)
    encrypted2 = np.zeros((height * 2, width * 2), dtype=np.uint8)

    for row in range(height):
        for column in range(width):
            if img[row][column] == full_pixel:
                i = random.randint(0, len(full_pixel_share1) - 1)
                share1 = full_pixel_share1[i]
                share2 = full_pixel_share2[i]
            else:
                i = random.randint(0, len(empty_pixel_share1) - 1)
                share1 = empty_pixel_share1[i]
                share2 = empty_pixel_share2[i]
            encrypted1[2 * row: 2 * row + 2, 2 * column: 2 * column + 2] = share1
            encrypted2[2 * row: 2 * row + 2, 2 * column: 2 * column + 2] = share2

    return encrypted1, encrypted2


def _multi_level_encoding(img: np.ndarray) -> (np.ndarray, np.ndarray):
    def _count_white_black(vector):
        black = 0
        white = 0
        for i in vector:
            if i == 255:
                white += 1
            else:
                black += 1
        return black, white
    height, width = img.shape

    M0 = [([0, 0, 255, 255], [0, 0, 255, 255]),
          ([0, 255, 0, 255], [0, 255, 0, 255]),
          ([0, 255, 255, 0], [0, 255, 255, 0]),
          ([255, 0, 0, 255], [255, 0, 0, 255]),
          ([255, 0, 255, 0], [255, 0, 255, 0]),
          ([255, 255, 0, 0], [255, 255, 0, 0])]
    M1 = [([0, 0, 255, 255], [0, 255, 0, 255]),
          ([0, 0, 255, 255], [255, 0, 0, 255]),
          ([255, 255, 0, 0], [0, 255, 255, 0]),
          ([0, 0, 255, 255], [0, 255, 255, 0]),
          ([0, 255, 0, 255], [0, 0, 255, 255]),
          ([0, 255, 0, 255], [255, 0, 0, 255]),
          ([0, 255, 0, 255], [0, 255, 255, 0]),
          ([0, 255, 0, 255], [255, 255, 0, 0]),
          ([255, 255, 0, 0], [255, 0, 0, 255]),
          ([255, 255, 0, 0], [255, 0, 255, 0]),
          ([255, 0, 0, 255], [0, 0, 255, 255])]
    M2 = [([255, 0, 0, 255], [0, 255, 255, 0]),
          ([255, 0, 255, 0], [0, 255, 0, 255]),
          ([255, 255, 0, 0], [0, 0, 255, 255]),
          ([0, 255, 255, 0], [255, 0, 0, 255]),
          ([0, 0, 255, 255], [255, 255, 0, 0]),
          ([0, 255, 0, 255], [255, 0, 255, 0])]

    encrypted1 = np.zeros(img.shape)
    encrypted2 = np.zeros(img.shape)
    for i in range(height):
        for j in range(0, width, 4):
            b, w = _count_white_black(img[i, j:j+4])
            if w == 4 or w == 3:
                m = M0[random.randint(0, len(M0) - 1)]
            elif w == 2:
                m = M1[random.randint(0, len(M1) - 1)]
            else:
                m = M2[random.randint(0, len(M2) - 1)]
            encrypted1[i, j:j + 4] = m[0]
            encrypted2[i, j:j + 4] = m[1]
    return encrypted1, encrypted2


def _rgb_cmy(img: np.ndarray) -> np.ndarray:
    return (np.ones(img.shape, dtype=np.int8) * 255) - img

