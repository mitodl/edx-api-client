# -*- encoding: utf-8 -*-
"""
Python setup file for the eds_api app.
"""
import os
from setuptools import setup, find_packages

import edx_api

# pylint: disable=invalid-name
dev_requires = [
    'flake8',
]

install_requires = open('requirements.txt').read().splitlines()


def read(filename):
    """Helper function to read bytes from file"""
    try:
        return open(os.path.join(os.path.dirname(__file__), filename)).read()
    except IOError:
        return ''


setup(
    name="edx-api-client",
    version=edx_api.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    license='The AGPL License',
    platforms=['OS Independent'],
    keywords='edx, rest api',
    author='MIT Office of Digital Learning',
    author_email='mitx-devops@mit.edu',
    url="https://github.com/mitodl/edx-api-client",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'dev': dev_requires,
    },
)
