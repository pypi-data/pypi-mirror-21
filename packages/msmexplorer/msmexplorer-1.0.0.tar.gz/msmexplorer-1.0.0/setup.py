# -*- coding: utf-8 -*-

"""
MSMExplorer: Visualizations for statistical models of biomolecular dynamics
"""

import sys
import subprocess
from setuptools import setup, find_packages

from distutils.spawn import find_executable
try:
    sys.dont_write_bytecode = True
    sys.path.insert(0, '.')
    from basesetup import write_version_py
finally:
    sys.dont_write_bytecode = False

NAME = "msmexplorer"
VERSION = "1.0.0"
ISRELEASED = True
__version__ = VERSION


def readme_to_rst():
    pandoc = find_executable('pandoc')
    if pandoc is None:
        raise RuntimeError("Turning the readme into a description requires "
                           "pandoc.")
    long_description = subprocess.check_output(
        [pandoc, 'README.md', '-t', 'rst'])
    short_description = long_description.split(b'\n\n')[1]
    return {
        'description': short_description,
        'long_description': long_description,
    }


def main(**kwargs):

    write_version_py(VERSION, ISRELEASED, 'msmexplorer/version.py')

    setup(
        name=NAME,
        version=VERSION,
        platforms=("Windows", "Linux", "Mac OS-X", "Unix",),
        classifiers=(
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Operating System :: Unix',
            'Operating System :: MacOS',
            'Operating System :: Microsoft :: Windows',
            'Topic :: Scientific/Engineering',
        ),
        keywords=('visualizations', 'biomolecular', 'simulations',
                  'markov state models'),
        author="Carlos Xavier Hernández",
        author_email="cxh@stanford.edu",
        url='https://github.com/cxhernandez/%s' % NAME,
        download_url='https://github.com/cxhernandez/%s/tarball/master' % NAME,
        license='LGPLv2+',
        packages=find_packages(),
        include_package_data=True,
        package_data={
            NAME: ['README.md',
                   'requirements.txt'],
        },
        zip_safe=False,
        **kwargs
    )


if __name__ == '__main__':
    kwargs = {}
    if any(e in sys.argv for e in ('upload', 'register', 'sdist')):
        kwargs = readme_to_rst()
    main(**kwargs)
