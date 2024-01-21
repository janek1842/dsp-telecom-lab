import numpy as np
import matplotlib.pyplot as plt
pi = np.pi

# parameters
PERIOD_VECTOR_SIZE = 60

# loading Rx vector from file and..
Rx = np.load('TxSignal.npy')

# .. ploting it
plt.plot(Rx)
plt.axhline(y=0,color='black')
plt.grid()
plt.show()

# CALLCULATION
t = np.linspace(0, 2*pi,PERIOD_VECTOR_SIZE, endpoint=False)

# references
ref_f1_sin = np.sin(t)
ref_f1_cos = np.cos(t) 

ref_f2_sin = np.sin(2*t)
ref_f2_cos = np.cos(2*t)

# dot products
dot_f1_sin = np.dot(Rx,ref_f1_sin)
dot_f1_cos = np.dot(Rx,ref_f1_cos) 

dot_f2_sin = np.dot(Rx,ref_f2_sin) 
dot_f2_cos = np.dot(Rx,ref_f2_cos) 

# amplitudes
amp_f1_sin = (dot_f1_sin/TIME_VECTOR_SIZE)*2  
amp_f1_cos = (dot_f1_cos/TIME_VECTOR_SIZE)*2 

amp_f2_sin = (dot_f2_sin/TIME_VECTOR_SIZE)*2 
amp_f2_cos = (dot_f2_cos/TIME_VECTOR_SIZE)*2 

# PRESENTATION
print(f'amp_f1_sin={amp_f1_sin:0.1f}')
print(f'amp_f1_cos={amp_f1_cos:0.1f}')
print(f'amp_f2_sin={amp_f2_sin:0.1f}')
print(f'amp_f2_cos={amp_f2_cos:0.1f}')


