from scipy.signal import butter, lfilter, hilbert
import numpy as np
from numpy.fft import fft, ifft
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import soundfile as sf


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    return butter(order, [low, high], btype='band')

def apply_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    return lfilter(b, a, data)

# ---------------------------------------------
# READ THE NOISY, MODULATED SIGNAL
noisy_audio, fs = sf.read("D:\\ITC Recruitment\\ERC\\Convener_assignment_resources\\signal\\modulated_noisy_audio.wav")
dt = 1/fs
N_audio = len(noisy_audio)
time_axis = np.arange(0, N_audio*dt, dt)


# ----------------------------------------------
# APPLY FFT
freq_spectrum = np.abs(fft(noisy_audio))
N_freq = len(freq_spectrum)
freq_axis = np.arange(0.0, N_freq, 1.0)
freq_axis *= (fs/N_freq)

# IGNORE HALF OF THE FREQUENCY SPECTRUM (IN ACCORDANCE WITH NYQUIST-SHANNON SAMPLING THEOREM)
max_freq_index = np.where(freq_axis >= 0.5*fs)[0][0]
freq_axis = freq_axis[:max_freq_index]
freq_spectrum = freq_spectrum[:max_freq_index]

# PLOT THE FREQUENCY SPECTRUM
plt.subplots_adjust(hspace = 0.5, wspace = 0.6)
plt.subplot(3,1,1)
plt.plot(freq_axis, freq_spectrum)
plt.title("Frequncy Spectrum (before demodulation)")

# WE CAN SEE FROM THE FREQUENCY SPECTRUM THAT THE CARRIER FREQUENCY IS ROUGHLY 10000Hz
fc = 10000


# -----------------------------------------------
# DEMODULATING THE SIGNAL
analytic_signal = hilbert(noisy_audio)
audio_demod = np.abs(analytic_signal)


# -------------------------------------------------
# APPLYING BANDPASS FILTER TO GET RID OF NOISE IN THE SIGNAL
filtered = apply_bandpass_filter(audio_demod, 800, 1800, 44100, 5)
filtered /= np.max(np.abs(filtered)) # Normalize the filtered signal
plt.subplot(3,1,2)
plt.plot(time_axis, filtered)
plt.title("Time-domain filtered signal")


# PLOTTING THE FREQUENCY SPECTRUM OF THE FINAL FILTERED SIGNAL
freq_filtered = np.abs(fft(filtered))
N_freq_filtered = len(freq_filtered)
freq_axis_filtered = np.arange(0.0, N_freq_filtered, 1.0)
freq_axis_filtered *= (fs/N_freq_filtered)

freq_axis_filtered = freq_axis_filtered[:max_freq_index]
freq_filtered = freq_filtered[:max_freq_index]

plt.subplot(3,1,3)
plt.plot(freq_axis_filtered[:15000], freq_filtered[:15000])
plt.title("Frequency spectrum of filtered signal")
plt.show()


# --------------------------------------------------
# SAVE THE FILTERED SIGNAL TO AUDIO FILE
sf.write("D:\\ITC Recruitment\\ERC\\Convener_assignment_resources\\signal\\filtered_audio.wav", filtered, fs)
