import os.path
import glob

from numpy.testing import set_local_path, restore_path
import numpy as N
import pylab as P

set_local_path('../../..')
import supreme as sr
from supreme.config import data_path
restore_path()

print "Reading images and features..."
features = []
images = []

dataset = 'pathfinder'
basename = 'i44'
imagetype = 'png'
featuretype = 'surf'
T = 0.6
image_files = sorted(glob.glob(os.path.join(data_path,'%s/%s*.%s' % (dataset,basename,imagetype))))
feature_files = sorted(glob.glob(os.path.join(data_path,'%s/%s*.%s' % (dataset,basename,featuretype))))

images = [sr.imread(fn,flatten=True) for fn in image_files]
features = [sr.feature.SIFT.fromfile(fn,mode=featuretype.upper()) for fn in feature_files]

for pair in zip(image_files,feature_files):
    print pair[0], '->', pair[1]

print "Matching features..."
ref = features[0]
tf_matrices = [N.eye(3)]
valid_matrices = [True]
for frame in features[1:]:
    match,dist,valid = sr.feature.match(frame['data'],ref['data'],threshold=T)

    valid_ref = match[valid]
    xf,yf = frame['column'][valid],frame['row'][valid]
    xr,yr = ref['column'][valid_ref],ref['row'][valid_ref]

    M,ier = sr.register.sparse(yr,xr,yf,xf)
    valid_matrices.append(ier == 1)
    tf_matrices.append(M)

    print "Found %d matches." % valid.sum()

images = [i for i,v in zip(images,valid_matrices) if v]
tf_matrices = [t for t,v in zip(tf_matrices,valid_matrices) if v]

# Scale for super-resolution
scale = 3.
for M in tf_matrices:
    M[:2,:] *= scale
oshape = N.ceil(N.array(images[0].shape)*scale).astype(int)

for img in images:
    img -= img.min()
print "Reconstructing using interpolation..."
out1 = sr.register.stack.with_transform(images,tf_matrices,oshape=oshape)

# Astronomy
#out[out > 10] = 10
#out /= out.max()


print "Stacking using polygon overlap..."
out2 = N.zeros(oshape,float)
for i,(img,M) in enumerate(zip(images,tf_matrices)):
    print "Stacking frame %d" % i
    out2 += sr.ext.interp_transf_polygon(img,N.linalg.inv(M),oshape)
out2 /= len(images)
#out2[out2 > 500] = 500

import scipy as S
imsave = S.misc.pilutil.imsave
imsave('original.png',images[0])
imsave('_linear.png',out1)
imsave('_polygon.png',out2)

P.subplot(121)
P.imshow(out1,interpolation='nearest',cmap=P.cm.gray)
P.subplot(122)
P.imshow(out2,interpolation='nearest',cmap=P.cm.gray)
P.show()
