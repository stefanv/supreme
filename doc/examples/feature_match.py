import matplotlib.pyplot as plt
import numpy as np
import os, sys

from supreme.config import data_path
from supreme import transform
from supreme.io import imread, ImageCollection
from supreme.transform import matrix as homography
from supreme.feature import dpt

import supreme.register

# This used to do log polar transforms, but now
# we just match the distributions of the coefficients
from supreme.register.correspond import correspond

# ----------------------------------------------------------------------

if len(sys.argv) == 3:
    icc = [imread(sys.argv[i]) for i in (1, 2)]
    ic = [imread(sys.argv[i], flatten=True) for i in (1, 2)]
    imgc0 = icc[0]
    img0 = ic[0]
    imgc1 = icc[1]
    img1 = ic[1]
else:
    icc = ImageCollection(os.path.join(data_path, 'pathfinder/i44*.png'))
    ic = ImageCollection(os.path.join(data_path, 'pathfinder/i44*.png'),
                         grey=True)

    imgc0 = icc[0]
    imgc1 = icc[7]
    img0 = ic[0]
    img1 = ic[7]

show_features = False # Whether to display the features found on screen
stack = True # Disable this to view the output without stacking
feature_method = 'fast' # 'dpt' or 'fast'
dpt_feature_nr = 200
fast_barrier = 10
registration_method = 'RANSAC' # or iterative
RANSAC_confidence = 0.99
win_size = None
save_tiff = True # Save warped images to tiff
refine_using_MI = False # Refine using mutual information
window = 0 # only return 1 feature per window

# ----------------------------------------------------------------------

print "Getting feature coordinates."
def get_brightest_pulses(weight, area, N=100):
    """
    Return feature coordinates and areas.
    """
    sort_idx = np.argsort(weight.flat)
    not_brightest = sort_idx[:-N]
    brightest = sort_idx[-N:]

    weight.flat[not_brightest] = 0
    feat = zip(*np.nonzero(weight))
    area = area.flat[brightest]

    return feat, area

def set_boundary_zero(x, size=5):
    x[:size, :] = 0
    x[:, :size] = 0
    x[-size:, :] = 0
    x[:, -size:] = 0

if feature_method == 'dpt':
    import supreme.lib.dpt as dpt
    import supreme.lib.dpt.connected_region_handler as crh
    from supreme.feature.dpt import features as dpt_feat

    print "Decomposing discrete pulse transform..."
    pulses = dpt.decompose(img0.astype(np.int))
    pulses_mod = dpt.decompose(img1.astype(np.int))

    print "Calculating feature positions..."
    weight, area = dpt_feat(pulses, img0.shape, win_size=window, max_area=100)
    weight_mod, area_mod = dpt_feat(pulses_mod, img1.shape, win_size=window)

    # Ignore features that occur right on boundary
    set_boundary_zero(weight, 5)
    set_boundary_zero(area, 5)
    set_boundary_zero(weight_mod, 5)
    set_boundary_zero(area_mod, 5)

    feat_coord, feat_area = get_brightest_pulses(weight, area, N=dpt_feature_nr)
    feat_mod_coord, feat_mod_area = get_brightest_pulses(weight_mod, area_mod,
                                                         N=dpt_feature_nr)
elif feature_method == 'fast':
    from supreme.lib import fast

    perm = np.random.permutation
    feat_coord = perm(fast.corner_detect(img0,
                                         barrier=fast_barrier))
    print "FAST found %d features." % len(feat_coord)
    feat_coord = [(i,j) for (j,i) in feat_coord]
    feat_mod_coord = perm(fast.corner_detect(img1,
                                             barrier=fast_barrier))

    feat_area = np.ones(len(feat_coord)) * 4
    feat_mod_coord = [(i,j) for (j,i) in feat_mod_coord]
    feat_mod_area = np.ones(len(feat_mod_coord)) * 4
else:
    raise ValueError("Invalid feature extractor specified.")

import matplotlib.pyplot as plt

if show_features:
    plt.subplot(121)
    plt.hold(True)
    plt.imshow(img0, cmap=plt.cm.gray, interpolation='nearest')
    for (i, j), a in zip(feat_coord, feat_area):
        plt.plot(j, i, 'o', markersize=4)

    plt.subplot(122)
    plt.hold(True)
    plt.imshow(img1, cmap=plt.cm.gray, interpolation='nearest')
    for (i, j), a in zip(feat_mod_coord, feat_mod_area):
        plt.plot(j, i, 'o', markersize=4)
    plt.show()

print "Finding tentative correspondences..."
if win_size is None:
    win_size = np.mean(feat_mod_area)
    print win_size
    win_size = np.clip(win_size, 5, 100)
    print "Automatically determining window size...%d" % win_size

print "win_size=%.2f" % win_size
correspondences = correspond(feat_coord, img0.astype(np.uint8),
                             feat_mod_coord, img1.astype(np.uint8),
                             win_size=win_size)

if stack:
    pairs = np.array(correspondences)
    print '%d correspondences found' % len(pairs)
    if len(pairs) <= 4:
        raise RuntimeError('Not enough correspondences to do H-matrix'
                           'estimation.')
    M, converged = supreme.register.sparse(pairs[:, 1, 0], pairs[:, 1, 1],
                                           pairs[:, 0, 0], pairs[:, 0, 1],
                                           mode=registration_method,
                                           confidence=RANSAC_confidence)
#                                           inliers_required=len(pairs)*0.8)
    print np.array2string(M, separator=', ')
    print "Also writing transformation matrix to /tmp/H.H."
    np.savetxt('/tmp/H.H', M)

    if refine_using_MI:
        # Estimate parameters from M
        s = np.sqrt(M[0, 0]**2 + M[1, 0]**2)
        theta = np.arccos(M[0, 0]/s)
        p = [theta, s, s, M[0, 2], M[1, 2]]
        M, S = supreme.register.dense_MI(img0.astype(np.uint8),
                                         img1.astype(np.uint8), p=p, levels=1)
        print np.array2string(M, separator=', ')

    if show_features:
        plt.subplot(2, 1, 2)
        stack = supreme.register.stack.with_transform((imgc0, imgc1),
                                                      (np.eye(3), M),
                                                      save_tiff=save_tiff)
        plt.imshow(stack/stack.max(), cmap=plt.cm.gray, interpolation='nearest')

if show_features:
    plt.subplot(2, 1, 1)
    r0, c0 = img0.shape
    r1, c1 = img1.shape
    oshape = (max(r0, r1), c0 + c1)
    side_by_side = np.zeros(oshape, dtype=img0.dtype)
    side_by_side[0:r0, 0:c0] = img0
    side_by_side[0:r1, c0:c0 + c1] = img1
    plt.imshow(side_by_side, cmap=plt.cm.gray, interpolation='nearest')
    for ((i,j), (m, n)) in correspondences:
        plt.plot([j, n + img0.shape[1]], [i, m], '-o')
    plt.axis('image')

    plt.show()
