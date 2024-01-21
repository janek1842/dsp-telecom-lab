import numpy as np
import matplotlib.pyplot as plt
from mylib import my_stem_plot

SAMPLE_NR = 10
FREQ_1 = 1
FREQ_2 = 3
A_1 = 1/5
A_2 = 1

t = np.linspace(0, 2*np.pi, SAMPLE_NR, endpoint=False)

samples =  A_1*np.sin(t*FREQ_1) + A_2*np.cos(t*FREQ_2)

my_stem_plot(samples,f'samples, sin_f={FREQ_1}, a_sin={A_1}, cos_f={FREQ_2}, a_cos={A_2}',y_range=(-6,7))

fft = np.fft.fft(samples)
my_stem_plot(np.real(fft),'DFT real',y_range=(-6,7))
my_stem_plot(np.imag(fft) ,'DFT imag',y_range=(-6,7))
