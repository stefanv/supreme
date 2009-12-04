import os.path
from numpy.distutils.core import Extension

def CExtension(name, files, path='', **kwargs):
    """Build an extension with a dummy Py_InitModule.

    """
    name = os.path.join(path, name)
    files = [os.path.join(path, f) for f in files]
    libname = os.path.basename(name)
    initfile = os.path.join(path, libname + 'init.c')
    if not os.path.exists(initfile):
        f = open(initfile,'w')
        f.write('''
#include <Python.h>

PyMethodDef methods[] = {
  {NULL, NULL},
};

void
init%(module)s()
{
    (void)Py_InitModule("%(module)s", methods);
}
''' % {'module':libname})

    if not initfile in files:
        files.append(initfile)
    return Extension(name, files, **kwargs)
