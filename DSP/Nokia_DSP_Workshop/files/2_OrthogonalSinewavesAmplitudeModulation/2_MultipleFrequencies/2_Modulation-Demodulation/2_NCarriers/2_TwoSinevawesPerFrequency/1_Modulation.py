import numpy as np
import matplotlib.pyplot as plt
pi = np.pi

# PARAMETERS
TIME_VECTOR_SIZE = 60

# amplitudes for frequency [1,2,3,4,5,6]
AMPL_VECTOR_SIN = [ 1.23,  4.56,  7.89, -1.23, -4.56, -7.89]
AMPL_VECTOR_COS = [-9.87, -6.54, -3.21,  9.87,  6.54,  3.21]

# CALCULATION
t = np.linspace(0, 2*pi,TIME_VECTOR_SIZE, endpoint=False)

Tx = np.zeros(TIME_VECTOR_SIZE)
for i, (amp_sin,amp_cos) in enumerate(zip(AMPL_VECTOR_SIN,AMPL_VECTOR_COS)):
    f   =  i + 1
    Tx +=  amp_sin*np.sin(f*t) + amp_cos*np.cos(f*t)

# PRESENTATION
plt.plot(Tx)
plt.axhline(y=0,color='black')
plt.grid()
plt.show()

# SAVING
np.save('TxSignal',Tx)

