import numpy as np
import matplotlib.pyplot as plt
pi = np.pi

# PARAMETERS
TIME_VECTOR_SIZE = 60

AMPL_F1 = 4.3 
AMPL_F2 = 2.1 

# CALCULATION
t = np.linspace(0, 2*pi,TIME_VECTOR_SIZE, endpoint=False)

carrier_f1 = 1
carrier_f2 = 2

tx_f1 = AMPL_F1 * np.sin(carrier_f1*t)
tx_f2 = AMPL_F2 * np.sin(carrier_f2*t)

Tx = tx_f1 + tx_f2

# PRESENTATION
plt.plot(Tx, color='black')
plt.axhline(y=0,color='black')
plt.grid()
plt.show()

# SAVING
np.save('TxSignal',Tx)
