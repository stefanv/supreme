"""Dependency injector with interface checking."""

__all__ = ['interface','inject']

import inspect
from numpy.testing import set_local_path, restore_path

set_local_path('../..')
import supreme.lib.zope.interface as zi
import supreme.lib.zope.interface.verify
restore_path()

def interface(cls,interface):
    """Set and verify class interface."""
    zi.classImplements(cls,interface)
    zi.verify.verifyClass(interface,cls)

def inject(cls, member_name, new_instance):
    """Inject functionality into a cls.member_name.

    Inputs:
    -------
    cls : class instance
        Class instance into which the new member is injected.
    member_name : string
        Member name to replace.
    new_instance : class instance
        cls.member_name is set to new_instance.

    Example:
    --------
    >>> class ISort(zi.Interface): pass

    >>> class DefaultSort: pass
    >>> interface(DefaultSort, ISort)

    >>> class QuickSort: pass
    >>> interface(QuickSort, ISort)

    >>> class Sorter:
    ...     def __init__(self):
    ...         self.sort = DefaultSort()
    ...
    >>> s = Sorter()
    >>> inject(s, 'sort', QuickSort())

    """
    for iface in zi.providedBy(getattr(cls,member_name)):
        zi.verify.verifyObject(iface,new_instance)

    setattr(cls,member_name,new_instance)
