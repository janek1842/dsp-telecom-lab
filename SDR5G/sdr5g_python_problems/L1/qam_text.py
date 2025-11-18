from random import randint
from numpy.fft import fft,ifft
from numpy import fft as numpyfft
import numpy as np
from commpy.channels import awgn
import matplotlib.pyplot as plt

Nfft= 512
SNR = -15
string_to_transmit="text to be transmitted"
lengths=[]
iqTAB = np.array([-1-1j, -1+1j, 1-1j, 1+1j])
rx_string=""

for s in string_to_transmit:
    binary = ""
    binary+=str((bin(ord(s))[2:]))
    lengths.append(len(bin(ord(s))[2:]))


    chunks = [binary[max(i - 2, 0):i] for i in range(len(binary), 0, -2)]
    chunks.reverse()

    numTx=[]
    Ns = len(chunks)

    for chunk in chunks:
        numb = 0

        if len(chunk)==1:
            if chunk[0] == "1":
                numb += 1
        else:
            if chunk[0]=="1":
                numb+=2
            if chunk[1]=="1":
                numb+=1
        numTx.append(numb)

    iqTX = np.zeros(len(numTx),dtype="complex")

    for i in range(len(numTx)):
        iqTX[i] = iqTAB[numTx[i]]

    X=np.zeros(Nfft,dtype="complex")
    X[:Ns] = iqTX

    x = ifft(numpyfft.ifftshift(X))
    y = awgn(x,SNR)

    Y = numpyfft.fftshift(fft(y))
    iqRx = Y[:Ns]

    numRx=[]
    for k in iqRx:
        if np.real(k) < 0 and np.imag(k) < 0:
            numRx.append(0)
        elif np.real(k) < 0 and np.imag(k) > 0:
            numRx.append(1)
        elif np.real(k) > 0 and np.imag(k) < 0:
            numRx.append(2)
        elif np.real(k) > 0 and np.imag(k) > 0:
            numRx.append(3)

    final_bin=""
    for numb in numRx:
        if numb==3:
            final_bin+="11"
        elif numb==2:
            final_bin+="10"
        elif numb==1:
            final_bin+="01"
        elif numb==0:
            final_bin+="00"

    decimal = int(final_bin, 2)
    rx_string += (chr(decimal))

print("Received text: ", rx_string)