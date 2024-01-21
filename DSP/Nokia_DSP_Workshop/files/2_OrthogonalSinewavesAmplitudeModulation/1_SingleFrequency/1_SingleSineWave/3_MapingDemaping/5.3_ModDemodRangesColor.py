# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 22:48:01 2023

@author: janfi
"""

import numpy as np
import matplotlib.pyplot as plt
pi = np.pi

# PARAMETERS
TIME_VECTOR_SIZE = 60
AMPL_VECTOR=np.linspace(0,4,8)

# CALCULATION
t = np.linspace(0, 2*pi,TIME_VECTOR_SIZE, endpoint=False)
amplitudes_l = []
Carrier = np.sin(t)

NOISE_DEVIATION=0.6
TANSMISION_NR=100

for i in range(TANSMISION_NR):

    amp = AMPL_VECTOR[i%8]     

    # modulation
    Tx = np.array([])  
    Tx = np.append(Tx, amp * Carrier)

    # channel
    Rx= Tx + np.random.normal(0,NOISE_DEVIATION,len(Tx))    
    
    # demodulation
    dot  = np.dot(Carrier,Rx)
    ampl = 2*(dot/TIME_VECTOR_SIZE)   
    amplitudes_l.append(ampl)

    
# PRESENTATION  

plt.plot(amplitudes_l[0::8],'p',color='red')
plt.plot(amplitudes_l[1::8],'p',color='orange')
plt.plot(amplitudes_l[2::8],'p',color='green')
plt.plot(amplitudes_l[3::8],'p',color='blue')
plt.plot(amplitudes_l[4::8],'p',color='black')
plt.plot(amplitudes_l[5::8],'p',color='yellow')
plt.plot(amplitudes_l[6::8],'p',color='pink')
plt.plot(amplitudes_l[7::8],'p',color='purple')

plt.axhline(y=0,color='black')
plt.grid(axis='y')
plt.show()

print(f'received amplitudes: {amplitudes_l}')

