# Supreme module initialisation

import config
import lib
import ext

import geometry
import transform
import register
import feature
import io
import photometry

def iterable(x):
    try:
        iter(x)
    except:
        return False
    else:
        return True

def test_data():
    """Return an image for testing purposes.

    Returns
    -------
    I : ndarray of uint8
        512x512 test image.

    """
    import os
    f = os.path.join(os.path.dirname(__file__),
                     'lib/pywt/demo/data/aero.png')
    return io.imread(f)

def show(*images):
    """Display images on screen.

    """
    import matplotlib.pyplot as plt

    L = len(images)
    for i in range(L):
        plt.subplot(1, L, i + 1)
        plt.imshow(images[i], cmap=plt.cm.gray, interpolation='nearest')

    plt.show()
