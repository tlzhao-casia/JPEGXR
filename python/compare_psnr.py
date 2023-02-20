import argparse
import utils

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--img1', type = str, default = None,
                        help = 'The first image.')
    parser.add_argument('--img2', type = str, default = None,
                        help = 'The second image.')
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    import cv2

    args = parse_args()
    assert (args.img1 is not None and args.img2 is not None)

    img1 = cv2.imread(args.img1)
    img2 = cv2.imread(args.img2)

    psnr = utils.psnr(img1, img2)

    print('The PSNR of the image: {} and image {} is {:.2f}'.format(
            args.img1, args.img2, psnr
        ))
