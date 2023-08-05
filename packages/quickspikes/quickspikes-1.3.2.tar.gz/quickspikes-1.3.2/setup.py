#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python -*-
from setuptools import setup, find_packages, Extension

import numpy
try:
    numpy_include = numpy.get_include()
except AttributeError:
    numpy_include = numpy.get_numpy_include()

try:
    from Cython.Distutils import build_ext
    SUFFIX = '.pyx'
except ImportError:
    from distutils.command.build_ext import build_ext
    SUFFIX = '.c'

compiler_settings = {
    'include_dirs' : [numpy_include]
    }
_spikes = Extension('quickspikes.spikes', sources=['quickspikes/spikes' + SUFFIX],
                    **compiler_settings)

setup(
    name = 'quickspikes',
    version = '1.3.2',
    packages=find_packages(exclude=["*test*"]),
    ext_modules = [_spikes],
    cmdclass = {'build_ext': build_ext},

    install_requires = ["numpy>=1.9"],
    scripts = [],

    description = "detect and extract spikes in time series data",
    long_description = "detect and extract spikes in time series data",

    author = "Dan Meliza",
    author_email = "dan@meliza.org",
    maintainer = "Dan Meliza",
    maintainer_email = "dan@meliza.org",
    url= 'http://melizalab.github.com/quickspikes',
    download_url= 'https://github.com/downloads/melizalab/quickspikes',
    test_suite = 'nose.collector',
    )
