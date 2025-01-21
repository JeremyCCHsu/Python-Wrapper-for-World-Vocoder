"""PyWorld is a Python wrapper for WORLD vocoder.

PyWorld wrappers WORLD, which is a free software for high-quality speech
analysis, manipulation and synthesis. It can estimate fundamental frequency (F0),
aperiodicity and spectral envelope and also generate the speech like input speech
with only estimated parameters.

For more information, see https://github.com/JeremyCCHsu/Python-Wrapper-for-World-Vocoder
"""
from __future__ import division, print_function, absolute_import
import sys
if sys.version_info >= (3, 8):
    from importlib.metadata import version
    __version__ = version('pyworld')
else:
    import pkg_resources
    __version__ = pkg_resources.get_distribution('pyworld').version

from .pyworld import *
