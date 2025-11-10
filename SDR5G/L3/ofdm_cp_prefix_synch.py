# Cyclic prefix-based OFDM symbol synchronization and offset correction

import numpy as np
from numpy.fft import fft,ifft
from numpy import fft as numpyfft
import matplotlib.pyplot as plt
from commpy.channels import awgn
from sympy import conjugate

###
# CHANNEL PARAMETERS
scs=30e3
Nfft = 256 # number of all subcarriers
Ncp=18 # Cyclic Prefix length 18 (short) 22 (long)
SNR=300 # SNR
G=np.array([1,0.01,0.01]) # channel-gain (attenuation)
ph=np.array([0,0,0]) # channel phase shift 0, -pi/20 ... (not too large impact)
D=0 # channel delay in samples (very large impact)
dD=0 # channel delay in fraction of samples: 0.01,0.1,0.25
dk=100 # carrier frequency offset

fs = scs*Nfft
Nsymb = Ncp + Nfft

QAM4 = np.array([-1-1j, -1+1j, 1-1j, 1+1j])
numTX = np.random.randint(0, 4, size=Nfft)
scrambl = np.random.randint(0, 4, size=Nfft)
numscTX = np.bitwise_xor(numTX.astype(np.uint8), scrambl.astype(np.uint8)).astype(int)
iqTX = QAM4[numscTX]
added_cfo = 0.1
# END OF CHANNEL PARAMETERS
###

# TWO FUNCTIONS FOR CP SYMBOL SYNCHRONIZATION AND CORRECTION

def find_symbol_start(iq,N_FFT,N_CP_1st,N_CP_OTHER):
    N_block = (N_CP_1st+N_FFT) + 13*(N_CP_OTHER+N_FFT) # 14 OFDM symbol
    N = np.min([len(iq),N_block]) # number of samples

    r = np.zeros(N,dtype=complex)

    for n in range(0,(N-(N_FFT+N_CP_1st-1))):
        r[n] = np.corrcoef(iq[n:n+N_CP_1st-1], iq[n+N_FFT:n+N_FFT+N_CP_1st-1])[0, 1]

    max_corr_index = np.argmax(abs(r))
    max_corr_value = r[max_corr_index]

    plt.stem(abs(r))
    plt.title('CP correlation(n)')
    plt.xlim(0,30)
    plt.grid(True)

    return max_corr_index,r

def estimate_cfo(iq,N_fft,N_cp,jj):
    cfo = 1 / (2*np.pi) * np.mean(np.angle(np.conj(iq[1:N_cp]) * iq[1+N_fft:N_cp+N_fft]))
    cfo = cfo + jj*cfo

    iq = iq * np.exp(-1j*2*np.pi*np.arange(len(iq)) * cfo /N_fft)
    return iq,cfo

# TX
x = ifft(numpyfft.ifftshift(iqTX)) # time domain signal
x = np.concatenate((x[-Ncp:], x)) # ADD CYCLIC PREFIX

Ns = len(x)

# CHANNEL
y = awgn(x,SNR)
y = np.roll(y,D)

h = G * np.exp(1j * ph)       # wektor kanału złożony (kompleksowy)
y = np.convolve(y, h, mode='full')  # splot „same” (tak jak w MATLAB)

y *= np.exp(1j * 2 * np.pi * dk / fs * np.arange(Ns+2))  # CFO

max_corr_index,correlations = find_symbol_start(y,Nfft,Ncp,Ncp)
y = np.roll(y,-1*(max_corr_index-1))
y,cfo = estimate_cfo(y,Nfft,Ncp,added_cfo)

print("estimated cfo is ",cfo*scs, " Hz")

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