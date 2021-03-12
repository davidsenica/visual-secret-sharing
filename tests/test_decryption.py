import VisualSecretSharing as vss
from PIL import Image
import numpy as np


def test_binary():
    decrypted = vss.decrypt_black_white('tests/images/lena-gray-1.png', 'tests/images/lena-gray-2.png')
    expected = np.asarray(Image.open('tests/images/decrypted-lena-gray.png').convert('L'))
    np.testing.assert_array_equal(decrypted, expected)


def test_colour():
    decrypted = vss.decrypt_colour('tests/images/lena-1.png', 'tests/images/lena-2.png')
    expected = np.asarray(Image.open('tests/images/decrypted-lena.png'))
    np.testing.assert_array_equal(decrypted, expected)
