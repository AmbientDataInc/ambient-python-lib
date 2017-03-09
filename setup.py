#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages

setup(
        name             = 'ambient',
        version          = '0.1.3',
        packages         = find_packages(),
        description      = 'Python module to send data to Ambient',
        license          = 'MIT',
        author           = 'Takehiko Shimojima',
        url              = 'https://github.com/TakehikoShimojima/ambient-python-lib.git',
        keywords         = 'pip github python ambient',
        py_modules       = ['ambient'],
        install_requires = ['requests']
        )
