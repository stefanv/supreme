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
from supreme.io import load_vgg, imread, imsave
from supreme.transform import homography
from supreme.noise import dwt_denoise
from supreme.photometry import photometric_adjust

import scipy.ndimage as ndi

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
                  help='Do not perform photometric adjustment '
                       '[default: %default]')
parser.add_option('-L', '--norm', type=int,
                  help='The norm used to measure errors. [default: %default]')
parser.add_option('-c', '--convergence', dest='previous_result',
                  help='Use a previously calculated result to track '
                       'convergence in "update"-mode. The image file '
                       'should be specified as the parameter.')
parser.add_option('-i', '--ignore', action="append", type="int",
                  help='Ignore this frame nr. May be specified more than once.')

parser.set_defaults(scale=2,
                    damp=1e-1,
                    method='CG',
                    operator='polygon',
                    update=False,
                    norm=2,
                    photo_adjust=True)

(options, args) = parser.parse_args()

if options.previous_result and not options.update:
    raise RuntimeError('Cannot do convergence tracking in direct '
                       'estimation mode.')

if options.norm not in (1, 2):
    raise ValueError("Only L1 and L2 error norms are supported.")

if not options.ignore:
    options.ignore = []

d = options.__dict__
print "Input Parameters"
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
scale_offset = []
for i in range(len(ic)):
    scale = 1
    offset = 0

    if options.photo_adjust:
        img_warp = homography(ic[i], ic[i].info['H'])
        scale, offset = photometric_adjust(img_warp, ref)
        scale_offset.append((scale, offset))

    images.append(ic[i] * scale + offset)

print "Images adjusted by: %s" % str(['%.2f, %.2f' % (a,b)
                                      for (a,b) in scale_offset])

images = [img for i,img in enumerate(images) if not i in options.ignore]

HH = [i.info['H'] for i in images]
oshape = np.floor(np.array(images[0].shape) * options.scale)
avg = initial_guess_avg(images, HH, options.scale, oshape)

#
# Update solution one frame at a time
#
if options.update:
    if options.previous_result:
        res = imread(options.previous_result, flatten=True)
        err = []

    out = avg.copy()
    for j in range(1):
        print "SR iteration %d" % j
        for i in range(len(images)):
            print "Resolving frame %d" % i
            out = solve([images[i]], [HH[i]], scale=options.scale, tol=0,
                        x0=out, damp=options.damp, iter_lim=200,
                        method=options.method, operator=options.operator,
                        norm=options.norm)

            if options.previous_result:
                if not res.shape == out.shape:
                    raise RuntimeError('Previous result specified for '
                                       'convergence analysis did not have '
                                       'same shape as output.  Is this the '
                                       'same data-set and zoom ratio?')
                err.append(np.linalg.norm(res - out))

else:
    #
    # Solve all at once
    #
    out = avg.copy()
    out = solve(images, HH, scale=options.scale, tol=0,
                x0=out, damp=options.damp, iter_lim=200,
                method=options.method, operator=options.operator,
                norm=options.norm)

import matplotlib.pyplot as plt

if options.previous_result:
    plt.figure()
    plt.plot(err)
    plt.xlabel('Iteration')
    plt.ylabel('Error Norm')
    plt.title('SR Convergence')

if options.photo_adjust:
    a, b = photometric_adjust(out, avg)
    out *= a
    out += b

out = np.clip(out, 0, 255)

imsave('/tmp/avg.png', avg)
print 'Average image saved as /tmp/avg.png'
imsave('/tmp/out.png', out)
print 'Resulting image saved as /tmp/out.png'

plt.figure()
plt.subplot(3, 1, 1)
plt.imshow(ic[0], interpolation='nearest', cmap=plt.cm.gray)

plt.subplot(3, 1, 2)
plt.imshow(avg, interpolation='lanczos', cmap=plt.cm.gray)

plt.subplot(3, 1, 3)
plt.imshow(out, interpolation='lanczos', cmap=plt.cm.gray)

plt.show()

print "Input Parameters were:"
print "------------------------"
for k in d:
    print '%s: %s' % (k, d[k])
print "------------------------"

filename = '_'.join([os.path.basename(os.path.abspath(vgg_dir)),
                     'x%.2f' % options.scale,
                     '%.3flam' % options.damp,
                     options.method,
                     options.operator,
                     (options.update and 'update') or 'direct',
                     'L%d' % options.norm,
                     (options.photo_adjust and 'PA') or ''])
print "Suggested filename: %s.png" % filename
