from os.path import join, dirname
from glob import glob

def configuration(parent_package='', top_path=None, package_name='klt'):
    from numpy.distutils.misc_util import Configuration
    config = Configuration(package_name,parent_package,top_path)
    config.add_extension('libklt_',
                         sources=['convolve.c', 'error.c', 'pnmio.c', \
                                  'pyramid.c', 'selectGoodFeatures.c',\
                                  'storeFeatures.c', 'trackFeatures.c', \
                                  'klt.c', 'klt_util.c', 'writeFeatures.c'])
    config.add_data_dir('tests')
    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(configuration=configuration)
