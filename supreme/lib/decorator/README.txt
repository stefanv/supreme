Decorator module
---------------------------

Dependencies:

The decorator module is intented for usage in Python 2.4 and above, 
but it also works with limitated functionality in Python 2.3 and 
possibily below.

Installation:

If you have ``easy_install``, just type ``easy_install decorator``, else
unzip the distribution archive into a directory called "decorator" 
in your Python path. For instance, on Unices you could give something 
like that:

$ unzip decorator.zip -d decorator

Testing:

Just go in the package directory and give

$ python doctester.py documentation.txt

This will generate the _main.py file containing all the examples
discussed in the documentation, and will run the corresponding tests.


Backward compatibility
------------------------------------

The 2.0 release of the decorator module breaks backward compatibility in
a few minor ways.

- now ``decorator`` fails setting the right name for the decorated function
  when using Python 2.3. I judged that this was an acceptable price 
  considering that Python 2.3 has become pretty old and that in any case
  using decorators in Python 2.3 is uncommon.

- now the decorated function and the original function do not share the
  same attributes, the decorated function has just a copy of the 
  original function attributes.

- now the utility function ``getinfo`` returns a different dictionary;

- the utility function ``newfunc`` has been removed; its functionality has been
  subsumed into ``update_wrapper``.
