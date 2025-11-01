import numpy as np
from numpy.fft import fft,ifft

from numpy import fft as numpyfft
import matplotlib.pyplot as plt

Nfft = 512 # number of subcarriers
scs = 30e+3 # subcarrier spacing
fx = [8*scs,16*scs] # orthogonal subcarriers
# 240 i 480 kHz

Ax = [1,2] # Signal amplitudes
fs = scs * Nfft # signal bandwidth
dt = 1/fs # sampling period

Nx = Nfft
t = dt * np.arange(Nx)
x1 = np.zeros(Nx)
x2=x1

for k in range(len(fx)):
    x1 = x1 + Ax[k] * np.cos(2*np.pi*fx[k]*t)
    x2 = x2 + Ax[k] * np.exp(1j*2*np.pi*fx[k]*t)

# Signal analysis and spectrum shift
X1 = fft(x1)/Nx
X2 = fft(x2)/Nx

X1DC = numpyfft.fftshift(X1)
X2DC = numpyfft.fftshift(X2)

# signal reconstruction
x1back = ifft(numpyfft.ifftshift(X1DC))*Nx
x2back = ifft(numpyfft.ifftshift(X2DC))*Nx

error_x1 = max(abs(x1-x1back))
error_x2 = max(abs(x2-x2back))

print(error_x1,error_x2)

f0=fs/Nx
k=np.arange(Nx)
kDC = np.arange(-Nx/2, Nx/2)

fkDC = kDC * f0
fk=k*f0

plt.figure(figsize=(12,8))

plt.subplot(211)
plt.stem(fk,np.abs(X1), label='|X1(f)|')
plt.title('Widmo X1')
plt.ylabel('Amplituda')
plt.legend()
plt.grid(True)

plt.subplot(212)
plt.stem(fk,np.abs(X2), label='|X2(f)|')
plt.title('Widmo X2')
plt.xlabel('f [Hz]')
plt.ylabel('Amplituda')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(12,8))

plt.subplot(211)
plt.stem(fkDC,np.abs(X1DC), label='|X1DC(f)|')
plt.title('Schifted widmo X1')
plt.ylabel('Amplituda')
plt.legend()
plt.xlim(-2e6,2e6)
plt.grid(True)

plt.subplot(212)
plt.stem(fkDC,np.abs(X2DC), label='|X2DC(f)|')
plt.title('Schifted widmo X2')
plt.xlabel('f [Hz]')
plt.ylabel('Amplituda')
plt.legend()
plt.xlim(-2e6,2e6)
plt.grid(True)
plt.show()
