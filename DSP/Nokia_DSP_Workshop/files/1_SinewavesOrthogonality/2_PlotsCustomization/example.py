import numpy as np
import matplotlib.pyplot as plt
from scipy import signal #required for triangle signal generation

# DATA CREATION

# definition of pi constant by using numpy library
pi = np.pi 

# time vector.
# from zero to 2pi in 30 steps
t = np.linspace(0, 3*3*pi,60, endpoint=False) #

# “simple” sinusoid
sin_a = np.sin(t)

# sinusoid with amplitude equal to 2 and time shift qual to pi/4
sin_b = 1.41*np.sin(t+pi)

# triangular waveforms
#"0.5" denotes proportion between positive and negative slope
trian_a = signal.sawtooth(t,0.5)
trian_b = 3*signal.sawtooth(t+pi/40, 0.5)
trian_c = trian_a+trian_b

suma=trian_b+sin_b

# adding waveforms to figure
plt.plot(t,suma, '--', label='sum', color='red')
plt.plot(t,trian_b,'-p', label='triangle', color='green')
plt.plot(t,sin_b,'.', label='sinusoid', color='blue')

# customizing figure
plt.title('trianle + sinus')
plt.xlabel('tempus[s]')
plt.ylabel('amplitudo[a.u.]')
plt.xlim(0,10)
plt.ylim(-4,6)
plt.axhline(y=0,color='red')
plt.grid()
plt.legend()

# drawing figure
plt.show()

