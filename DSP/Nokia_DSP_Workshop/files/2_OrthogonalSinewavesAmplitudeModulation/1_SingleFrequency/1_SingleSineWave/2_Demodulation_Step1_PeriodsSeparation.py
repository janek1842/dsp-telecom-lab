import numpy as np
import matplotlib.pyplot as plt

# parameters
PERIOD_VECTOR_SIZE = 60
PERIOD_NUMBER = 5

# loading Rx vector from file and..
Rx = np.load('TxSignal.npy')

# .. ploting it
plt.plot(Rx)
plt.grid()
plt.show()

# spliting vector into time slots coresponding to single periods
RxPeriods = np.reshape(Rx,(PERIOD_NUMBER,PERIOD_VECTOR_SIZE))

# plotting periods one by one
for i, RxPeriod in enumerate(RxPeriods):
    plt.figure()
    plt.plot(RxPeriod)
    plt.title(f'Period {i}')
    plt.grid()
    plt.show()
