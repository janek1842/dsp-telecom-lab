# Program presenting DSL transmitter, channel and receiver scheme

import scipy .io
import numpy as np
from scipy.signal import lfilter
import matplotlib.pyplot as plt

fs = 2.208e6
codingGain = 4.2
margin = 6

N = 512
Ld = 32
Le = 16
Nd = N + Ld
Ns = 200

inputPower = 23
inputImp = 100
lineNoise = [-140,-130,-120,-110,-100,-90,-80]
finalSNR=[]

# loading channel parameters from the file

# c - frequency response
# w - filter impulse response
# Dx - delay from the impulse response

for n in lineNoise:

    c = scipy.io.loadmat("c_w_Dx.mat")["c"].ravel()
    w = scipy.io.loadmat("c_w_Dx.mat")["w"].ravel()
    Dx = int(scipy.io.loadmat("c_w_Dx.mat")["Dx"].ravel()[0])


    if len(c) < N:
        c = np.append(c, np.zeros(N-len(c)))
    sir = np.convolve(w,c)

    if len(sir) < N:
        sir = np.append(sir, np.zeros(N-len(sir)))
    SIR = np.fft.fft(sir[:N])
    k = np.arange(N)

    # FEQ
    FEQ = SIR * (1/(2*np.sqrt(2))) * np.exp(1j*2*np.pi/N * k * Dx)
    rb = np.zeros(2*Nd)
    tf_sig = np.zeros(N)
    tf_err = np.zeros(N)
    U = np.zeros(N)
    U0 = np.zeros(N)
    c_res = np.zeros(len(c)-1)
    w_res = np.zeros(len(w)-1)

    noiseAWGN = np.random.randn(Ns * Nd) * np.sqrt(inputImp * 0.001 * fs / 2 * 10 ** (n/10) )
    signalPower = inputImp * 0.001 * 10 ** (inputPower/10)
    scalingFactor = np.sqrt(10** (codingGain/10)) * np.sqrt(signalPower)

    for iter in range(Ns):
        # TX

        U0 = U # symulacja po ilości ramek
        Ur = np.sqrt(3) * (2*np.random.rand(N//2 - 1) - 1 )
        Ui = np.sqrt(3) * (2 * np.random.rand(N // 2 - 1) - 1)

        U = Ur + 1j * Ui # modulacja QAM
        U = np.concatenate(([0], U, [0], np.conj(U[::-1])))
        x = np.fft.ifft(U) # modulacja OFDM

        x = np.real(x) * np.sqrt(N) / np.sqrt(2) # normalizacja
        x = np.concatenate((x[N - Ld:], x)) # dodanie cyklicznego prefiksu
        s = x * scalingFactor # wzmocnienie sygnału

        # CHANNEL

        y, c_res = lfilter(c, [1], s, zi=c_res) # przejscie przez kanal
        y = y + noiseAWGN[(iter) * Nd : (iter+1) * Nd] # dodanie szumu
        y = y / scalingFactor # normalizacja sygnalu

        # RX
        ye, w_res = lfilter(w, [1], y, zi=w_res)  # korektor TEQ
        rb[:Nd] = rb[Nd:]
        rb[Nd:] = ye

        y = rb[Dx+Ld:N+Dx+Ld] # usuniecie prefiksu

        Y = np.fft.fft(y)
        Y = Y / (2*np.sqrt(N)) # Normowanie sygnalu
        U_r = Y / FEQ # FEQ

        if iter > 2:
            e = U0 - U_r
            tf_sig = tf_sig + U0 * np.conj(U0)
            ce = e * np.conj(e)
            tf_err = tf_err + ce

    idx = np.where(tf_err == 0)
    tf_err[idx] = np.finfo(float).eps

    snr = tf_sig[:N//2] / tf_err[:N//2]
    finalSNR.append(sum(abs(snr)))

plt.plot(lineNoise,finalSNR)
plt.ylabel("SNR")
plt.xlabel("Noise [db]")
plt.show()
