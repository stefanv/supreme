"""From each of a sequence of images, crop a sub-image of given size.

"""

from optparse import OptionParser
import scikits.image.io as sio

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from math import floor

usage = "%prog [options] file1 file2 ..."
parser = OptionParser(usage=usage)
parser.add_option('-s', '--size', type=str,
                  help='Size of cropped sub image, e.g. "100x200"')
parser.set_defaults(size="100x100")

(options, args) = parser.parse_args()

SIZE = [int(v) for v in options.size.split('x')]

def crop_factory(canvas):

    def crop(event):
        if event.key != 'c': return
        fn = canvas.name + "_crop.png"
        h, w = canvas.patch_size
        sio.imsave(fn, canvas.img[canvas.y:canvas.y + h, canvas.x:canvas.x + w])
        print "Written cropped image to %s." % fn

    return crop

def set_roi_factory(canvas):

    def set_roi(event):
        canvas.x = floor(event.xdata)
        canvas.y = floor(event.ydata)
        canvas.paint()

    return set_roi

class Canvas(object):
    def __init__(self, img, name='misc', patch_size=(100, 100),
                 axes=None):
        """

        Parameters
        ----------
        img : 2-D ndarray
            Image to crop from.
        name : str
            Basename of output files for images cropped from this canvas.
        patch_size : tuple of ints
            Size of the patch to crop (rows, cols).
        axes : matplotlib axes object
            Axes on which to draw the patch.

        """
        self.name = name
        self.img = img
        self.x = 0
        self.y = 0
        self.patch_size = patch_size
        h, w = self.patch_size
        self.patch = Rectangle((self.x, self.y), h, w, alpha=0.3)
        self.axes = axes
        axes.add_patch(self.patch)

    def paint(self):
        self.patch.set_x(self.x)
        self.patch.set_y(self.y)

        # This is probably not the right call.  Should call redraw on canvas?
        plt.draw()

for fn in args:
    try:
        img = sio.imread(fn, as_grey=True)/255.
    except IOError:
        print "Could not open file '%s'." % fn
        continue

    plt.imshow(img, cmap=plt.cm.gray)
    c = Canvas(name=('.'.join(fn.split('.')[:-1]).split('/')[-1]),
               img=img,
               patch_size=SIZE,
               axes=plt.gca())

    plt.title('Click anywhere to move the region of interest. Press any "c" '
              'to crop.')
    plt.connect('key_press_event', crop_factory(c))
    plt.connect('button_press_event', set_roi_factory(c))
    plt.show()


