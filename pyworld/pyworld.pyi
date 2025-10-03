# PyWorld type stub
from typing import Tuple

import numpy as np
from numpy.typing import NDArray


def wav2world(
    x: NDArray[np.float64],
    fs: int,
    frame_period: float = 5.0,
    f0_floor: float = 71.0,
    f0_ceil: float = 800.0,
) -> Tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]: ...


def synthesize(
    f0: NDArray[np.float64],
    spectrogram: NDArray[np.float64],
    aperiodicity: NDArray[np.float64],
    fs: int,
    frame_period: float = 5.0,
) -> NDArray[np.float64]: ...


def dio(
    x: NDArray[np.float64],
    fs: int,
    f0_floor: float = 71.0,
    f0_ceil: float = 800.0,
    channels_in_octave: float = 2.0,
    frame_period: float = 5.0,
    speed: int = 1,
) -> Tuple[NDArray[np.float64], NDArray[np.float64]]: ...


def stonemask(
    x: NDArray[np.float64],
    f0: NDArray[np.float64],
    temporal_positions: NDArray[np.float64],
    fs: int,
) -> NDArray[np.float64]: ...


def cheaptrick(
    x: NDArray[np.float64],
    f0: NDArray[np.float64],
    temporal_positions: NDArray[np.float64],
    fs: int,
    q1: float = -0.15,
    f0_floor: float = 71.0,
    fft_size: int = 2048,
) -> NDArray[np.float64]: ...


def d4c(
    x: NDArray[np.float64],
    f0: NDArray[np.float64],
    temporal_positions: NDArray[np.float64],
    fs: int,
    threshold: float = 0.85,
    fft_size: int = 2048,
) -> NDArray[np.float64]: ...