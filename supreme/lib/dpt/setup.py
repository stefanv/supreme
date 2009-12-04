def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration, get_numpy_include_dirs

    config = Configuration('dpt', parent_package, top_path)

    for dpt_mod in ('int_array', 'connected_region',
                    'connected_region_handler', 'ccomp', 'base'):
        config.add_extension(dpt_mod, sources=[dpt_mod + '.c'],
                             include_dirs=[get_numpy_include_dirs()])

    config.add_data_dir('tests')

    return config
