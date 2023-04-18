from __future__ import with_statement, print_function, absolute_import

from setuptools import setup, find_packages, Extension
from distutils.version import LooseVersion

import sys
from glob import glob
from os.path import join
import numpy

from setuptools.command.build_ext import build_ext


_VERSION = '0.3.3'


world_src_top = join("lib", "World", "src")
world_sources = glob(join(world_src_top, "*.cpp"))

ext_modules = [
    Extension(
        name="pyworld.pyworld",
        include_dirs=[world_src_top, numpy.get_include()],
        sources=[join("pyworld", "pyworld.pyx")] + world_sources,
        language="c++")]

kwargs = {"encoding": "utf-8"} if int(sys.version[0]) > 2 else {}
setup(
    name="pyworld",
    description="PyWorld: a Python wrapper for WORLD vocoder",
    long_description=open("README.md", "r", **kwargs).read(),
    long_description_content_type="text/markdown",
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
    version=_VERSION,
    packages=find_packages(),
    setup_requires=[
        'numpy>=1.14.3',
    ],
    install_requires=[
        'numpy>=1.14.3',
        'cython>=0.28',
    ],
    extras_require={
        'test': ['nose'],
        'sdist': ['numpy>=1.14.3', 'cython>=0.28'],
    },
    author="Pyworld Contributors",
    author_email="jeremycchsu@gmail.com",
    url="https://github.com/JeremyCCHsu/Python-Wrapper-for-World-Vocoder",
    keywords=['vocoder'],
    classifiers=[],
)
