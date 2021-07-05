import numpy as np


def error_diffusion(img: np.ndarray, kernel: np.ndarray = None) -> np.ndarray:
    """
    Halftone using error diffusion method.

    :param img: 2D/3D numpy array of image (2D for gray and 3D for colour images)
    :param kernel: matrix used for error distribution
    :return: 2D/3D numpy array of halftone image
    """
    if kernel is None:
        kernel = np.array([
            [0, 0, 7],
            [3, 5, 1]
        ], dtype=np.float32) / 16  # a kernel suggested by  Floyd and Steinberg
    if len(img.shape) == 3:
        output = []
        for i in range(3):
            output.append(_error_diffusion(img[:, :, i], kernel=kernel))
        return np.dstack(output)
    else:
        return _error_diffusion(img, kernel)


def _error_diffusion(img: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    k_h, k_w = kernel.shape[0], kernel.shape[1]
    h, w = img.shape[0], img.shape[1]
    orig = np.zeros((h + k_h - 1, w + k_w - 1))
    orig[int(k_h/2):h + int(k_h/2), int(k_w/2):w + int(k_w/2)] = img
    output = np.zeros((h + k_h - 1, w + k_w - 1), dtype=np.uint8)
    for x in range(int(k_h/2), h):
        for y in range(int(k_w/2), w):
            is_white = (float(orig[x, y]) / 255) > 0.5
            pixel_color = int(is_white) * 255
            output[x, y] = pixel_color
            err = np.multiply(kernel, pixel_color - float(orig[x, y]))  # calculate error
            orig[x:x+kernel.shape[0], y:y+kernel.shape[1]] -= err  # distribute error based on kernel
    return output[int(k_h/2):h + int(k_h/2), int(k_w/2):w + int(k_w/2)]


def ordered_dithering(img: np.ndarray, kernel: np.ndarray = None) -> np.ndarray:
    """
    Halftone using ordered dithering method

    :param img: 2D/3D numpy array of image (2D for gray and 3D for colour images)
    :param kernel: dithering matrix
    :return: 2D/3D numpy array of halftone image
    """
    if kernel is None:
        kernel = np.array([[0, 32, 8, 40, 2, 34, 10, 42],
              [48, 16, 56, 24, 50, 18, 58, 26],
              [12, 44, 4, 36, 14, 46, 6, 38],
              [60, 28, 52, 20, 62, 30, 54, 22],
              [3, 35, 11, 43, 1, 33, 9, 41],
              [51, 19, 59, 27, 49, 17, 57, 25],
              [15, 47, 7, 39, 13, 45, 5, 37],
              [63, 31, 55, 23, 61, 29, 53, 21]], dtype=np.float32) / 64.0
    if len(img.shape) == 3:
        output = []
        for i in range(img.shape[2]):
            output.append(_ordered_dithering(img[:, :, i], kernel=kernel))
        return np.dstack(output)
    else:
        return _ordered_dithering(img, kernel)


def _ordered_dithering(img: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    k_h, k_w = kernel.shape[0], kernel.shape[1]
    h, w = img.shape[0], img.shape[1]
    orig = np.zeros((h + (h % k_h), w + (w % k_w)))
    output = np.zeros((h + (h % k_h), w + (w % k_w)), dtype=np.uint8)
    orig[0:h, 0:w] = np.float32(img) / 255.0
    for x in range(0, orig.shape[0], k_h):
        x_shape = k_h if x+k_h < orig.shape[0] else orig.shape[0] - x
        for y in range(0, orig.shape[1], k_w):
            y_shape = k_w if y + k_w < orig.shape[1] else orig.shape[1] - y
            mask = np.zeros((x_shape, y_shape))
            mask[orig[x:x+x_shape, y:y+y_shape] > kernel[0:x_shape, 0:y_shape]] = 255
            output[x:x+x_shape, y:y+y_shape] = mask
    return output[0:h, 0:w]
