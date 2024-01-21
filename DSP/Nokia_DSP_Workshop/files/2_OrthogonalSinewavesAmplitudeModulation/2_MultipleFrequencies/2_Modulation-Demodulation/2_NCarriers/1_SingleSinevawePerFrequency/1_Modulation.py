import numpy as np
import matplotlib.pyplot as plt
pi = np.pi

# PARAMETERS
TIME_VECTOR_SIZE = 60
# amplitudes for frequencies [1,2,3,4,5,6]
AMPL_VECTOR = [1.23,4.56, 7.89,-1.23,-4.56, -7.89]

# CALCULATION
t = np.linspace(0, 2*pi,TIME_VECTOR_SIZE, endpoint=False)

Tx = np.zeros(len(t))
for i, amp in enumerate(AMPL_VECTOR):
    f = i+1
    Tx += amp*np.sin(f*t)

# PRESENTATION
plt.plot(Tx)
plt.axhline(y=0,color='black')
plt.grid()
plt.show()

# SAVING
np.save('TxSignal',Tx)

