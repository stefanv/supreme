from os.path import join, dirname
from glob import glob

def configuration(parent_package='', top_path=None, package_name='ext'):
    from numpy.distutils.misc_util import Configuration
    config = Configuration(package_name,parent_package,top_path)
    config.add_extension('libsupreme_', sources=glob(join(dirname(__file__),'*.c')))
    config.add_data_dir('tests')
    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(configuration=configuration)
