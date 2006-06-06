"""
Demonstrate log polar transform.
"""

import pylab as P
import os

from numpy.testing import set_local_path, restore_path
set_local_path('../../..')
import supreme
restore_path()

img1 = supreme.imread(os.path.join(supreme.config.data_path,
                                   'misc/nova_alpha.png'))
print "Input image shape: ", img1.shape
                                   
import timeit
tic = timeit.time.time()
img2 = supreme.transform.logpolar(img1)
print "Output image shape: ", img2.shape
toc = timeit.time.time()
print "Transform completed in %.2f seconds." % (toc-tic)

P.figure()
P.subplot(121)
P.imshow(img1)
P.subplot(122)
P.imshow(img2,origin='upper')
P.xlabel('Log distance')
P.ylabel(r'Angle')
P.show()
P.close()
