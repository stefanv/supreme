import os.path
import glob

import numpy as np
import matplotlib.pyplot as plt

import supreme.api as sr
from supreme.config import data_path, mkdir

print "Reading images and features..."
features = []
images = []

dataset = 'toystory'
basename = 'toystory'
imagetype = 'png'
featuretype = 'sift'
T = 0.6
image_files = sorted(glob.glob(
    os.path.join(data_path, '%s/%s*.%s' % (dataset,basename,imagetype))))
feature_files = sorted(glob.glob(
    os.path.join(data_path,'%s/%s*.%s' % (dataset,basename,featuretype))))

images = [sr.io.imread(fn,flatten=True) for fn in image_files]
features = [sr.feature.SIFT.fromfile(fn, mode=featuretype.upper())
            for fn in feature_files]

for pair in zip(image_files,feature_files):
    print pair[0], '->', pair[1]

print "Matching features..."
ref = features[0]
tf_matrices = [np.eye(3)]
valid_matrices = [True]
for frame in features[1:]:
    match,dist,valid = sr.feature.match(frame['data'],ref['data'],threshold=T)

    valid_ref = match[valid]
    xf,yf = frame['column'][valid],frame['row'][valid]
    xr,yr = ref['column'][valid_ref],ref['row'][valid_ref]

    try:
        M,converged = sr.register.sparse(yr,xr,yf,xf,mode='RANSAC',confidence=0.8)
    except:
        print "RANSAC did not converge.  Skipping frame."
        continue

    valid_matrices.append(converged)
    tf_matrices.append(M)
    print M

    print "Found %d matches." % valid.sum()

images = [i for i,v in zip(images,valid_matrices) if v]
tf_matrices = [t for t,v in zip(tf_matrices,valid_matrices) if v]

# Scale for super-resolution
scale = 5.
for M in tf_matrices:
    M[:2,:] *= scale
oshape = np.ceil(np.array(images[0].shape)*scale).astype(int)

for img in images:
    img -= img.min()
print "Reconstructing using interpolation..."
out1 = sr.register.stack.with_transform(images,tf_matrices,oshape=oshape)

# Astronomy
#out[out > 10] = 10
#out /= out.max()


print "Stacking using polygon overlap..."
out2 = np.zeros(oshape,float)
for i,(img,M) in enumerate(zip(images,tf_matrices)):
    print "Stacking frame %d" % i
    out2 += sr.ext.interp_transf_polygon(img,np.linalg.inv(M),oshape)
out2 /= len(images)
out2[out2 > 500] = 500

import scipy as S
imsave = S.misc.pilutil.imsave
mkdir('output')

imsave('output/original.png', images[0])
imsave('output/_linear.png', out1)
imsave('output/_polygon.png', out2)

plt.subplot(121)
plt.imshow(out1,interpolation='nearest',cmap=plt.cm.gray)
plt.subplot(122)
plt.imshow(out2,interpolation='nearest',cmap=plt.cm.gray)
plt.show()
