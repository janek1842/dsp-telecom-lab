# DFT experiments with self-implemented DFT and its comaprison with FFT

import numpy as np
import matplotlib.pyplot as plt

from numpy.fft import fft,ifft
from numpy import fft as numpyfft

def my_dft(x):
    X = np.zeros(len(x),dtype=complex)
    for n in range(len(x)):
        for k in range(len(x)):
            X[k] += x[n] * np.exp(-1j*(2*np.pi/len(x))*k*n)
    return X

fpr = 100 # sampling frequency
f = 3 # signal frequency
dt = 1/fpr # time steps
tmax=2 # signal time
t = np.linspace(0,tmax,fpr*tmax) # time domain
A = 2 # amplitude

x = A*np.sin(2*np.pi*f*t + np.pi/2) # signal
f_domain = np.linspace(0,fpr,fpr*tmax) # frequency domain
X = my_dft(x) # signal in frequency domain

# Plotting
plt.title('Signal x in time domain')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.plot(t,x,'o--')
plt.show()

plt.subplot(2,1,1)
plt.title('Signal x in frequency domain - my dft')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.xlim(0,10)
plt.stem(f_domain,np.real(X),'o--')
plt.subplots_adjust(wspace=1)
plt.subplots_adjust(hspace=1)

plt.subplot(2,1,2)
plt.title('Signal x in frequency domain - fft numpy')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.stem(f_domain,np.real((fft(x))),'o--')
plt.subplots_adjust(wspace=1)
plt.subplots_adjust(hspace=1)
plt.xlim(0,10)
plt.show()


