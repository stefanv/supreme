import numpy as np
import os
from glob import glob
from optparse import OptionParser

from supreme.register.parzen import joint_hist, mutual_info
import supreme.register as register
from supreme.io import imread, imsave

usage = "%prog [options] vgg_dir"
parser = OptionParser(usage=usage)
parser.add_option('-t', action='store_true', dest='translation',
                  default=False, help='Use translation-only model')
parser.add_option('-l', '--levels', type=int,
                  default=2,
                  help='Number of levels to downsample during registration. '
                       '[default: %default]')
parser.add_option('-s', action='store_true', dest='fixed_scale',
                  default=False, help='Fix scale to 1 in motion model.')
(options, args) = parser.parse_args()

import sys
if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(0)

vgg = sys.argv[-1]

if not os.path.isdir(vgg):
    raise RuntimeError("Cannot open VGG directory")

img_dir = [d for d in os.listdir(vgg) if d in ['pgm', 'png', 'jpg']]
if not img_dir:
    raise RuntimeError("Cannot find images inside VGG directory")
img_dir = img_dir[0]

images = [imread(i, flatten=True).astype(np.uint8) for i in
          glob(os.path.join(os.path.join(vgg, img_dir), '*.' + img_dir))]

H_dir = os.path.join(vgg, 'H')
if not os.path.isdir(H_dir):
    os.mkdir(H_dir)

A = images[0]
M_0A = np.eye(3)
for i, img in enumerate(images[1:]):
    print "Registering %d -> %d" % (i, i + 1)
    B = images[i + 1]
    M_0B, S = register.dense_MI(B, A, levels=options.levels + 1,
                                std=3, win_size=9,
                                translation_only=options.translation,
                                fixed_scale=options.fixed_scale)
    print "Mutual information: ", S
    if S > 1.5:
        print "Warning: registration (%d -> %d) probably failed." % (i, i + 1)

    H = '%03d.%03d.H' % (i, i + 1)
    imsave(os.path.join(H_dir, H + '.png'),
           register.stack.with_transform([A, B],
                                         [np.eye(3), np.linalg.inv(M_0B)],
                                         oshape=A.shape),
           )

    M_A0 = np.linalg.inv(M_0A)
    M_0A = M_0B
    # Transformation relative to previous frame
    #
    # H_0B = H_AB * H_0A
    # => H_AB = H_0B * H_0A.I
    #
    M_AB = np.dot(M_0B, M_A0)
    np.savetxt(os.path.join(H_dir, H), M_AB, delimiter=' ')
