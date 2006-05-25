from numpy.distutils.core import setup, Extension

setup(
    name='Nurbs',
    version='0.1',
    description='Python module to work with NURBS curves and surfaces.',
    author='Runar Tenfjord',
    author_email='runten@netcom.no',
    url='http://runten.tripod.com/',
    packages=['Nurbs', 'Nurbs.demos'],
    ext_modules = [Extension("Nurbs._Bas", ["Nurbs/_Bas.c"])],
    data_files=[('Nurbs/Doc', ['LICENSE', 'README'])]
    )

