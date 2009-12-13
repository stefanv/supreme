import numpy as np

from demo_data import chelsea
from supreme.register.parzen import joint_hist, mutual_info
from supreme.transform import homography

import matplotlib.pyplot as plt

h1 = chelsea(grey=True).astype(np.uint8)
plt.suptitle('Parzen-Window Joint PDF Estimator')

for n, t in enumerate([0, 0.01, 0.1]):
    plt.subplot(1, 3, n + 1)

    h2 = homography(h1, [[np.cos(t), -np.sin(t), 0],
                         [np.sin(t),  np.cos(t), 0],
                         [0,            0,       1]])

    if n == 0:
        plt.ylabel('Grey levels in A')
        plt.xlabel('Grey levels in B')

    H = joint_hist(h1, h2, win_size=5, std=1)
    S = mutual_info(H)

    plt.title('Rotation $%.2f^\\circ$\nS=%.5f' % ((t / np.pi * 180), S))

    plt.imshow(np.log(H + 10), interpolation='nearest')

plt.show()
