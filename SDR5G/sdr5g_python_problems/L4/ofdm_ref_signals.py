# Reference signal interpolation in 5G

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RectBivariateSpline
from commpy.channels import awgn

Nsymb = 256
Nfft = 256
QAM4 = np.array([-1-1j, -1+1j, 1-1j, 1+1j])
SNR = 2
time_steps = [1,2,4,6,8]
freq_steps = [1,2,4,6,8]
timeerrors = []
freqerrors = []

def perform_analysis(nstep,kstep):
    nstep = nstep  # step in time
    kstep = kstep  # step in frequency

    numTXref = np.random.randint(0, 4, size=(Nfft, Nsymb))
    iqTX = QAM4[numTXref]

    k = np.arange(Nfft)
    n = np.arange(Nsymb)

    # Channel - H(t,f)
    X, Y = np.meshgrid(n, k)
    H = (X / Nsymb + Y / Nfft) * (1 + 1j)
    H = awgn(H, SNR)
    iqRX = iqTX * H  # apply channel

    nref = np.arange(0, Nsymb, nstep)  # REF signal position in TIME
    kref = np.arange(0, Nfft, kstep)  # REF signal position in FREQ

    iqTXref = iqTX[np.ix_(kref, nref)]  # IQ REF TRANSMITTED
    iqRXref = iqRX[np.ix_(kref, nref)]  # IQ REF RECEIVED

    # Channel estimation

    Hdec = iqRXref / iqTXref

    xdec = nref  # time-axis
    ydec = kref  # freq-axis

    spline_real = RectBivariateSpline(ydec, xdec, Hdec.real)
    spline_imag = RectBivariateSpline(ydec, xdec, Hdec.imag)

    x = np.arange(Nsymb)
    y = np.arange(Nfft)

    Hest_real = spline_real(y, x)
    Hest_imag = spline_imag(y, x)

    Hest = Hest_real + 1j * Hest_imag

    # Channel equalization
    iqRXdat = iqRX / Hest

    # Error calculation
    error = np.sum(np.abs(iqRXdat - iqTX))

    return error


for time in time_steps:
    error_sum=[]
    for i in range(10):
        error_sum.append(perform_analysis(time,1))
    timeerrors.append(np.mean(error_sum))

for freq in freq_steps:
    error_sum = []
    for i in range(10):
        error_sum.append(perform_analysis(1,freq))
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