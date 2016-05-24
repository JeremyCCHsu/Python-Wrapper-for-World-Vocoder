#PyWorldVocoder<br/>A Python wrapper for World Vocoder

Morise's World Vocoder is a fast and high-quality vocoder.
World Vocoder parameterizes speech into three components:
  1. Pitch (fundamental frequency, F0) contour
  2. smoothed spectrogram
  3. aperiodicity

It can also resynthesize speech using these features.

For more information, please visit Morise's Github repository:<br/>
  https://github.com/mmorise/World <br/>
  And the official website of World Vocoder:<br/>
  http://ml.cs.yamanashi.ac.jp/world/english/


##APIs

###Vocoder Functions
```
import pyworld as pw
pyDioOpt = pw.pyDioOption()
_f0, t = pw.dio(x, fs)    # raw pitch extractor
f0 = pw.stonemask(x, _f0, t, fs)  # pitch refinement
sp = pw.cheaptrick(x, f0, t, fs)  # extract smoothed spectrogram
ap = pw.d4c(x, f0, t, fs)         # extract aperiodicity
y = pw.synthesize(f0, sp, ap, fs, pyDioOpt.option['frame_period'])
```


###Utility
```
# Convert speech into features (using default options)
f0, sp, ap, pyDioOpt = pw.wav2world(x, fs)
```

## Installation
Linux Ubuntu 14.04 <br/>
Python 2.7.6 on <br/>
Cython 0.24 is required

**Prerequisite**: <br/>
1. Please `git clone` Morise's World (C++ version) first (https://github.com/mmorise/World)

2. Then `git clone` this repository, and move all the files to the directory of World.


**If you just want to try out some experiments:** <br/>
1. Execute <br/>
  `python setup.py build_ext --inplace` <br/>
  Then you can use PyWorld from this directory.

2. You can also copy the resulting **pyworld.so** file to<br/>
  `~/.local/lib/python2.7/site-packages` <br/>
  so that you can use it everywhere like an installed package.


**If you want to "install" this package, try <br/>**
  `python setup.py install`


Hint:
  1. add `--user` if you don't have root access
  2. If you want to uninstall PyWorld, just remove the pyworld files from the installation directory.
  3. You can validate installation by running<br/>
    `python demo.py`<br/>
     to see if you get results in the `test/` direcotry.

## Troubleshooting
1. Upgrade your Cython version to 0.24.<br/>
   (I failed to build it on Cython 0.20.1post0)<br/>
   It'll require you to download Cython form http://cython.org/ <br/>
   Unzip it, and `python setup.py install` it.<br/>
   (I tried `pip install Cython` but the upgrade didn't seem correct)<br/>
   (Again, add `--user` if you don't have root access.)


## Note:
1. This wrapper is an updated version of sotelo's "world.py"<br/>
  https://github.com/sotelo/world.py

## TODO List
  - [ ] Realtime synthesizer
