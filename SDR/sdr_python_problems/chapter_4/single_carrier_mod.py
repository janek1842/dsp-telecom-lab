# Single carrier modulation investigation on the idea of pulse-shaping filters

import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft,ifft,fftshift
from commpy.filters import rcosfilter

# I signal
I = np.array([-1,1,-1,1,1,-1,-1,-1,1,-1])

# Inserting zeros
I0 = []

for n in range(len(I)):
    I0.append(I[n])
    for i in range(4):
        I0.append(0)
I0 = np.array(I0)

# Applying filter (square vs rcs35 vs rcs70)
N = 30
h_sq = np.ones(N)

beta = 0.25
betav2 = 1
sps = 5

t,h_rc = rcosfilter(N, beta, 1, sps)
t,h_rcv2 = rcosfilter(N, betav2, 1, sps)

y_square = np.convolve(I0, h_sq, mode='same')
y_rcs = np.convolve(I0, h_rc, mode='same')
y_rcsv2 = np.convolve(I0, h_rcv2, mode='same')

Y_SQ = np.fft.fftshift(fft(y_square)/len(y_square))
Y_rcs = np.fft.fftshift(fft(y_rcs)/len(y_rcs))
Y_rcsv2 = np.fft.fftshift(fft(y_rcsv2)/len(y_rcsv2))

plt.figure()
plt.subplot(311)
plt.stem(y_square)
plt.title("Square filter")
plt.subplot(312)
plt.stem(y_rcs)
plt.title("RCS rolloff 0.25")
plt.subplot(313)
plt.stem(y_rcsv2)
plt.title("RCS rolloff 1")
plt.tight_layout()
plt.show()

# Frequecy analysis - RCS more efficient and prevents from ISI
# Warning! Further analysis would show that RCS is harder to detect

N = len(y_square)
fs = sps
f = fftshift(np.fft.fftfreq(len(y_square), d=1/fs))
f_rcs = fftshift(np.fft.fftfreq(len(y_rcs), d=1/fs))
f_rcsv2 = fftshift(np.fft.fftfreq(len(y_rcsv2), d=1/fs))

plt.figure()
plt.stem(f,np.abs(Y_SQ), linefmt='r-', markerfmt='ro', basefmt='k-',label='Square filter')
plt.stem(f_rcs,np.abs(Y_rcs), linefmt='g-', markerfmt='go', basefmt='k-',label='Root square cosine 0.25')
plt.stem(f_rcsv2,np.abs(Y_rcsv2), linefmt='b-', markerfmt='bo', basefmt='k-',label='Root square cosine 1.0')

plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()
plt.show()
