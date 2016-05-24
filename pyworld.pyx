import cython
from libc.stdlib cimport free
from cpython cimport PyObject, Py_INCREF, array

import numpy as np
cimport numpy as np
np.import_array()

# Notice: wavread and wavwrite is removed form world.
# [TODO] It seems that I can't specify fft_size from outside?

cdef extern from "src/world/synthesis.h":
    void Synthesis(const double *f0, 
        int f0_length, double** spectrogram, 
        double** aperiodicity, 
        int fft_size, double frame_period, 
        int fs, int y_length, double *y)

    
cdef extern from "src/world/cheaptrick.h":
    ctypedef struct CheapTrickOption:
        double q1
        double f0_floor

    int GetFFTSizeForCheapTrick(int fs, const CheapTrickOption *option)
    void InitializeCheapTrickOption(CheapTrickOption *option)
    void CheapTrick(const double *x, int x_length, int fs, const double *time_axis,
        const double *f0, int f0_length, const CheapTrickOption *option,
        double **spectrogram)


cdef extern from "src/world/dio.h":
    ctypedef struct DioOption:
        double f0_floor
        double f0_ceil
        double channels_in_octave
        double frame_period
        int speed
        double allowed_range

    void InitializeDioOption(DioOption *option)
    
    int GetSamplesForDIO(int fs, int x_length, double frame_period)
    void Dio(const double *x, int x_length, int fs, const DioOption *option,
        double *time_axis, double *f0)


cdef extern from "src/world/d4c.h":
    ctypedef struct D4COption:
        double dummy
    
    void InitializeD4COption(D4COption *option)
    void D4C(const double *x, int x_length, int fs, const double *time_axis,
        const double *f0, int f0_length, int fft_size, const D4COption *option,
        double **aperiodicity) 


cdef extern from "src/world/stonemask.h":
    void StoneMask(const double *x, int x_length, int fs, 
        const double *time_axis, const double *f0, int f0_length, 
        double *refined_f0)


class pyDioOption:
    ''' DioOption '''
    def __init__(self, f0_floor=71, f0_ceil=800, 
        channels_in_octave=2.0, frame_period=5, speed=1, allowed_range=0.1):
        cdef DioOption option
        InitializeDioOption(&option)
        option.channels_in_octave = channels_in_octave
        option.f0_floor = f0_floor
        option.f0_ceil = f0_ceil
        option.frame_period = frame_period
        option.speed = speed
        self.option = option


def dio(
    np.ndarray[double, ndim=1, mode="c"] x not None, 
    int fs, 
    pyDioOpt):
    ''' Raw Pitch (F0) extractor '''
    x_length = len(x)
    cdef DioOption dioOption = pyDioOpt.option
    f0_length = GetSamplesForDIO(fs, x_length, dioOption.frame_period)
    cdef np.ndarray[double, ndim=1, mode="c"] f0 = \
        np.zeros(f0_length, dtype = np.dtype('float64'))
    cdef np.ndarray[double, ndim=1, mode="c"] time_axis = \
        np.zeros(f0_length, dtype = np.dtype('float64'))
    Dio(&x[0], x_length, fs, &dioOption, &time_axis[0], &f0[0])
    return f0, time_axis


def stonemask(
    np.ndarray[double, ndim=1, mode="c"] x not None, 
    np.ndarray[double, ndim=1, mode="c"] f0 not None, 
    np.ndarray[double, ndim=1, mode="c"] time_axis not None, 
    int fs):
    ''' Pitch (F0) refinement '''
    cdef int x_length = len(x)
    cdef int f0_length = len(f0)
    cdef np.ndarray[double, ndim=1, mode="c"] refined_f0 = \
        np.zeros(f0_length, dtype = np.dtype('float64'))
    StoneMask(&x[0], x_length, fs, &time_axis[0],
        &f0[0], f0_length, &refined_f0[0])
    return refined_f0


