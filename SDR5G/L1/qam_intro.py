from random import randint
from numpy.fft import fft,ifft
from numpy import fft as numpyfft
import numpy as np
from commpy.channels import awgn
import matplotlib.pyplot as plt

Nfft= 512
iqTAB = np.array([-1-1j, -1+1j, 1-1j, 1+1j])

# TX
X = np.random.choice(iqTAB, size=Nfft)
x = ifft(numpyfft.ifftshift(X))
print(x)

# CHANNEL
SNR=24
y = awgn(x,SNR)

# RX
Xback = numpyfft.fftshift(fft(y))
error_X = max(abs(X-Xback))

plt.figure(figsize=(12,8))

plt.subplot(211)
plt.plot(np.real(X), np.imag(X), 'o')
plt.legend()
plt.xlabel('In-phase (I)')
plt.ylabel('Quadrature (Q)')
plt.title('Constellation Diagram')
plt.grid(True)

plt.subplot(212)
plt.plot(np.real(Xback), np.imag(Xback), 'o')
plt.xlabel('In-phase (I)')
plt.ylabel('Quadrature (Q)')
plt.legend()
plt.grid(True)
plt.show()