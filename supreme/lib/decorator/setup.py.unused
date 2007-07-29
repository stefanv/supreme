try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='decorator',
      version='2.0.0',
      description=\
        'Better living through Python with decorators.',
      long_description="""\
As of now, writing custom decorators correctly requires some experience 
and it is not as easy as it could be. For instance, typical implementations
of decorators involve nested functions, and we all know 
that flat is better than nested. Moreover, typical implementations
of decorators do not preserve the signature of decorated functions,
thus confusing both documentation tools and developers.

The aim of the decorator module it to simplify the usage of decorators 
for the average programmer, and to popularize decorators usage giving 
examples of useful decorators, such as memoize, tracing, 
redirecting_stdout, locked, etc.""",
      author='Michele Simionato',
      author_email='michele.simionato@gmail.com',
      url='http://www.phyast.pitt.edu/~micheles/python/documentation.html',
      license="Python License",
      py_modules = ['decorator'],
      keywords="decorators generic utility",
      classifiers=['Development Status :: 1 - Stable',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Python License',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries',
                   'Topic :: Utilities'])

