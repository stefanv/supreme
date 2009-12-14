from supreme._build import CExtension

def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration, get_numpy_include_dirs

    config = Configuration('pywt', parent_package, top_path)

    config.add_extension('_pywt', sources=['_pywt.c', 'common.c',
                                           'convolution.c', 'wavelets.c',
                                           'wt.c'],
                         include_dirs=[get_numpy_include_dirs()])

    config.add_data_dir('tests')

    return config

if __name__ == "__main__":
    from numpy.distutils.core import setup
    setup(configuration=configuration)
