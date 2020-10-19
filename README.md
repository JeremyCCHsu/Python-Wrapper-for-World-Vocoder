# PyWORLD - A Python wrapper of WORLD Vocoder


| **`Linux`** | **`Windows`** |
|-----------------|-----------|
| [![Build Status](https://travis-ci.org/JeremyCCHsu/Python-Wrapper-for-World-Vocoder.svg?branch=master)](https://travis-ci.org/JeremyCCHsu/Python-Wrapper-for-World-Vocoder) | [![Build Status](https://ci.appveyor.com/api/projects/status/github/JeremyCCHsu/Python-Wrapper-for-World-Vocoder?svg=true)](https://ci.appveyor.com/project/JeremyCCHsu/python-wrapper-for-world-vocoder) |


WORLD Vocoder is a fast and high-quality vocoder
which parameterizes speech into three components:

  1. `f0`: Pitch contour
  2. `sp`: Harmonic spectral envelope
  3. `ap`: Aperiodic spectral envelope (relative to the harmonic spectral envelope)

It can also (re)synthesize speech using these features (see examples below).

For more information, please visit Dr. Morise's [WORLD repository](https://github.com/mmorise/World)
and the [official website of WORLD Vocoder](http://ml.cs.yamanashi.ac.jp/world/english)


## APIs

### Vocoder Functions
```python
import pyworld as pw
_f0, t = pw.dio(x, fs)    # raw pitch extractor
f0 = pw.stonemask(x, _f0, t, fs)  # pitch refinement
sp = pw.cheaptrick(x, f0, t, fs)  # extract smoothed spectrogram
ap = pw.d4c(x, f0, t, fs)         # extract aperiodicity

y = pw.synthesize(f0, sp, ap, fs) # synthesize an utterance using the parameters
```


### Utility
```python
# Convert speech into features (using default arguments)
f0, sp, ap = pw.wav2world(x, fs)
```
<br/>

You can change the default arguments of the function, too. 
See more info using `help`.


## Installation

### Using Pip
`pip install pyworld`  
<br/>

### Building from Source
```bash
git clone https://github.com/JeremyCCHsu/Python-Wrapper-for-World-Vocoder.git
cd Python-Wrapper-for-World-Vocoder
git submodule update --init
pip install -U pip
pip install -r requirements.txt
pip install .
```
It will automatically `git clone` Morise's World Vocoder (C++ version).<br/>
(It seems to me that using `virtualenv` or `conda` is the best practice.)<br/>
<br/>

### Installation Validation
You can validate installation by running
```bash
cd demo
python demo.py
```
to see if you get results in `test/` direcotry.
(Please avoid writing and executing codes in the `Python-Wrapper-for-World-Vocoder` folder for now.)<br/>

### Environment/Dependencies  
- Operating systems 
  - Linux Ubuntu 14.04+
  - Windows (thanks to [wuaalb](https://github.com/wuaalb))
  - WSL
- Python
  - 2.7 (Windows is currently not supported)
  - 3.7/3.6/3.5

You can install dependencies these by `pip install -r requirements.txt`



## Notice
- WORLD vocoder is designed for speech sampled ≥ 16 kHz.
  Applying WORLD to 8 kHz speech will fail.
  See a possible workaround [here](https://github.com/JeremyCCHsu/Python-Wrapper-for-World-Vocoder/issues/54).
- When the SNR is low, extracting pitch using `harvest` instead of `dio` 
  is a better option.


## Troubleshooting
1. Upgrade your Cython version to 0.24.<br/>
   (I failed to build it on Cython 0.20.1post0)<br/>
   It'll require you to download Cython form http://cython.org/<br/>
   Unzip it, and `python setup.py install` it.<br/>
   (I tried `pip install Cython` but the upgrade didn't seem correct)<br/>
   (Again, add `--user` if you don't have root access.)
2. Upon executing `demo/demo.py`, the following code might be needed in some environments (e.g. when you're working on a remote Linux server):<br/>

 ```python
 import matplotlib
 matplotlib.use('Agg')
 ```
3. If you encounter `library not found: sndfile` error upon executing `demo.py`,  
   you might have to install it by `apt-get install libsoundfile1`.  
   You can also replace `pysoundfile` with `scipy` or `librosa`, but some modification is needed:   
   - librosa:
     - load(fiilename, dtype=np.float64)
     - output.write_wav(filename, wav, fs)
     - remember to pass `dtype` argument to ensure that the method gives you a `double`.
   - scipy:
     - You'll have to write a customized utility function based on the following methods
     - scipy.io.wavfile.read (but this gives you `short`)
     - scipy.io.wavfile.write

4. If you have installation issue on Windows, I probably could not provide 
   much help because my development environment is Ubuntu 
   and Windows Subsystem for Linux ([read this if you are interested in installing it](https://github.com/JeremyCCHsu/wsl)).


### Other Installation Suggestions
1. Use `pip install .` is safer and you can easily uninstall pyworld by `pip uninstall pyworld`
  - For Mac users: You might need to do `MACOSX_DEPLOYMENT_TARGET=10.9 pip install .` See [issue](https://github.com/SeanNaren/warp-ctc/issues/129#issuecomment-502349652).
2. Another way to install pyworld is via<br/>
   `python setup.py install`<br/>
   - Add `--user` if you don't have root access<br/>
   - Add `--record install.txt` to track the installation dir<br/>
3. If you just want to try out some experiments, execute<br/>
  `python setup.py build_ext --inplace`<br/>
  Then you can use PyWorld from this directory.<br/>
  You can also copy the resulting **pyworld.so** (pyworld.{arch}.pyd on Windows) file to
  `~/.local/lib/python2.7/site-packages` (or corresponding Windows directory)
  so that you can use it everywhere like an installed package.<br/>
  Alternatively you can copy/symlink the compiled files using pip, e.g. `pip install -e .`



## Acknowledgement
Thank all contributors ([tats-u](https://github.com/tats-u), [wuaalb](https://github.com/wuaalb), [r9y9](https://github.com/r9y9), [rikrd](https://github.com/rikrd), [kudan2510](https://github.com/kundan2510)) for making this repo better and [sotelo](https://github.com/sotelo) whose [world.py](https://github.com/sotelo/world.py) inspired this repo.<br/>
