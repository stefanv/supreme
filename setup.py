#!/usr/bin/env python

VERSION = '0.9'

import os
import sys
from glob import glob

import numpy as np

def configuration(parent_package='', top_path=None):
    if os.path.exists('MANIFEST'): os.remove('MANIFEST')

    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)

    config.set_options(
            ignore_setup_xxx_py=True,
            assume_default_configuration=True,
            delegate_options_to_subpackages=True,
            quiet=True)

    config.add_subpackage('supreme')

    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup

    setup(
        name = 'supreme',
        version = VERSION,
        configuration = configuration,

        package_data = {
            '': ['*.txt', '*.png', '*.jpg', '*.pgm'],
        },

        author = "Stefan van der Walt",
        author_email = "<stefan.no-spam(at)mentat.za.net>",
        description = "SUper REsolution MEthods",
        url = "http://mentat.za.net",
        license = "BSD3",
    )
