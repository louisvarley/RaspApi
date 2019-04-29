#! /usr/bin/env python3

"""
Distutils setup file.
"""

import os

try:
    from setuptools import setup, find_packages
except:
    raise ImportError("setuptools is required!")
import io
import os


def get_long_description():
    """Extract description from README.md, for PyPI's usage"""
    try:
        fpath = os.path.join(os.path.dirname(__file__), "README.md")
        with io.open(fpath, encoding="utf-8") as f:
            readme = f.read()
            desc = readme.partition("<!-- start_ppi_description -->")[2]
            desc = desc.partition("<!-- stop_ppi_description -->")[0]
            return desc.strip()
    except IOError:
        return None

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('VERSION') as f:
    version = 'v1.0.' + f.readline()

# https://packaging.python.org/guides/distributing-packages-using-setuptools/
setup(
    name='myRaspPI',
    version=version,
    packages=find_packages(),
    install_requires=required,
    package_data={'': ['VERSION']},
    entry_points = {
            'console_scripts': [
                'myRaspPI = myRaspPI.app:main',                  
            ],              
        },
    python_requires='>=3',
    # pip > 9 handles all the versioning
    zip_safe=False,

    # Metadata
    author='Louis Varley',
    author_email='louisvarley@googlemail.com',
    maintainer='Louis Varley',
    description='Raspberry PI Distributed API Controllers for IOT',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    license='GPLv2',
    url='https://scapy.net',
    project_urls={
        'Source Code': 'https://github.com/louisvarley/myRaspPI',
    },
    download_url='https://github.com/louisvarley/myRaspPItarball/master',
    keywords=["IOT"]
)

