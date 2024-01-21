import numpy as np
import matplotlib.pyplot as plt
from mylib import my_stem_plot, myDFT

SAMPLE_NR = 10
SIN_FREQ = 3
COS_FREQ = 3
A_1 = 0
A_2 = 0.8

t = np.linspace(0, 2*np.pi, SAMPLE_NR, endpoint=False)

samples = A_1*np.sin(t*SIN_FREQ) + A_2*np.cos(t*COS_FREQ)
my_stem_plot(samples,f'samples, f_sig={SIN_FREQ}')
    
real,image = myDFT(samples)

my_stem_plot(real,'my DFT real',y_range=(-6,7))
my_stem_plot(image,'my DFT imag',y_range=(-6,7))


