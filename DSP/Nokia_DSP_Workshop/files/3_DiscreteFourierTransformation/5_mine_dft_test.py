import numpy as np
import matplotlib.pyplot as plt

# plots stem plot fro given "y" vector
def my_stem_plot(y,title,y_range=(-6,7)):
    x = np.arange(len(y))    
    plt.stem(x,y,'-p')
    
    plt.ylim((-5,5))
    plt.xticks(x)
    plt.yticks(np.arange(*y_range))
    plt.grid()
    plt.title(title)
    fig = plt.gcf()
    fig.set_size_inches(4, 3.6)
    plt.show()

#----------------------------

SAMPLE_NR = 10
SIN_FREQ = 3 

t = np.linspace(0, 2*np.pi, SAMPLE_NR, endpoint=False)

samples=np.cos(t*1)*2/5 + np.sin(t*4) * 4/5
my_stem_plot(samples,f'samples')


real,imag=myDFT(samples)
my_stem_plot(real,'my DFT real')
my_stem_plot(imag,'my DFT imag')

fft = np.fft.fft(samples)
my_stem_plot(fft.real,'FFT real',y_range=(-6,7))
my_stem_plot(fft.imag,'FFT imag',y_range=(-6,7))


