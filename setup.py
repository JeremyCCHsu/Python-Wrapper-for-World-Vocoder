"""PyWorld is a Python wrapper for WORLD vocoder.

PyWorld wrappers WORLD, which is a free software for high-quality speech
analysis, manipulation and synthesis. It can estimate fundamental frequency (F0),
aperiodicity and spectral envelope and also generate the speech like input speech
with only estimated parameters.
"""


from __future__ import with_statement, print_function, absolute_import

from setuptools import setup, find_packages, Extension
from distutils.version import LooseVersion

import os
from glob import glob
from os.path import join

from setuptools.command.build_ext import build_ext as _build_ext


DOCLINES = __doc__.split('\n')
_VERSION = '0.2.8'

class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())

world_src_top = join("lib", "World", "src")
world_sources = glob(join(world_src_top, "*.cpp"))

ext_modules = [
    Extension(
        name="pyworld.pyworld",
        include_dirs=[world_src_top],
        sources=[join("pyworld", "pyworld.pyx")] + world_sources,
        language="c++")]

setup(
    name="pyworld",
    description=DOCLINES,
    long_description='\n'.join(DOCLINES[2:]),
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
    version='0.2.8',
    packages=find_packages(),
    setup_requires=[
        'numpy',
    ],
    install_requires=[
        'numpy',
        'cython>=0.24.0',
    ],
    extras_require={
        'test': ['nose'],
        'sdist': ['numpy', 'cython'],
    },
    author="Pyworld Contributors",
    author_email="jeremycchsu@gmail.com",
    url="https://github.com/JeremyCCHsu/Python-Wrapper-for-World-Vocoder",
    keywords=['vocoder'],
    classifiers=[],
)
