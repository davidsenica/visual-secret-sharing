import VisualSecretSharing as vss
import random
from PIL import Image
import numpy as np


def test_binary():
    random.seed(10)
    e1, e2 = vss.binary_image('images/bomb.png')
    i1 = np.asarray(Image.open('images/bomb-1.png').convert('L'))
    i2 = np.asarray(Image.open('images/bomb-2.png').convert('L'))
    np.testing.assert_array_equal(e1, i1)
    np.testing.assert_array_equal(e2, i2)


def test_gray():
    random.seed(10)
    e1, e2 = vss.gray_image('images/lena-gray.png')
    i1 = np.asarray(Image.open('images/lena-gray-1.png').convert('L'))
    i2 = np.asarray(Image.open('images/lena-gray-2.png').convert('L'))
    np.testing.assert_array_equal(e1, i1)
    np.testing.assert_array_equal(e2, i2)


def test_colour():
    random.seed(10)
    e1, e2 = vss.colour_image('images/lena.png')
    i1 = np.asarray(Image.open('images/lena-1.png'))
    i2 = np.asarray(Image.open('images/lena-2.png'))
    np.testing.assert_array_equal(e1, i1)
    np.testing.assert_array_equal(e2, i2)
