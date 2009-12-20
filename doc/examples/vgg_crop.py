"""Load a VGG data-set and stack the images.

"""
import numpy as np
from scipy.misc import imsave

from supreme.io import load_vgg

import os, sys
from optparse import OptionParser

usage = "%prog [options] source_dir target_dir"
parser = OptionParser(usage=usage)
parser.add_option('-c', '--clip-box', dest='clip_box', nargs=4,
                  help='Clipping boundaries: x0, y0, x1, y1')
(options, args) = parser.parse_args()

if len(sys.argv) < 3:
    parser.print_help()
    sys.exit(0)

source_dir = sys.argv[-2]
target_dir = sys.argv[-1]

if os.path.exists(target_dir):
    raise ValueError("Output directory already exists.")

ic = load_vgg(source_dir)

image_dir = os.path.join(target_dir, 'png')
H_dir = os.path.join(target_dir, 'H')
os.mkdir(target_dir)
os.mkdir(image_dir)
os.mkdir(H_dir)

if not options.clip_box:
    x0, y0 = 0, 0
    y1, x1 = ic[0].shape
else:
    x0, y0, x1, y1 = [int(i) for i in options.clip_box]


for n, img in enumerate(ic):
    fn = os.path.join(image_dir, os.path.basename(source_dir) + \
                                 '%03d.png' % n)
    print "Saving %s" % fn
    imsave(fn, img[y0:y1, x0:x1, ...])

    H_tr = np.array([[1, 0, x0],
                     [0, 1, y0],
                     [0, 0, 1]])

    H_tr_I = np.linalg.inv(H_tr)

    if n > 0:
        fn = os.path.join(H_dir, os.path.basename(source_dir) + \
                          '%03d.%03d.H' % (n - 1, n))
        H = img.info['H_rel']

        H = np.dot(H_tr_I, np.dot(H, H_tr))

        print "Saving %s" % fn
        np.savetxt(fn, H)


