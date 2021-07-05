# Visual secret sharing
Implementation of algorithms for Visual secret sharing with 2 shares. It supports binary images, gray images and colour images.
It implements encryption of the image and decryption of the shares.

## Install
Download whl file and install it using `pip install VisualSecretSharing-0.0.1-py3-none-any.whl`

## Test
To run tests launch `pytest` from root directory

## Build
Build project with `python setup.py bdist_wheel`. You can then install it with `pip install dist\VisualSecretSharing-0.0.1-py3-none-any.whl`

## Run as CLI
Run the main program with `python -m VisualSecretSharing -h` for additional information on how to encrypt and decrypt images.

## Use as library
To use project as a library install it and then import it into your python script like `import VisualSecretSharing as vss `