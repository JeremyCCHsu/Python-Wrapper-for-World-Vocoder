from __future__ import print_function
import pyworld as pw
import os
from shutil import rmtree
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--frame_rate", type=int, default=5)
parser.add_argument("-s", "--speed", type=int, default=1)

# =================================
SHORT_MAX = 32767
EPSILON = 1e-8
def wavread(filename):
    fs, x = read(filename)
    x = x.astype(np.float) / SHORT_MAX
    return x, fs


def wavwrite(filename, fs, y):
    ymax = np.max(np.abs(y))
    if ymax < 1.0:
        y = y * SHORT_MAX
    else:
        y = (y / ymax) * SHORT_MAX
    y = y.astype(np.int16)
    write(filename, fs, y)


def savefig(filename, figlist, log=True):
    h = 10
    n = len(figlist)
    # peek into instances
    f = figlist[0]
    if len(f.shape) == 1:
        plt.figure()
        for i, f in enumerate(figlist):
            plt.subplot(n, 1, i+1)
            if len(f.shape) == 1:
                plt.plot(f)
                plt.xlim([0, len(f)])
    elif len(f.shape) == 2:
        Nsmp, dim = figlist[0].shape
        figsize=(h * float(Nsmp) / dim, len(figlist) * h)
        plt.figure(figsize=figsize)
        for i, f in enumerate(figlist):
            plt.subplot(n, 1, i+1)
            if log:
                plt.imshow(np.log(f.T + EPSILON))
            else:
                plt.imshow(f.T + EPSILON)
    else:
        raise ValueError('Input dimension must < 3.')
    plt.savefig(filename)
# =================================


def main(args):
    if os.path.isdir('test'):
        rmtree('test')
    os.mkdir('test')

    x, fs = wavread('utterance/vaiueo2d.wav')

    # 1. A convient way
    f0, sp, ap, pyDioOpt = pw.wav2world(x, fs)    # use default options
    y = pw.synthesize(f0, sp, ap, fs, pyDioOpt.option['frame_period'])

    # 2. Step by step
    pyDioOpt = pw.pyDioOption(
        f0_floor=50,
        f0_ceil=600,
        channels_in_octave=2,
        frame_period=args.frame_rate,
        speed=args.speed)

    # 2-1 Without F0 refinement
    _f0, t = pw.dio(x, fs, pyDioOpt)
    _sp = pw.cheaptrick(x, _f0, t, fs)
    _ap = pw.d4c(x, _f0, t, fs)
    _y = pw.synthesize(_f0, _sp, _ap, fs, pyDioOpt.option['frame_period'])
    wavwrite('test/y_without_f0_refinement.wav', fs, _y)

    # 2-2 With F0 refinement (using stonemask)
    f0 = pw.stonemask(x, _f0, t, fs)
    sp = pw.cheaptrick(x, f0, t, fs)
    ap = pw.d4c(x, f0, t, fs)
    y = pw.synthesize(f0, sp, ap, fs, pyDioOpt.option['frame_period'])
    wavwrite('test/y_with_f0_refinement.wav', fs, y)

    # Comparison
    savefig('test/wavform.png', [x, _y, y])
    savefig('test/sp.png', [_sp, sp])
    savefig('test/ap.png', [_ap, ap], log=False)
    savefig('test/f0.png', [_f0, f0])

    print('Please check "test" directory for output files')


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
