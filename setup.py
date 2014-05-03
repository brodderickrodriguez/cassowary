#/usr/bin/env python
from setuptools import setup
from cassowary import VERSION

try:
    readme = open('README.rst')
    long_description = str(readme.read())
finally:
    readme.close()

required_pkgs = []

setup(
    name='cassowary',
    version=VERSION,
    description='A pure Python implementation of the Cassowary constraint solving algorithm.',
    long_description=long_description,
    author='Russell Keith-Magee',
    author_email='russell@keith-magee.com',
    url='http://pybee.org/cassowary',
    packages=[
        'cassowary',
    ],
    install_requires=required_pkgs,
    license='New BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='tests'
)
