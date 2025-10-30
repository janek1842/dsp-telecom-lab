# FM modulation and demodulation
import numpy as np
import matplotlib.pyplot as plt

Nx = 2000
fs = 2000
fc = 400
fm = 2
df=50
dt = 1/fs
t = dt * np.arange(0,Nx-1)
SNR_DB = 100

xm = np.sin(2*np.pi*fm*t) # Sygnal modulujacy
x = np.exp(1j*(2*np.pi*0*t + 2*np.pi*df/fs*np.sum(xm))) # sygnal zmodulowany (informacyjny) FM
c = np.cos(2*np.pi*fc*t)
s = np.sin(2*np.pi*fc*t)

# UP conversion
xUp = x * (c+1j*s)
xUpReal = np.real(xUp)

# Noise
signal_power = np.mean(np.abs(xUpReal)**2)
noise_power = signal_power / (10**(SNR_DB / 10))
noise = np.sqrt(noise_power) * np.random.randn(len(x))
xUpReal += noise

# Down conversion
xDownCos = 2*xUpReal*c
xDownSin = -2*xUpReal*s
xDown = xDownCos + 1j*xDownSin

# Lowpass filtering
df = fs/Nx
K = int(np.floor(fc/df))

xDownFilt = np.fft.fftshift(xDown)
xDownFilt[K + 1:Nx-K] = 0
xDownFilt = np.fft.ifftshift(xDownFilt)

Error = np.max(abs(x-xDownFilt))
print(Error)
plt.plot(t,xDownFilt)
plt.title("Downfiltered Signal")
plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()