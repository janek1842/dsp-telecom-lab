# AM modulation and demodulation

from numpy import unwrap
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft,ifft
from numpy import fft as numpyfft
from commpy.channels import awgn
from scipy.signal import butter, filtfilt

# Modulation
A = 5
f = 2
fs = 20000
dt = 1/fs
Nx = 20000
f0=fs/Nx
k=np.arange(Nx-1)
fk=k*f0
SNR = 200

t = dt * np.arange(0,Nx-1)
x = A * np.cos(2*np.pi*f*t)
xm = (fft(x))

# Original signal
plt.subplot(211)
plt.plot(t,x, label="xOriginal")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)

plt.subplot(212)
plt.stem(fk,np.real(xm), label="xOriginal")
plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.xlim(0,3)
plt.legend()
plt.show()

# AM modulation
fc = 4000
c = np.exp(1j*2*np.pi*fc*t)
y = np.real(x) * np.real(c)  - np.imag(x)*np.imag(c)

# Modulated signal
plt.figure()
plt.plot(t,y, label="yModulated")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)
plt.show()

# Noise addition and demodulation
y = awgn(y,SNR)
a1 = 2*y*np.real(c) - 2*1j*y*np.imag(c)
xdem = np.real(a1)

b, a = butter(4, 10/fs)  # normalized cutoff = 10 Hz
xdem = filtfilt(b, a, xdem) * 2   # scale factor 2 is required

# Original signal
plt.subplot(211)
plt.plot(t,xdem, label="xDemod")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)

plt.subplot(212)
plt.stem(fk,np.real(fft(xdem)), label="xDemod")
plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.xlim(0,3)
plt.legend()
plt.show()