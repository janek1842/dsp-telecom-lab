# FM modulation and demodulation
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft,ifft
from numpy import fft as numpyfft

Nx = 2000
fs = 2000
fc = 400
fm = 2
df=50
dt = 1/fs
t = dt * np.arange(0,Nx-1)
SNR_DB = 1

xm = np.sin(2*np.pi*fm*t) # Sygnal modulujacy
x = np.exp(1j*(2*np.pi*0*t + 2*np.pi*df/fs*np.cumsum(xm))) # sygnal zmodulowany (informacyjny) FM

c = np.cos(2*np.pi*fc*t)
s = np.sin(2*np.pi*fc*t)

# UP CONVERSION
xUp = x * (c+1j*s)
xUpReal = np.real(xUp)

# NOISE ADDITION
signal_power = np.mean(np.abs(xUpReal)**2)
noise_power = signal_power / (10**(SNR_DB / 10))
noise = np.sqrt(noise_power) * np.random.randn(len(x))

xUpReal += noise

# DOWN CONVERSION
xDown = 2*xUpReal*(c - 1j*s)

# LOWPASS FILTERING
X = np.fft.fftshift(fft(xDown))
f = np.linspace(-fs/2, fs/2, Nx-1)
H = np.abs(f) < fc/2      # filtr dolnoprzepustowy
Xf = X * H
xDownFilt = ifft(np.fft.ifftshift(Xf))

Error = np.max(abs(x-xDownFilt))
print(Error)

# TIME DOMAIN ANALYSIS
plt.subplot(211)
plt.plot(t,np.real(x), label="xOriginal")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.legend()

plt.subplot(212)
plt.plot(t,np.real(xDownFilt), label="xDownFilt")
plt.legend()
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()

# FREQUENCY DOMAIN ANALYSIS
f0=fs/Nx
k=np.arange(Nx-1)
fk=k*f0

xm = numpyfft.fftshift(fft(xm))
xDownFilt = numpyfft.fftshift(fft(xDownFilt))

plt.subplot(211)
plt.stem(fk,xm, label="xOriginal")
plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.legend()

plt.subplot(212)
plt.stem(fk,xDownFilt, label="xDownFilt")
plt.legend()
plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()