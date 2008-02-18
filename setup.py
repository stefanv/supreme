#!/usr/bin/env python

import os
import sys
from glob import glob

from setuptools import setup, find_packages, Extension

def packages_and_tests(packages):
    out = []
    for p in packages:
        out.append(p)
        
        test_dir = p + '.tests'
        if os.path.isdir(test_dir.replace('.','/')):
            out.append(test_dir)

    return out

setup(
  name = 'supreme',
  version = '0.0',
  packages = packages_and_tests(find_packages()),
  
  ext_modules = [Extension('supreme/ext/libsupreme_', 
                           glob('supreme/ext/*.c')),

                 Extension('supreme/lib/klt/libklt_',
                           ['supreme/lib/klt/' + f for f in
                                 ['convolve.c', 'error.c', 'pnmio.c', \
                                  'pyramid.c', 'selectGoodFeatures.c',\
                                  'storeFeatures.c', 'trackFeatures.c', \
                                  'klt.c', 'klt_util.c', 'writeFeatures.c']]),

                 Extension('supreme/lib/fast/libfast_',
                           glob('supreme/lib/fast/*.c')),
                ],
                
  package_data = {
      '': ['*.txt', '*.png', '*.jpg', '*.pgm'],
  },
  
  zip_safe = False,
  
  author = "Stefan van der Walt",
  author_email = "<stefan.no-spam(at)mentat.za.net>",
  description = "SUper REsolution MEthods",
  url = "http://mentat.za.net",
  license = "GPL",
)