def cheaptrick(
    np.ndarray[double, ndim=1, mode="c"] x not None, 
    np.ndarray[double, ndim=1, mode="c"] f0 not None,
    np.ndarray[double, ndim=1, mode="c"] time_axis not None,
    int fs):
    ''' STRAIGHT spectrum '''
    cdef CheapTrickOption option
    InitializeCheapTrickOption(&option)
    cdef int x_length = len(x)
    cdef int f0_length = len(f0)
    cdef int fft_size = GetFFTSizeForCheapTrick(fs, &option)

    cdef double[:,::1] spectrogram = np.zeros((f0_length, fft_size/2+1))
    cdef np.intp_t[:] tmp = np.zeros(f0_length, dtype=np.intp)
    cdef double **cpp_spectrogram = <double**> (<void*> &tmp[0])
    cdef np.intp_t i
    for i in range(f0_length):
        cpp_spectrogram[i] = &spectrogram[i, 0]

    CheapTrick(&x[0], x_length, fs, &time_axis[0],
        &f0[0], f0_length, &option, cpp_spectrogram)
    return np.array(spectrogram, dtype=np.float64)


def d4c(
    np.ndarray[double, ndim=1, mode="c"] x not None, 
    np.ndarray[double, ndim=1, mode="c"] f0 not None,
    np.ndarray[double, ndim=1, mode="c"] time_axis not None,
    int fs):
    ''' Aperiodicity Estimation '''
    cdef int x_length = len(x)
    cdef int f0_length = len(f0)
    cdef CheapTrickOption opt
    InitializeCheapTrickOption(&opt)
    cdef int fft_size = GetFFTSizeForCheapTrick(fs, &opt)

    cdef D4COption option
    InitializeD4COption(&option)

    cdef double[:,::1] aperiodicity = np.zeros((f0_length, fft_size/2+1))
    cdef np.intp_t[:] tmp = np.zeros(f0_length, dtype=np.intp)
    cdef double **cpp_aperiodicity = <double**> (<void*> &tmp[0])
    cdef np.intp_t i
    for i in range(f0_length):
        cpp_aperiodicity[i] = &aperiodicity[i, 0]

    D4C(&x[0], x_length, fs, &time_axis[0],
        &f0[0], f0_length, fft_size, &option,
        cpp_aperiodicity) 
    return np.array(aperiodicity, dtype=np.float64)


def synthesize(
    np.ndarray[double, ndim=1, mode="c"] f0 not None,
    np.ndarray[double, ndim=2, mode="c"] np_spectrogram not None,
    np.ndarray[double, ndim=2, mode="c"] np_aperiodicity not None,
    int fs,
    double frame_period):
    ''' Synthesizer '''
    cdef int f0_length = len(f0)
    y_length = int(f0_length * frame_period * fs / 1000)
    # cdef int fft_size = GetFFTSizeForCheapTrick(fs)
    cdef int fft_size = (np_spectrogram.shape[1] - 1)*2
    cdef np.ndarray[double, ndim=1, mode="c"] y = \
        np.zeros(y_length, dtype = np.dtype('float64'))

    cdef double[:,::1] spectrogram = np_spectrogram
    cdef double[:,::1] aperiodicity = np_aperiodicity
    cdef np.intp_t[:] tmp = np.zeros(f0_length, dtype=np.intp)
    cdef np.intp_t[:] tmp2 = np.zeros(f0_length, dtype=np.intp)
    cdef double **cpp_spectrogram = <double**> (<void*> &tmp[0])
    cdef double **cpp_aperiodicity = <double**> (<void*> &tmp2[0])
    cdef np.intp_t i
    for i in range(f0_length):
        cpp_spectrogram[i] = &spectrogram[i,0]
        cpp_aperiodicity[i] = &aperiodicity[i,0]

    Synthesis(&f0[0], f0_length, cpp_spectrogram, 
        cpp_aperiodicity, fft_size, frame_period, fs, y_length, &y[0])
    return y


def wav2world(x, fs, pyDioOpt=None):
    if pyDioOpt is None:
        pyDioOpt = pyDioOption()
    _f0, t = dio(x, fs, pyDioOpt)
    f0 = stonemask(x, _f0, t, fs)
    sp = cheaptrick(x, f0, t, fs)
    ap = d4c(x, f0, t, fs)
    return f0, sp, ap, pyDioOpt
