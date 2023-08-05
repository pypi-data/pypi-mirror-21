#!/usr/bin/env python
import os
from distutils.core import setup



def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


setup(
    name='kunits',
    version='0.0.2',
    license='MIT',
    description='Unit conversion library',
    author='Keith Philpott',
    url='https://bitbucket.org/cinckitchen/kunits',
    packages=get_packages('kunits'),
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ]
)
