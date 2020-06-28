# This file is part of PyCI.
#
# PyCI is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# PyCI is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyCI. If not, see <http://www.gnu.org/licenses/>.

r"""
PyCI setup script.

Run `python setup.py --help` for help.

"""

from io import open
from os import path

from setuptools import setup

import numpy


name = 'pyci'

version = '0.2.0'

license = 'GPLv3'

author = 'Michael Richer'

author_email = 'richerm@mcmaster.ca'

url = 'https://github.com/msricher/pyci'

description = 'A flexible ab-initio quantum chemistry library for Configuration Interaction.'

long_description = open('README.rst', 'r', encoding='utf-8').read()


classifiers = [
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Science/Engineering :: Molecular Science',
    ]


install_requires = [
    'numpy>=1.13',
    'scipy>=0.17',
    ]


extras_require = {
    'build': ['cython'],
    'test': ['nose'],
    'doc': ['sphinx', 'sphinx_rtd_theme'],
    }


packages = [
    'pyci',
    'pyci.test',
    ]


package_data = {
    'pyci': ['*.h', '*.cpp', '*.pxd', '*.pyx'],
    'pyci.test': ['data/*.fcidump', 'data/*.npz'],
    }


include_dirs = [
    'parallel-hashmap',
    'eigen',
    'spectra/include',
    numpy.get_include(),
    path.abspath(path.dirname(__file__)),
    ]


compile_args = [
    '-DNPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION',
    '-Wall',
    '-fopenmp',
    '-O3',
    ]


cext = {
    'name': 'pyci.cext',
    'language': 'c++',
    'sources': [
        'pyci/common.cpp',
        'pyci/onespin.cpp',
        'pyci/twospin.cpp',
        'pyci/solve.cpp',
        'pyci/rdm.cpp',
        'pyci/enpt2.cpp',
        'pyci/hci.cpp',
        'pyci/cext.cpp',
        ],
    'include_dirs': include_dirs,
    'extra_compile_args': compile_args,
    'extra_link_args': compile_args,
    }


try:
    from Cython.Distutils import build_ext, Extension
    cext['sources'].remove('pyci/cext.cpp')
    cext['sources'].append('pyci/cext.pyx')
    cext['cython_compile_time_env'] = dict(PYCI_VERSION=version)
except ImportError:
    from setuptools.command.build_ext import build_ext
    from setuptools import Extension


if __name__ == '__main__':

    setup(
        name=name,
        version=version,
        license=license,
        author=author,
        author_email=author_email,
        url=url,
        description=description,
        long_description=long_description,
        classifiers=classifiers,
        install_requires=install_requires,
        extras_require=extras_require,
        packages=packages,
        package_data=package_data,
        include_package_data=True,
        ext_modules=[Extension(**cext)],
        cmdclass={'build_ext': build_ext},
        )
