import numpy as np

def psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)

    if mse == 0: mse = 1e-10

    return 10 * np.log10(255 ** 2 / mse)
