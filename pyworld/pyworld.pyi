from __future__ import division
from typing import Tuple
import numpy as np

default_frame_period = 5.0
default_f0_floor = 71.0
default_f0_ceil = 800.0


def dio(x: np.ndarray, fs: int,
        f0_floor: float = default_f0_floor, f0_ceil: float = default_f0_ceil,
        channels_in_octave: float = 2.0, frame_period: float = default_frame_period,
        speed: int = 1, allowed_range: float = 0.1) -> Tuple[np.ndarray, np.ndarray]:
    """DIO F0 extraction algorithm.

    Parameters
    ----------
    x : ndarray
        Input waveform signal.
    fs : int
        Sample rate of input signal in Hz.
    f0_floor : float
        Lower F0 limit in Hz.
        Default: 71.0
    f0_ceil : float
        Upper F0 limit in Hz.
        Default: 800.0
    channels_in_octave : float
        Resolution of multiband processing; normally shouldn't be changed.
        Default: 2.0
    frame_period : float
        Period between consecutive frames in milliseconds.
        Default: 5.0
    speed : int
        The F0 estimator may downsample the input signal using this integer factor
        (range [1;12]). The algorithm will then operate on a signal at fs/speed Hz
        to reduce computational complexity, but high values may negatively impact
        accuracy.
        Default: 1 (no downsampling)
    allowed_range : float
        Threshold for voiced/unvoiced decision. Can be any value >= 0, but 0.02 to 0.2
        is a reasonable range. Lower values will cause more frames to be considered
        unvoiced (in the extreme case of `threshold=0`, almost all frames will be unvoiced).
        Default: 0.1

    Returns
    -------
    f0 : ndarray
        Estimated F0 contour.
    temporal_positions : ndarray
        Temporal position of each frame.
    """


def harvest(x: np.ndarray, fs: int,
            f0_floor: float = default_f0_floor, f0_ceil: float = default_f0_ceil,
            frame_period: float = default_frame_period) -> Tuple[np.ndarray, np.ndarray]:
    """Harvest F0 extraction algorithm.

    Parameters
    ----------
    x : ndarray
        Input waveform signal.
    fs : int
        Sample rate of input signal in Hz.
    f0_floor : float
        Lower F0 limit in Hz.
        Default: 71.0
    f0_ceil : float
        Upper F0 limit in Hz.
        Default: 800.0
    frame_period : float
        Period between consecutive frames in milliseconds.
        Default: 5.0

    Returns
    -------
    f0 : ndarray
        Estimated F0 contour.
    temporal_positions : ndarray
        Temporal position of each frame.
    """


def stonemask(x: np.ndarray, d0: np.ndarray,
              temporal_positions: np.ndarray, fs: int) -> np.ndarray:
    """StoneMask F0 refinement algorithm.

    Parameters
    ----------
    x : ndarray
        Input waveform signal.
    f0 : ndarray
        Input F0 contour.
    temporal_positions : ndarray
        Temporal positions of each frame.
    fs : int
        Sample rate of input signal in Hz.

    Returns
    -------
    refined_f0 : ndarray
        Refined F0 contour.
    """


def get_cheaptrick_fft_size(fs: int, f0_floor: float = default_f0_floor) -> int:
    """Calculate suitable FFT size for CheapTrick given F0 floor.

    Parameters
    ----------
    fs : int
        Sample rate of input signal in Hz.
    f0_floor : float
        Lower F0 limit in Hz. The required FFT size is a direct
        consequence of the F0 floor used.
        Default: 71.0

    Returns
    -------
    fft_size : int
        Resulting FFT size.
    """


def get_cheaptrick_f0_floor(fs: int, fft_size: int) -> float:
    """Calculates actual lower F0 limit for CheapTrick
    based on the sampling frequency and FFT size used. Whenever F0 is below
    this threshold the spectrum will be analyzed as if the frame is unvoiced
    (using kDefaultF0 defined in constantnumbers.h).

    Parameters
    ----------
    fs : int
        Sample rate of input signal in Hz.
    fft_size : int
        FFT size used for CheapTrick.

    Returns
    -------
    f0_floor : float
        Resulting lower F0 limit in Hz.
    """


def cheaptrick(x: np.ndarray, f0: np.ndarray,
               temporal_positions: np.ndarray, fs: int,
               q1: float = -0.15, f0_floor: float = default_f0_floor,
               fft_size: int | None = None) -> np.ndarray:
    """CheapTrick harmonic spectral envelope estimation algorithm.

    Parameters
    ----------
    x : ndarray
        Input waveform signal.
    f0 : ndarray
        Input F0 contour.
    temporal_positions : ndarray
        Temporal positions of each frame.
    fs : int
        Sample rate of input signal in Hz.
    q1 : float
        Spectral recovery parameter.
        Default: -0.15 (this value was tuned and normally does not need adjustment)
    f0_floor : float, None
        Lower F0 limit in Hz. Not used in case `fft_size` is specified.
        Default: 71.0
    fft_size : int, None
        FFT size to be used. When `None` (default) is used, the FFT size is computed
        automatically as a function of the given input sample rate and F0 floor.
        When `fft_size` is specified, the given `f0_floor` parameter is ignored.
        Default: None

    Returns
    -------
    spectrogram : ndarray
        Spectral envelope (squared magnitude).
    """


