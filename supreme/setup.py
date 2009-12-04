import os

def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration, get_numpy_include_dirs

    config = Configuration('supreme', parent_package, top_path)

    base_path = os.path.join(os.getcwd(), config.local_path)
    mod = [d for d in os.listdir(base_path) if not '.' in d]

    for m in mod:
        config.add_subpackage(m)

        if os.path.isdir(os.path.join(config.local_path, m, 'tests')):
            config.add_data_dir(os.path.join(m, 'tests'))

    return config
