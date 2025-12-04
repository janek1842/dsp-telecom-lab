# FM modulation and demodulation
from numpy import unwrap
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft,ifft
from numpy import fft as numpyfft

# Modulation
A = 5
f = 2
fs = 20000
dt = 1/fs
Nx = 20000
f0=fs/Nx
k=np.arange(Nx-1)
fk=k*f0

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

# FM modulation
fc = 4000
BW = 1 * fc
df = 10 # MODULATION DEPTH
y = np.exp(1j*2*np.pi*(fc*t + df*np.cumsum(x) * dt ))

# Modulated signal
plt.figure()
plt.plot(t,y, label="yModulated")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.legend()

plt.grid(True)

# FM demodulation
ang = unwrap(np.angle(y))
fi1 = np.diff(ang) / (2*np.pi*dt)
xest = (fi1 - fc)/df
xmest = (fft(xest))

# Demodulated signal
plt.figure()
plt.tight_layout()

plt.subplot(211)
plt.plot(t[1:],(xest), label="xDemodulated")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)

plt.subplot(212)
plt.stem(fk[0:len(xmest)],np.real(xmest), label="xDemodulated")
plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.xlim(0,3)
plt.legend()
plt.show()
