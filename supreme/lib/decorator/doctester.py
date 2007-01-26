#!/usr/bin/env python2.4
# Author: michele.simionato@gmail.com
"""\
Example of usage:
$ doctester.py -v file.txt
"""
import sys, doctest, textwrap, re, types
#import warnings;warnings.filterwarnings('ignore', category=DeprecationWarning)

# regular expressions to identify code blocks of the form
#<scriptname.py> ... </scriptname.py>
DOTNAME = r'\b[a-zA-Z_][\w\.]*', # identifier with or without dots
SCRIPT = re.compile(r'(?s)#<(%s)>(.*?)#</\1>' % DOTNAME)

class file_(file):
    """This is a file class which treats specially the filename "-",
    returning stdin or stdout according to the mode."""
    def __new__(cls, name, mode="r", buffering=1):
        if name == "-" and "w" in mode or "a" in mode:
            return sys.stdout
        elif name == "-" and "r" in mode:
            return sys.stdin
        return super(file_, cls).__new__(cls, name, mode, buffering)
    
# a simple utility to extract the scripts contained in the original text
def scripts(txt):
    for MO in SCRIPT.finditer(txt):
        yield MO.group(1), textwrap.dedent(MO.group(2))

# save the scripts in the current directory
def savescripts(fname, txt):
    scriptdict = {}
    for scriptname, script in scripts(txt): # read scripts
        if scriptname not in scriptdict:
            scriptdict[scriptname] = script
        else:
            scriptdict[scriptname] += script
    for scriptname in scriptdict: # save scripts
        code = '# ' + scriptname + scriptdict[scriptname]
        print >> file(scriptname, 'w'), code
    return scriptdict

# based on a clever trick: it converts the original text into the docstring of
# the _main module; works both for Python 2.3 and 2.4;  threads work properly
# too.

def runtests(fname, txt, verbose=False):
    if "_main.py" in savescripts(fname, txt):
        _main = __import__("_main") # real module
    else: # dynamic module
        _main = types.ModuleType("__main__")
    _main.__doc__ = txt
    failed, tot = doctest.testmod(_main, verbose=verbose)
    doctest.master = None # cleanup the DocTestRunner
    # needed to avoid a warning in case of multiple calls of runtests
    if not verbose:
        print >> sys.stderr, "doctest: run %s tests, failed %s" % (tot, failed)
    # remove scripts
    return failed, tot

if __name__ == '__main__':
    try: set # need sets for option parsing
    except NameError: import sets; set = sets.Set # for Python 2.3
    try: fname = sys.argv[1]
    except IndexError: sys.exit(__doc__)
    valid_options = set("-v -h".split())
    options = set(sys.argv[2:])
    assert options < valid_options, "Unrecognized option"
    if "-h" in options: # print usage message and exit
        sys.exit(__doc__)
    runtests(fname, file_(fname).read(), "-v" in options)
