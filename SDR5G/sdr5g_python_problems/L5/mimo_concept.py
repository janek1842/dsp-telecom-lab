# MIMO concept explained

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RectBivariateSpline
from commpy.channels import awgn

Nsymb = 256
Nfft = 256
QAM4 = np.array([-1-1j, -1+1j, 1-1j, 1+1j])
SNR = 300
time_steps = [2,4,6,8]
freq_steps = [2,4,6,8]
timeerrors = []
freqerrors = []

def interpolate_signal(Hdec,nref,kref):
    xdec = nref  # time-axis
    ydec = kref  # freq-axis

    spline_real = RectBivariateSpline(ydec, xdec, Hdec.real)
    spline_imag = RectBivariateSpline(ydec, xdec, Hdec.imag)

    x = np.arange(Nsymb)
    y = np.arange(Nfft)

    Hest_real = spline_real(y, x)
    Hest_imag = spline_imag(y, x)

    Hest = Hest_real + 1j * Hest_imag
    return Hest

def perform_analysis(nstep,kstep):
    nstep = nstep  # step in time
    kstep = kstep  # step in frequency

    iqTX1 = QAM4[np.random.randint(0, 4, size=(Nfft, Nsymb))]
    iqTX2 = QAM4[np.random.randint(0, 4, size=(Nfft, Nsymb))]
    iqTX1z = iqTX1
    iqTX2z = iqTX2

    k = np.arange(Nfft)
    n = np.arange(Nsymb)

    # Channel - H(t,f)
    X, Y = np.meshgrid(n, k)
    nref = np.arange(0, Nsymb, nstep)  # REF signal position in TIME

    kref1 = np.arange(0, Nfft, kstep)  # REF signal position in FREQ for ant 1
    kref2 = np.arange(int(kstep/2), Nfft, kstep) # REF signal position in FREQ for ant 2

    iqTX1z[np.ix_(kref2,nref)] = 0 # IMPORTANT setting zeros for ant 1 in REF points of ant 2
    iqTX2z[np.ix_(kref1,nref)] = 0 # IMPORTANT setting zeros for ant 2 in REF points of ant 1

    H11 = (X / Nsymb + Y / Nfft) * (1 + 1j)
    H11 = awgn(H11, SNR)

    H12 = (X / Nsymb + Y / Nfft) * (1 - 1j)
    H12 = awgn(H12, SNR)

    H21 = (X / Nsymb + Y / Nfft) * (-1 + 1j)
    H21 = awgn(H21, SNR)

    H22 = (X / Nsymb + Y / Nfft) * (-1 - 1j)
    H22 = awgn(H22, SNR)

    iqRX1 = iqTX1z * H11 + H21 * iqTX2z
    iqRX2 = iqTX1z * H12 + H22 * iqTX2z

    iqTX1ref = iqTX1z[np.ix_(kref1, nref)] # IQ REF transmitted by ant 1
    iqTX2ref = iqTX2z[np.ix_(kref2, nref)] # IQ REF transmitted by ant 2

    iqRX11ref = iqRX1[np.ix_(kref1, nref)]  # RX ant 1 of REF TX ant 1
    iqRX12ref = iqRX2[np.ix_(kref1, nref)]  # RX ant 2 of REF TX ant 1
    iqRX21ref = iqRX1[np.ix_(kref2, nref)]  # RX ant 1 of REF TX ant 2
    iqRX22ref = iqRX2[np.ix_(kref2, nref)]  # RX ant 2 of REF TX ant 2

    # RECEIVER
    H11dec = iqRX11ref / iqTX1ref
    H12dec = iqRX12ref / iqTX1ref
    H21dec = iqRX21ref / iqTX2ref
    H22dec = iqRX22ref / iqTX2ref

    H11est = interpolate_signal(H11dec,nref,kref1)
    H12est = interpolate_signal(H12dec, nref, kref1)
    H21est = interpolate_signal(H21dec, nref, kref2)
    H22est = interpolate_signal(H22dec, nref, kref2)

    H = np.stack([
        np.stack([H11est, H21est], axis=-1),
        np.stack([H12est, H22est], axis=-1)
    ], axis=-2)

    Hinv = np.linalg.inv(H)
    Y = np.stack([iqRX1, iqRX2], axis=-1)  # shape (Nfft, Nsymb, 2)
    iqRX = np.einsum('...ij,...j->...i', Hinv, Y)
    error = np.sum(np.abs(iqTX1z - iqRX[..., 0])) + np.sum(np.abs(iqTX2z - iqRX[..., 1]))

    return error

for time in time_steps:
    error_sum=[]
    for i in range(10):
        error_sum.append(perform_analysis(time,2))
    timeerrors.append(np.mean(error_sum))

for freq in freq_steps:
    error_sum = []
    for i in range(10):
        error_sum.append(perform_analysis(2,freq))
    freqerrors.append(np.mean(error_sum))

# Plotting

plt.figure()

plt.subplot(211)
plt.plot(time_steps,timeerrors,"o--")
plt.xlabel('Reference signal time steps')
plt.ylabel('Sum of errors')
plt.title('Analysis of time REF errors')
plt.grid(True)

plt.subplot(212)
plt.plot(freq_steps,freqerrors,"o--")
plt.xlabel('Reference signal frequency steps')
plt.ylabel('Sum of errors')
plt.title('Analysis of freq REF errors')
plt.grid(True)

plt.tight_layout()
plt.show()