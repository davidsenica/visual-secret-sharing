import VisualSecretSharing as vss
from PIL import Image
import argparse


def encrypt_binary(image: str, output_dir: str = None):
    e1, e2 = vss.binary_image(image)
    tokens = image.split('.')
    if output_dir:
        output = output_dir + tokens[-2].split('/')[-1]
    else:
        output = '.'.join(tokens[:-1])
    print(output)
    Image.fromarray(e1, 'L').save(output + "-1." + tokens[-1])
    Image.fromarray(e2, 'L').save(output + "-2." + tokens[-1])


def encrypt_gray(image: str, output_dir: str = None):
    e1, e2 = vss.gray_image(image)
    tokens = image.split('.')
    if output_dir:
        output = output_dir + tokens[-2].split('/')[-1]
    else:
        output = '.'.join(tokens[:-1])
    Image.fromarray(e1, 'L').save(output + "-1." + tokens[-1])
    Image.fromarray(e2, 'L').save(output + "-2." + tokens[-1])


def encrypt_colour(image: str, output_dir: str = None):
    e1, e2 = vss.colour_image(image)
    i1 = Image.fromarray(e1, 'RGB')
    i2 = Image.fromarray(e2, 'RGB')
    tokens = image.split('.')
    if output_dir:
        output = output_dir + tokens[-2].split('/')[-1]
    else:
        output = '.'.join(tokens[:-1])
    i1.save(output + "-1.png")
    i2.save(output + "-2.png")


def main():
    parser = argparse.ArgumentParser(description='Visual secret sharing: encryption and decryption of images')
    parser.add_argument('-e', '--encrypt', choices=['b', 'g', 'c'],
                        help='Encrypt image, choose b for binary image, g for gray and c for colour image')
    parser.add_argument('-d', '--decrypt', choices=['b', 'g', 'c'],
                        help='Decrypt image, choose b for binary image, g for gray and c for colour image')
    parser.add_argument('-o', '--output', action="store", help='Output directory')
    parser.add_argument('image', type=str, nargs="+", help='Image for encryption or shares for decryption. '
                                                           'In case of decryption it takes in two images.')
    args = parser.parse_args()
    if not args.encrypt and not args.decrypt:
        raise Exception('Please choose encryption or decryption')
    output = None
    if args.output:
        output = args.output
        if output[-1] != '/':
            output += '/'
    if args.encrypt == 'b':
        encrypt_binary(args.image[0], output)
    elif args.encrypt == 'g':
        encrypt_gray(args.image[0], output)
    elif args.encrypt == 'c':
        import random
        random.seed(11)
        encrypt_colour(args.image[0], output)
    elif args.decrypt == 'b' or args.decrypt == 'g':
        img = vss.decrypt_black_white(args.image[0], args.image[1])
        Image.fromarray(img, 'L').save(output + 'decrypted.png' if output else 'decrypted.png')
    elif args.decrypt == 'c':
        img = vss.decrypt_colour(args.image[0], args.image[1])
        Image.fromarray(img, 'RGB').save(output + 'decrypted.png' if output else 'decrypted.png')
    else:
        raise Exception('Not valid option')


if __name__ == '__main__':
    main()
