# supreme — SUper-REsolution MEthods

[http://mentat.za.net/supreme](http://mentat.za.net/supreme)

This is experimental research software that performs multi-image
super-resolution imaging.  It requires the images to be registered
beforehand using, e.g., Elastix, or a
[robust feature-based method](https://github.com/scikit-image/skimage-tutorials/blob/master/lectures/adv3_panorama-stitching.ipynb).

You are most likely only interested in running
`doc/example/super_resolve.py`.  That script requires the images to be
in
[VGG format](https://github.com/stefanv/supreme/blob/master/doc/vgg_format.pdf).
An [example VGG dataset](https://mentat.za.net/supreme/data/library.tar.gz) is
provided of the Oxford Library Sequence.

For a full technical overview of this work, please refer
to [the overview paper](http://arxiv.org/abs/1210.3404)
or [my dissertation](https://mentat.za.net/phd_dissertation.html).
