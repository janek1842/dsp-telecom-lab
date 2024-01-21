import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from mylib import myDFT

# loads samples from .wav file with exemplary DTFM signal
# adapt file path 
samples = read(r'wav\a.wav')
sampling_freq = samples[0]
samples = samples[1]
samples = samples[:1024]
plt.plot(samples)

# use comments to switch between myDTF and numpy DTF (FFT)
normalized_samples = (samples - np.mean(samples))
freq_np = np.linspace(0, sampling_freq, len(normalized_samples))

real, imag = myDFT(normalized_samples)



# Convert lists to NumPy arrays
real = np.array(real)
imag = np.array(imag)
magnitudes = np.sqrt(real**2 + imag**2)

print(len(magnitudes))

plt.figure(1)
plt.plot(freq_np, magnitudes, label='Amplitudes')
plt.title('Amplitudes of Sinusoidal Components - a.wav')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.grid()
plt.legend()
plt.xlim(0, 1500)

plt.show()