import VisualSecretSharing as vss
from PIL import Image
import numpy as np


def test_gray_dithering():
    original = np.asarray(Image.open('tests/images/lena-gray.png').convert('L'))
    expected = np.asarray(Image.open('tests/images/lena-gray-dithering.png').convert('L'))
    halftone = vss.ordered_dithering(original)
    np.testing.assert_array_equal(expected, halftone)


def test_gray_diffusion():
    original = np.asarray(Image.open('tests/images/lena-gray.png').convert('L'))
    expected = np.asarray(Image.open('tests/images/lena-gray-diffusion.png').convert('L'))
    halftone = vss.error_diffusion(original)
    np.testing.assert_array_equal(expected, halftone)


def test_dithering():
    original = np.asarray(Image.open('tests/images/lena.png'))
    expected = np.asarray(Image.open('tests/images/lena-colour-dithering.png'))
    halftone = vss.ordered_dithering(original)
    np.testing.assert_array_equal(expected, halftone)


def test_diffusion():
    original = np.asarray(Image.open('tests/images/lena.png'))
    expected = np.asarray(Image.open('tests/images/lena-colour-diffusion.png'))
    halftone = vss.error_diffusion(original)
    np.testing.assert_array_equal(expected, halftone)
