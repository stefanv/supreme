def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration, get_numpy_include_dirs

    config = Configuration('nurbs', parent_package, top_path)

    config.add_extension('_Bas', ['_Bas.c'],
                         include_dirs=[get_numpy_include_dirs()],
                         )
    config.add_data_dir('doc')

    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(
        configuration=configuration,

        version='0.1',
        description='Python module to work with NURBS curves and surfaces.',
        author='Runar Tenfjord',
        author_email='runten@netcom.no',
        url='http://runten.tripod.com/',
        )

