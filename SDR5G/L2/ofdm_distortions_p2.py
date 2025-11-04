# Investigations on OFDM distortions induced by the channel or TX/RX
from pickletools import uint8

import numpy as np
from numpy.fft import fft,ifft
from numpy import fft as numpyfft
import matplotlib.pyplot as plt
from commpy.channels import awgn

# CHANNEL PARAMETERS
scs=30e3
Nfft = 256 # number of all subcarriers
Ncp=22 # Cyclic Prefix length 18 (short) 22 (long)
SNR=300 # SNR
G=np.array([1,0.1,0.3]) # channel-gain (attenuation)
ph=np.array([0,0,0]) # channel phase shift 0, -pi/20 ... (not too large impact)
D=0 # channel delay in samples (very large impact)
dD=0 # channel delay in fraction of samples: 0.01,0.1,0.25
dk=0 # carrier frequency offset
# END OF CHANNEL PARAMETERS

fs = scs*Nfft
Nsymb = Ncp + Nfft

QAM4 = np.array([-1-1j, -1+1j, 1-1j, 1+1j])
numTX = np.random.randint(0, 4, size=Nfft)
scrambl = np.random.randint(0, 4, size=Nfft)
numscTX = np.bitwise_xor(numTX.astype(np.uint8), scrambl.astype(np.uint8)).astype(int)
iqTX = QAM4[numscTX]

# TX
x = ifft(numpyfft.ifftshift(iqTX)) # time domain signal
x = np.concatenate((x[-Ncp:], x)) # ADD CYCLIC PREFIX

Ns = len(x)

# CHANNEL
y = awgn(x,SNR)
y = np.roll(y,D)

h = G * np.exp(1j * ph)       # wektor kanału złożony (kompleksowy)
y = np.convolve(y, h, mode='full')  # splot „same” (tak jak w MATLAB)

y *= np.exp(1j * 2 * np.pi * dk *scs / fs * np.arange(Ns+2))  # CFO

# RX
y = y[Ncp:Ncp+Nfft]
Xback = numpyfft.fftshift(fft(y))

# VISUALIZATION
plt.figure(figsize=(12,8))

plt.subplot(211)
plt.plot(np.real(iqTX), np.imag(iqTX), 'o', label="signal tx")
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