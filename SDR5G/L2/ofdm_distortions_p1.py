# Investigations on OFDM distortions induced by the channel or TX/RX
import numpy as np
from numpy.fft import fft,ifft
from numpy import fft as numpyfft
import matplotlib.pyplot as plt
from commpy.channels import awgn

# CHANNEL PARAMETERS
Nfft = 64 # number of all subcarriers
Ncar=48 # number of used sub-carriers
SNR=20 # SNR
G=1 # channel-gain (attenuation)
ph=0 # channel phase shift 0, -pi/20 ... (not too large impact)
D=0 # channel delay in samples (very large impact)
dk=0.1 # carrier frequency offset (CFO) 0,0.1,0.5,1,1.1 (quite large impact)
# END OF CHANNEL PARAMETERS

iqTAB = [-1-1j, -1+1j, 1-1j, 1+1j]
X=np.zeros(Nfft,dtype="complex")
X = np.random.choice(iqTAB, size=Nfft)

# TX
x = ifft(numpyfft.ifftshift(X)) # time domain signal

# CHANNEL
y = awgn(x,SNR)
y = G*np.exp(1j*ph)*np.roll(y,D)*np.exp(1j*2*np.pi*dk/Nfft * np.arange(0,Nfft))

# RX
Xback = numpyfft.fftshift(fft(y))
error_X = max(abs(X-Xback))

plt.figure(figsize=(12,8))

plt.subplot(211)
plt.plot(np.real(X), np.imag(X), 'o', label="signal tx")
plt.legend()
plt.xlabel('In-phase (I)')
plt.ylabel('Quadrature (Q)')
plt.title('Constellation Diagram')
plt.grid(True)

plt.subplot(212)
plt.plot(np.real(Xback), np.imag(Xback), 'o', label="signal rx")
plt.xlabel('In-phase (I)')
plt.ylabel('Quadrature (Q)')
plt.legend()
plt.grid(True)
plt.show()