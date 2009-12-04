from supreme._build import CExtension

def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration, get_numpy_include_dirs

    config = Configuration('klt', parent_package, top_path)

    config.ext_modules.append(CExtension('libklt_',
                                         ['convolve.c', 'error.c', 'pnmio.c',
                                          'pyramid.c', 'selectGoodFeatures.c',
                                          'storeFeatures.c', 'trackFeatures.c',
                                          'klt.c', 'klt_util.c',
                                          'writeFeatures.c'],
                                         path=config.local_path))

    config.add_data_dir('tests')

    return config
