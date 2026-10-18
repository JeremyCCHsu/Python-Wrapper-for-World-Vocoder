"""Read-only feature arrays remain valid inputs to the native speech functions."""
import unittest

import numpy as np
import pyworld as pw

class TestReadOnlyInputs(unittest.TestCase):
    def setUp(self):
        self.fs = 22050
        self.fft_size = 1024
        self.f0 = np.full(5, 200.0)
        self.spectrogram = np.ones((5, self.fft_size // 2 + 1))
        self.aperiodicity = np.full_like(self.spectrogram, 0.1)

    def check_readonly(self, function, arguments, positions):
        arguments = list(arguments)
        originals = [(i, arguments[i].copy()) for i in positions]
        expected = function(*arguments)
        for i in positions:
            arguments[i] = arguments[i].view()
            arguments[i].flags.writeable = False
        actual = function(*arguments)
        np.testing.assert_array_equal(actual, expected)
        for i, original in originals:
            np.testing.assert_array_equal(arguments[i], original)
            self.assertFalse(arguments[i].flags.writeable)

    def test_synthesis_with_readonly_f0(self):
        self.check_readonly(pw.synthesize, (self.f0, self.spectrogram, self.aperiodicity, self.fs), [0])

    def test_synthesis_with_readonly_spectral_envelope(self):
        self.check_readonly(pw.synthesize, (self.f0, self.spectrogram, self.aperiodicity, self.fs), [1])

    def test_synthesis_with_readonly_aperiodicity(self):
        self.check_readonly(pw.synthesize, (self.f0, self.spectrogram, self.aperiodicity, self.fs), [2])

    def test_synthesis_with_all_inputs_readonly(self):
        self.check_readonly(pw.synthesize, (self.f0, self.spectrogram, self.aperiodicity, self.fs), [0, 1, 2])

    def test_code_aperiodicity_with_readonly_input(self):
        self.check_readonly(pw.code_aperiodicity, (self.aperiodicity, self.fs), [0])

    def test_decode_aperiodicity_with_readonly_input(self):
        coded = pw.code_aperiodicity(self.aperiodicity, self.fs)
        self.check_readonly(pw.decode_aperiodicity, (coded, self.fs, self.fft_size), [0])

    def test_code_spectral_envelope_with_readonly_input(self):
        self.check_readonly(pw.code_spectral_envelope, (self.spectrogram, self.fs, 24), [0])

    def test_decode_spectral_envelope_with_readonly_input(self):
        coded = pw.code_spectral_envelope(self.spectrogram, self.fs, 24)
        self.check_readonly(pw.decode_spectral_envelope, (coded, self.fs, self.fft_size), [0])


if __name__ == '__main__':
    unittest.main()
