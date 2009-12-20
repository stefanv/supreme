import sys

import numpy as np

from supreme.io import ImageCollection
from supreme.noise import dwt_denoise

import matplotlib.pyplot as plt

# --------------------------------------
alpha = 2
# --------------------------------------

if len(sys.argv) == 1:
    print "Usage: noise_fingerprint.py file1 file2 file3 ..."

ic = ImageCollection(sys.argv[1:10])

n = []
denoise = []
for i, img in enumerate(ic):
    print "Denoising image %d..." % i

    clean = dwt_denoise(img, wavelet='db8', alpha=alpha, levels=4)

    if i == 0:
        denoise.append(clean)

    n.append(img - clean)

avg = np.zeros(n[0].shape, dtype=float)
for noise in n:
    avg += noise
avg /= len(n)

print "Noise minimum and maximum:", avg.min(), avg.max()

imdata = avg + avg.min()
imdata = imdata / imdata.max()

plt.subplot(2, 2, 1)
plt.imshow(ic[0])
plt.title('Input data, $\\sigma^2 = %.2f$' % np.var(ic[0]))

plt.subplot(2, 2, 2)
plt.imshow(denoise[0] / denoise[0].max())
plt.title('Denoised')

plt.subplot(2, 2, 3)
plt.imshow(imdata)
plt.title('Noise Fingerprint')

Y = np.clip(ic[0] - avg, 0, 255)
denoise_var = np.var(Y)
Y = Y / 255.

plt.subplot(2, 2, 4)
plt.imshow(Y)
plt.title('Fingerprint removed, $\\sigma^2 = %.2f$' % denoise_var)

plt.show()