def d4c(x: np.ndarray, f0: np.ndarray,
        temporal_positions: np.ndarray, fs: int,
        threshold: float = 0.85, fft_size: int | None = None) -> np.ndarray:
    """D4C aperiodicity estimation algorithm.

    Parameters
    ----------
    x : ndarray
        Input waveform signal.
    f0 : ndarray
        Input F0 contour.
    temporal_positions : ndarray
        Temporal positions of each frame.
    fs : int
        Sample rate of input signal in Hz.
    q1 : float
        Spectral recovery parameter.
        Default: -0.15 (this value was tuned and normally does not need adjustment)
    threshold : float
        Threshold for aperiodicity-based voiced/unvoiced decision, in range 0 to 1.
        If a value of 0 is used, voiced frames will be kept voiced. If a value > 0 is
        used some voiced frames can be considered unvoiced by setting their aperiodicity
        to 1 (thus synthesizing them with white noise). Using `threshold=0` will result
        in the behavior of older versions of D4C. The current default of 0.85 is meant
        to be used in combination with the Harvest F0 estimator, which was designed to have
        a high voiced/unvoiced threshold (i.e. most frames will be considered voiced).
        Default: 0.85
    fft_size : int, None
        FFT size to be used. When `None` (default) is used, the FFT size is computed
        automatically as a function of the given input sample rate and the default F0 floor.
        When `fft_size` is specified, it should match the FFT size used to compute
        the spectral envelope (i.e. `fft_size=2*(sp.shape[1] - 1)`) in order to get the
        desired results when resynthesizing.
        Default: None

    Returns
    -------
    aperiodicity : ndarray
        Aperiodicity (envelope, linear magnitude relative to spectral envelope).
    """


def synthesize(f0: np.ndarray, spectrogram: np.ndarray,
               aperiodicity: np.ndarray, fs: int,
               frame_period: float = default_frame_period) -> np.ndarray:
    """WORLD synthesis from parametric representation.

    Parameters
    ----------
    f0 : ndarray
        Input F0 contour.
    spectrogram : ndarray
        Spectral envelope.
    aperiodicity : ndarray
        Aperodicity envelope.
    fs : int
        Sample rate of input signal in Hz.
    frame_period : float
        Period between consecutive frames in milliseconds.
        Default: 5.0

    Returns
    -------
    y : ndarray
        Output waveform signal.
    """


def get_num_aperiodicities(fs: int) -> int:
    """Calculate the required dimensionality to code D4C aperiodicity.

    Parameters
    ----------
    fs : int
        Sample rate of input signal in Hz.

    Returns
    -------
    n_aper : int
        Required number of coefficients.
    """


def code_aperiodicity(aperiodicity: np.ndarray, fs: int) -> int:
    """Reduce dimensionality of D4C aperiodicity.

    Parameters
    ----------
    aperiodicity : ndarray
        Aperodicity envelope.
    fs : int
        Sample rate of input signal in Hz.

    Returns
    -------
    coded_aperiodicity : ndarray
        Coded aperiodicity envelope.
    """


def decode_aperiodicity(coded_aperiodicity: np.ndarray,
                        fs: int, fft_size: int) -> np.ndarray:
    """Restore full dimensionality of coded D4C aperiodicity.

    Parameters
    ----------
    coded_aperiodicity : ndarray
        Coded aperodicity envelope.
    fs : int
        Sample rate of input signal in Hz.
    fft_size : int
        FFT size corresponding to the full dimensional aperiodicity.

    Returns
    -------
    aperiodicity : ndarray
        Aperiodicity envelope.
    """


def code_spectral_envelope(spectrogram: np.ndarray, fs: int,
                           number_of_dimensions: int) -> np.ndarray:
    """Reduce dimensionality of spectral envelope.

    Parameters
    ----------
    spectrogram : ndarray
        Spectral envelope.
    fs : int
        Sample rate of input signal in Hz.
    number_of_dimensions : int
        Number of dimentions of coded spectral envelope

    Returns
    -------
    coded_spectral_envelope : ndarray
        Coded spectral envelope.
    """


def decode_spectral_envelope(coded_spectral_envelope: np.ndarray,
                             fs: int, fft_size: int) -> np.ndarray:
    """Restore full dimensionality of coded spectral envelope.

    Parameters
    ----------
    coded_spectral_envelope : ndarray
        Coded spectral envelope.
    fs : int
        Sample rate of input signal in Hz.
    fft_size : int
        FFT size corresponding to the full dimensional spectral envelope.

    Returns
    -------
    spectrogram : ndarray
        Spectral envelope.
    """


def wav2world(x: np.ndarray, fs: int, fft_size: int | None = None,
              frame_period: float = default_frame_period) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Convenience function to do all WORLD analysis steps in a single call.

    In this case only `frame_period` can be configured and other parameters
    are fixed to their defaults. Likewise, F0 estimation is fixed to
    DIO plus StoneMask refinement.

    Parameters
    ----------
    x : ndarray
        Input waveform signal.
    fs : int
        Sample rate of input signal in Hz.
    frame_period : float
        Period between consecutive frames in milliseconds.
        Default: 5.0
    fft_size : int
        Length of Fast Fourier Transform (in number of samples)
        The resulting dimension of `ap` adn `sp` will be `fft_size` // 2 + 1

    Returns
    -------
    f0 : ndarray
        F0 contour.
    sp : ndarray
        Spectral envelope.
    ap : ndarray
        Aperiodicity.
    """
