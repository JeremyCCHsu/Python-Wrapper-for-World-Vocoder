import os
import numpy
from setuptools import setup, Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension(
        name="pyworld",
        include_dirs=[numpy.get_include(),
        	os.path.join(os.getcwd(), 'src')],
        sources=["pyworld.pyx", 
        	"src/synthesis.cpp", "src/cheaptrick.cpp", "src/common.cpp", 
        	"src/d4c.cpp", "src/dio.cpp", "src/harvest.cpp", "src/fft.cpp", "src/matlabfunctions.cpp",
        	"src/stonemask.cpp", "src/synthesisrealtime.cpp"],
        language="c++")]

setup(name="pyworld",
	ext_modules=ext_modules,
	cmdclass={'build_ext': build_ext},
    version='0.1.2')
