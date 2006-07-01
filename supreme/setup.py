packages = ['geometry','register','transform']
ext_libs = ['lib/Nurbs-0.1','lib/Polygon-1.16']
data_files = ['doc/*.txt']

import os

def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('supreme',parent_package,top_path)
    for p in packages:
        config.add_subpackage(p)
        config.add_data_dir(os.path.join(p,'tests'))
    for f in data_files:
        config.add_data_files(f)
    config.make_config_py() # installs __config__.py
    return config
    
if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(configuration=configuration)
