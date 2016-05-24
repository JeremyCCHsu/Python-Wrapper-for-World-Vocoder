import pyworld as pw
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write

# =================================
SHORT_MAX = 32767
EPSILON = 1e-10
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

def savefig(filename, figlist):
    n = len(figlist)
    plt.figure()
    for i, f in enumerate(figlist):
        plt.subplot(n, 1, i+1)
        if f.shape == 1:
            plt.plot(x)
        elif f.shape == 2:
            plt.imshow(np.log(ap.T + EPSILON))
    plt.savefig(filename)
# =================================


x, fs = wavread('test/vaiueo2d.wav')


# 1. A convient way
f0, sp, ap, pyDioOpt = pw.wav2world(x, fs)    # use default options
y = pw.synthesize(f0, sp, ap, fs, pyDioOpt.option['frame_period'])


# 2. Step by step
pyDioOpt = pw.pyDioOption(
    f0_floor=50, 
    f0_ceil=600, 
    channels_in_octave=2,
    frame_period=5, 
    speed=1)


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
savefig('test/ap.png', [_ap, ap])
savefig('test/f0.png', [_f0, f0])

print 'Please check "test" directory for output files'

# # Plots
# plt.figure()
# plt.subplot(3, 1, 1)
# plt.plot(x)
# plt.subplot(3, 1, 2)
# plt.plot(_y)
# plt.subplot(3, 1, 3)
# plt.plot(y)
# plt.savefig('test-wavform.png')

# plt.figure()
# plt.subplot(1, 2, 1)
# plt.imshow(np.log(_sp.T + 1e-10))
# plt.subplot(1, 2, 2)
# plt.imshow(np.log(sp.T + 1e-10))
# plt.savefig('test-sp.png')

# plt.figure()
# plt.subplot(1, 2, 1)
# plt.imshow(np.log(_ap.T + 1e-10))
# plt.subplot(1, 2, 2)
# plt.imshow(np.log(ap.T + 1e-10))
# plt.savefig('test-ap.png')

# plt.figure()
# plt.plot(_f0)
# plt.plot(f0)
# plt.savefig('test-f0-cmp.png')
