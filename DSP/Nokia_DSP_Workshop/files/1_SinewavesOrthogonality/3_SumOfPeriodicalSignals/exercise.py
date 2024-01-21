import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
pi = np.pi

t = np.linspace(0, 3*(2*pi),100, endpoint=False)

y_sum = np.zeros(len(t)) # summaric vector filled with zeros
for i in range(3): # "3' - nr of componenets
    
    # generating random values of phase shift and amplitudes
    # rand function generates single random nr in range from 0 to 1
    phase = np.random.rand()*(2*pi) 
    ampl  = np.random.rand()
    
    # generating different waveforms 
    # select single waveform by comenting the remaining ones
    
    #y = ampl * signal.sawtooth(t+phase) #triangle
    #y = ampl * np.sin(t+phase) #sinusoid
    y = ampl * np.sign(np.sin(t+phase))     # rectangle

    
    plt.plot(t,y,'-')
    y_sum = y_sum + y

plt.title('Componenets')    
plt.show()

plt.title('Sum')    
plt.plot(t,y_sum,'-')
plt.show()

