"""
Demonstrate log polar transform.
"""

import pylab as P
import os

from numpy.testing import set_local_path, restore_path
set_local_path('../../..')
import supreme
restore_path()

images = ['misc/nova_grey.png', 'misc/nova.png', 'misc/nova_alpha.png']
im_descr = {'misc/nova_grey.png': 'Grey-level input',
           'misc/nova.png': 'Colour input',
	   'misc/nova_alpha.png': 'Alpha layered input'} 
for im in images:
    img1 = supreme.imread(os.path.join(supreme.config.data_path,im))
    print "Input image shape: ", img1.shape
                                   
    import timeit
    tic = timeit.time.time()
    img2 = supreme.transform.logpolar(img1)
    print "Output image shape: ", img2.shape
    toc = timeit.time.time()
    print "Transform completed in %.2f seconds." % (toc-tic)

    if img2.ndim == 3 and img2.shape[2] == 4:
	img1[...,1] = img1[...,1] & img1[...,3]
	img1 = img1[...,0:3]
	
	img2[...,1] = img2[...,1] & img2[...,3]
	img2 = img2[...,0:3]
	
    P.figure()
    P.subplot(121)
    P.title(im_descr[im])    
    P.imshow(img1,cmap=P.cm.gray)
    P.subplot(122)
    P.imshow(img2,origin='upper',cmap=P.cm.gray)
    P.title('Log polar transform')
    P.xlabel('Log distance')
    P.ylabel(r'Angle')
    P.show()
    P.close()
