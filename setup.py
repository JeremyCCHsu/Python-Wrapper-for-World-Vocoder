from __future__ import absolute_import, print_function, with_statement

import sys
from glob import glob
from os.path import join

import numpy
from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext


_VERSION = '0.3.5'


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
    install_requires=['numpy'],
    extras_require={
        'test': ['nose'],
        'sdist': ['numpy', 'cython>=0.24'],
    },
    author="Pyworld Contributors",
    author_email="jeremycchsu@gmail.com",
    url="https://github.com/JeremyCCHsu/Python-Wrapper-for-World-Vocoder",
    keywords=['vocoder'],
    classifiers=[],
)
