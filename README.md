# PyWorldVocoder - A Python wrapper for World Vocoder


| **`Linux`** |
|-----------------|
| [![Build Status](https://travis-ci.org/JeremyCCHsu/Python-Wrapper-for-World-Vocoder.svg?branch=master)](https://travis-ci.org/JeremyCCHsu/Python-Wrapper-for-World-Vocoder) |


Morise's World Vocoder is a fast and high-quality vocoder.
World Vocoder parameterizes speech into three components:

  1. Pitch (fundamental frequency, F0) contour  
  2. Harmonic spectral envelope
  3. Aperiodic spectral envelope (relative to the harmonic spectral envelope)

It can also resynthesize speech using these features (see examples below).

For more information, please visit [Morise's World repository](https://github.com/mmorise/World) 
and the [official website of World Vocoder](http://ml.cs.yamanashi.ac.jp/world/english/)


## I. APIs

### Vocoder Functions
```python
import pyworld as pw
pyDioOpt = pw.pyDioOption()
_f0, t = pw.dio(x, fs)    # raw pitch extractor
f0 = pw.stonemask(x, _f0, t, fs)  # pitch refinement
sp = pw.cheaptrick(x, f0, t, fs)  # extract smoothed spectrogram
ap = pw.d4c(x, f0, t, fs)         # extract aperiodicity
y = pw.synthesize(f0, sp, ap, fs, pyDioOpt.option['frame_period'])
```


### Utility
```python
# Convert speech into features (using default options)
f0, sp, ap, pyDioOpt = pw.wav2world(x, fs)
```


## II. Installation
### Installation procedures
```bash
git clone https://github.com/JeremyCCHsu/Python-Wrapper-for-World-Vocoder.git
pip install -U pip
pip install -r requirements.txt
cd Python-Wrapper-for-World-Vocoder
bash download_vocoder.sh
python setup.py install
```
It will automatically `git clone` Morise's World Vocoder (C++ version).<br/>
Alternatively you can clone or download the World repository manually and copy its "src" directory to this repositories directory.<br/>
As for installation mode (the last line), you can choose from the following options.


### Installation Mode
1. If you want to "install" this package, try<br/>
   `python setup.py install`<br/>
   (add `--user` if you don't have root access)
2. If you just want to try out some experiments, execute<br/>
  `python setup.py build_ext --inplace`<br/>
  Then you can use PyWorld from this directory.<br/>
  You can also copy the resulting **pyworld.so** (pyworld.{arch}.pyd on Windows) file to
  `~/.local/lib/python2.7/site-packages` (or corresponding Windows directory)
  so that you can use it everywhere like an installed package.<br/>
  Alternatively you can copy/symlink the compiled files using pip, e.g. `pip install -e .`

### Environment/Dependencies  
- Linux Ubuntu 14.04/16.04, Windows
- Python 2.7/3.5
- Cython 0.24 (or later versions; required)
- Numpy

Optional (for demo.py only):  
- argparse
- librosa
- Matplotlib

You can simply install these by `pip install -r requirements.txt`


### Validation
You can validate installation by running
`python demo.py`
to see if you get results in `test/` direcotry.


## Troubleshooting
1. Upgrade your Cython version to 0.24.<br/>
   (I failed to build it on Cython 0.20.1post0)<br/>
   It'll require you to download Cython form http://cython.org/<br/>
   Unzip it, and `python setup.py install` it.<br/>
   (I tried `pip install Cython` but the upgrade didn't seem correct)<br/>
   (Again, add `--user` if you don't have root access.)
2. The following code might be needed in some configurations:

 ```python
 import matplotlib
 matplotlib.use('Agg')
 ```


## Note:
1. This wrapper is an updated version of sotelo's "world.py"<br/>
   https://github.com/sotelo/world.py

## Acknowledgement
Thank all contributors ([rikrd](https://github.com/rikrd), [wuaalb](https://github.com/wuaalb)) for making this repo better!

## TODO List
  
- [ ] Realtime synthesizer

