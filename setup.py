#!/usr/bin/env python

import os
import sys

from numpy.distutils.misc_util import Configuration

def configuration(parent_package='',top_path=None):
    config = Configuration(None,parent_package,top_path)

    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_subpackage('supreme')
    return config

def setup_package():
    from numpy.distutils.core import setup

    old_path = os.getcwd()
    local_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(local_path)
    sys.path.insert(0,local_path)

    try:
        setup(
            name = 'supreme',
            version = '0.0',
            author = "Stefan van der Walt",
            author_email = "<stefan.no-spam(at)mentat.za.net>",
            description = "SUper REsolution MEthods",
            url = "http://mentat.za.net",
            license = "GPL",
            configuration = configuration)
    finally:
        del sys.path[0]
        os.chdir(old_path)
    return
            
if __name__ == '__main__':
    setup_package()
