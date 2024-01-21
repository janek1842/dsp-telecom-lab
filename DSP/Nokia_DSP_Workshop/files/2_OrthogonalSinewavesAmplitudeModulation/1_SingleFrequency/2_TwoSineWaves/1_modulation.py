import numpy as np
import matplotlib.pyplot as plt
pi = np.pi

# PARAMETERS
TIME_VECTOR_SIZE = 60

AMPL_VECTOR_SIN = ( 0.5,  1.0,  -1.5)
AMPL_VECTOR_COS = (-1.5,  1.0,   0.5)

# CALCULATION
t = np.linspace(0, 2*pi,TIME_VECTOR_SIZE, endpoint=False)

carrier_sin = np.sin(t)
carrier_cos = np.cos(t)

Tx = np.array([]) #empty time vector
for ampl_sin, ampl_cos in zip(AMPL_VECTOR_SIN, AMPL_VECTOR_COS):    
    TxSinglePeriod = ampl_sin*carrier_sin + ampl_cos*carrier_cos
    Tx = np.append(Tx,TxSinglePeriod)

# PRESENTATION
plt.plot(Tx)
plt.axhline(y=0,color='black')
plt.xticks((0,1*60,2*60,3*60))
plt.grid()

plt.show()

# SAVING
np.save('TxSignal',Tx)

