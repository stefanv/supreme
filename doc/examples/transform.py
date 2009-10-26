"""
Demonstrate log polar transform.
"""

import matplotlib.pyplot as plt
import os

import supreme

images = ['misc/nova_grey.png', 'misc/nova.png', 'misc/nova_alpha.png']
im_descr = {'misc/nova_grey.png': 'Grey-level input',
           'misc/nova.png': 'Colour input',
           'misc/nova_alpha.png': 'Alpha layered input'}

for im in images:
    img1 = supreme.misc.imread(os.path.join(supreme.config.data_path,im))
    print "Input image shape: ", img1.shape

    import timeit
    tic = timeit.time.time()
    img2 = supreme.transform.logpolar(img1)
    print "Output image shape: ", img2.shape
    toc = timeit.time.time()
    print "Transform completed in %.2f seconds.\n" % (toc-tic)

    if img2.ndim == 3 and img2.shape[2] == 4:
        img1[...,1] = img1[...,1] & img1[...,3]
        img1 = img1[...,0:3]

        img2[...,1] = img2[...,1] & img2[...,3]
        img2 = img2[...,0:3]

    plt.figure()
    plt.subplot(121)
    plt.title(im_descr[im])
    plt.imshow(img1,cmap=plt.cm.gray)
    plt.subplot(122)
    angles,d = img2.shape[:2]
    plt.imshow(img2,origin='upper',extent=(1,d,angles,1),cmap=plt.cm.gray)
    plt.title('Log polar transform')
    plt.xlabel('Log distance')
    plt.ylabel(r'Angle')
    plt.show()
    plt.close()
