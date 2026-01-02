# Scripts for Primary Synchronization Signal learning purposes in 5G

import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft,ifft,fftshift,ifftshift
from numpy import fft as numpyfft

N = 256

def generatePSS(NID2):
    x_table = np.zeros(128)
    x_table[:7] = [0,1,1,0,1,1,1]

    for n in range (8,128):
        x_table[n] = (x_table[n-3] - x_table[n-7]) % 2

    n = np.arange(0,127)
    seq = 1 - 2*x_table[((n+43*NID2)%127) + 1]
    return seq

plt.figure()
plt.subplot(311)
plt.stem(generatePSS(0))
plt.title("NID2 = 0")
plt.subplot(312)
plt.stem(generatePSS(1))
plt.title("NID2 = 1")
plt.subplot(313)
plt.stem(generatePSS(2))
plt.title("NID2 = 2")
plt.tight_layout()
plt.show()

x0 = ifftshift(np.fft.ifft((generatePSS(0)),256))
x1 = ifftshift(np.fft.ifft((generatePSS(1)),256))
x2 = ifftshift(np.fft.ifft((generatePSS(2)),256))

plt.figure()
plt.subplot(311)
plt.stem(np.abs(np.correlate(x0, x0,'full')))
plt.title("NID2 = 0")
plt.subplot(312)
plt.stem(np.abs(np.correlate(x1, x1,'full')))
plt.title("NID2 = 1")
plt.subplot(313)
plt.stem(np.abs(np.correlate(x2, x2,'full')))
plt.title("NID2 = 2")
plt.tight_layout()
plt.show()

CFO = 15.67

x0 = x0 * np.exp(-1j*2*np.pi/127 * CFO * np.arange(0,N))
x1 = x1 * np.exp(-1j*2*np.pi/127 * CFO * np.arange(0,N))
x2 = x2 * np.exp(-1j*2*np.pi/127 * CFO * np.arange(0,N))

plt.figure()
plt.subplot(311)
plt.stem(np.abs(np.correlate(x0, x0,'full')))
plt.title("NID2 = 0")
plt.subplot(312)
plt.stem(np.abs(np.correlate(x1, x1,'full')))
plt.title("NID2 = 1")
plt.subplot(313)
plt.stem(np.abs(np.correlate(x2, x2,'full')))
plt.title("NID2 = 2")
plt.tight_layout()
plt.show()

