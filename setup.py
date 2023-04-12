from __future__ import with_statement, print_function, absolute_import

from setuptools import setup, find_packages, Extension
from distutils.version import LooseVersion

from pathlib import Path
# import os
# from glob import glob
# from os.path import join
import numpy

from setuptools.command.build_ext import build_ext


_VERSION = '0.3.2'

world_src_top = Path("lib") / "World" / "src" #join("lib", "World", "src")
world_sources = world_src_top.glob("*.cpp")   # glob(join(world_src_top, "*.cpp"))

ext_modules = [
    Extension(
        name="pyworld.pyworld",
        include_dirs=[world_src_top, numpy.get_include()],
        # sources=[join("pyworld", "pyworld.pyx")] + world_sources,
        sources=[Path("pyworld") /  "pyworld.pyx"] + world_sources,
        language="c++")]

setup(
    name="pyworld",
    description="PyWorld: a Python wrapper for WORLD vocoder",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
    version=_VERSION,
    packages=find_packages(),
    setup_requires=[
        'numpy',
    ],
    install_requires=[
        'numpy',
        'cython>0.24',
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
