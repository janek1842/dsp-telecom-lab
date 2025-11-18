# Investigating fft variants and comparing each other from the complexity perspective
import numpy as np
from numpy.fft import fft,ifft
import time
import matplotlib.pyplot as plt

# Standard implementation - complexity: N^2
def my_dft(x):
    X = np.zeros(len(x),dtype=complex)
    for n in range(len(x)):
        for k in range(len(x)):
            X[k] += x[n] * np.exp(-1j*(2*np.pi/len(x))*k*n)
    return X

# Decimation in time
def fft_dit(x):
    N = len(x)
    v = int(np.ceil(np.log2(N)))  # liczba bitów (stages)
    num_zeros = 2**(v)-N

    x = np.concatenate((x, np.zeros(num_zeros)))
    N = len(x)

    x0 = np.zeros(N,dtype=complex)
    b = 2 ** np.arange(v - 1, -1, -1)

    for k in range(N-1):
        ind=k
        ko = np.zeros(v)

        for k1 in range(0,v-1):
            if ind -b[k1+1] >=0:
                ko[k1+1]=1
                ind = ind - b[k1+1]
        ind_o = int(np.sum(np.flip(ko)*b))
        x0[ind_o+1] = x[k+1]

    X = np.zeros((2, N), dtype=complex)  # memory for data and results (complex numbers)
    X[0, :] = x0  # data
    WN = np.exp(-1j * 2 * np.pi / N)
    N = len(X)
    X_temp = np.zeros_like(X, dtype=complex)

    for k in range(v):  # pętla po etapach
        M = 2 ** k  # liczba motylków w bloku
        for k1 in range(int(N / (2 * M))):  # pętla po blokach
            for k2 in range(M):  # pętla wewnątrz bloku
                # ustalenie indeksów
                p = int(k1 * N / (2 ** (v - k - 1)) + k2)
                q = p + M
                r = int((2 ** (v - k - 1)) * k2)
                # obliczenia motylkowe
                X_temp[p] = X[p] + (WN ** r) * X[q]
                X_temp[q] = X[p] - (WN ** r) * X[q]
        X[:] = X_temp  # podstawienie wyników po etapie

    Xw = X
    return Xw


### Signal common parameters

fpr = 100 # sampling frequency
f = 3 # signal frequency
dt = 1/fpr # time steps
tmax=2 # signal time

A = 2 # amplitude
N= []
N_size=11

### End of common parameters

for i in range(N_size):
    N.append(np.pow(2, i))

mydft_time=[]
for i in range(N_size):
    start = time.time()
    t = np.linspace(0,tmax,N[i]) # time domain
    x = A*np.sin(2*np.pi*f*t + np.pi/2) # signal
    X = my_dft(x) # signal in frequency domain
    end = time.time()
    mydft_time.append(end-start)

# 1. numpy fft
numpyfft_time = []
for i in range(N_size):
    start = time.time()
    t = np.linspace(0,tmax,N[i]) # time domain
    x = A*np.sin(2*np.pi*f*t + np.pi/2) # signal
    X = fft(x) # signal in frequency domain
    end = time.time()
    numpyfft_time.append(end-start)

# 2. decimation in time
fft_dit_time = []
for i in range(N_size):
    start = time.time()
    t = np.linspace(0,tmax,N[i]) # time domain
    x = A*np.sin(2*np.pi*f*t + np.pi/2) # signal
    X = fft_dit(x) # signal in frequency domain
    end = time.time()
    fft_dit_time.append(end-start)

# Results plotting
plt.title('Signal x in time domain')
plt.xlabel('Signal size 10^N')
plt.ylabel('Execution time [s]')
plt.plot(N,mydft_time,'o--',label="mydft")
plt.plot(N,numpyfft_time,'o--',label="numpy fft")
plt.plot(N,fft_dit_time,'o--',label="dit fft")
plt.legend()
plt.show()