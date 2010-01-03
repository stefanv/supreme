"""Construct super-resolution reconstruction of a registered data-set.

"""
## SCALE = 4
## UPDATE = 1 # if False, do a single pass calculation instead of
##            # adding one frame at a time
## DAMP = 1e-8
## PHOTOMETRIC_ADJUSTMENT = True
## METHOD = 'LSQR' # 'CG' or 'LSQR' or 'descent'
## OPERATOR = 'polygon' # 'polygon' # bilinear or polygon

import numpy as np

from supreme.resolve import solve, initial_guess_avg
from supreme.config import data_path
from supreme.io import load_vgg
from supreme.transform import homography
from supreme.noise import dwt_denoise

import matplotlib.pyplot as plt

import sys, os
from optparse import OptionParser

usage = "%prog [options] vgg_dir"
parser = OptionParser(usage=usage)
parser.add_option('-s', '--scale', type=float,
                  help='Resolution improvement required [default: %default]')
parser.add_option('-d', '--damp', type=float,
                  help='Damping coefficient -- '
                       'suppresses oscillations [default: %default]')
parser.add_option('-m', '--method', dest='method',
                  help='`CG`, `LSQR` or `descent`. '
                  'Specifies optimisation algorithm [default: %default]')
parser.add_option('-o', '--operator', dest='operator',
                  help='`polygon` or `bilinear`. The camera '
                       'model is approximated by this '
                       'interpolation scheme. [default: %default]')
parser.add_option('-u', '--update', action='store_true',
                  help='Use images as incremental evidence [default: %default]')
parser.add_option('-p', '--photo-adjust',
                  action='store_false',
                  help='Perform photometric adjustment [default: %default]')

parser.set_defaults(scale=2,
                    damp=1e-1,
                    method='CG',
                    operator='polygon',
                    update=False,
                    photo_adjust=True)

(options, args) = parser.parse_args()

d = options.__dict__
print "Options"
print "------------------------"
for k in d:
    print '%s: %s' % (k, d[k])
print "------------------------"

if len(parser.largs) == 1:
    vgg_dir = parser.largs[0]
else:
    parser.print_help()
    sys.exit(0)

ic = load_vgg(vgg_dir)

# Perform crude photometric registration
ref = ic[0].copy()
images = []
scales = []
for i in range(len(ic)):
    scale = 1

    if options.photo_adjust:
        img = ic[i]
        img_warp = homography(ic[i], ic[i].info['H'])
        mask = (img_warp > 20) & (img_warp < 220) & \
               (ref > 20) & (ref < 220)
        scale = np.mean(ref[mask].astype(float) / img_warp[mask])

    scales.append(scale)
    images.append(ic[i] * scale)

print "Images scaled by: %s" % str(['%.2f' % f for f in scales])

HH = [i.info['H'] for i in images]
oshape = np.floor(np.array(images[0].shape) * options.scale)
avg = initial_guess_avg(images, HH, options.scale, oshape)

#
# Solve by adding one frame at a time
#

if options.update:
    #
    # Update solution one frame at a time
    #
    out = avg.copy()
    for j in range(1):
        print "SR iteration %d" % j
        for i in range(len(images)):
            print "Resolving frame %d" % i
            out = solve([images[i]], [HH[i]], scale=options.scale, tol=0,
                        x0=out, damp=options.damp, iter_lim=200,
                        method=options.method, operator=options.operator)

else:
    #
    # Solve all at once
    #
    out = avg.copy()
    out = solve(images, HH, scale=options.scale, tol=0,
                x0=out, damp=options.damp, iter_lim=200,
                method=options.method)

import scipy.misc
scipy.misc.imsave('/tmp/avg.png', avg)
scipy.misc.imsave('/tmp/out.png', out)

plt.subplot(3, 1, 1)
plt.imshow(ic[0], interpolation='nearest', cmap=plt.cm.gray)

plt.subplot(3, 1, 2)
plt.imshow(avg, interpolation='lanczos', cmap=plt.cm.gray)

plt.subplot(3, 1, 3)
plt.imshow(out, interpolation='lanczos', cmap=plt.cm.gray)

plt.show()
