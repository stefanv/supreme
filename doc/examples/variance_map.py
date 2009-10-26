"""Demonstrate variance maps."""

import os.path

import matplotlib.pyplot as plt

import supreme
from supreme.config import data_path
from supreme.ext import variance_map

fn = 'toystory/toystory001.png'
x = supreme.misc.imread(os.path.join(data_path,fn),flatten=True)

plt.subplot(121)
plt.imshow(x,cmap=plt.cm.gray)
plt.xlabel('Input image')
plt.subplot(122)
vm = variance_map(x,shape=(20,20))
vm /= vm.max()
plt.imshow(vm)
plt.xlabel('Variance map')
plt.show()
