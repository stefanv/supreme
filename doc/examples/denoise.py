import numpy as np
import os

import matplotlib.pyplot as plt

from supreme.io import imread
from supreme.noise import dwt_denoise

import demo_data

X = demo_data.chelsea()

X_ = X + np.random.random(X.shape) * 150
X_ /= X_.max()

Y = np.clip(dwt_denoise(X_, alpha=0.02), 0, 255)
Y /= Y.max()

plt.subplot(2, 2, 1)
plt.imshow(X)
plt.title('Input Image')

plt.subplot(2, 2, 2)
plt.imshow(X_)
plt.title('Severe Noise Added')

plt.subplot(2, 2, 3)
plt.imshow(Y)
plt.title('Wavelet Filtered')

plt.subplot(2, 2, 4)
plt.imshow(X_ - Y)
plt.title('Difference')

plt.show()
