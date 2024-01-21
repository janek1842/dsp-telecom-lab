import numpy as np
import matplotlib.pyplot as plt
pi = np.pi

# PARAMETERS
TIME_VECTOR_SIZE = 60
AMPL_VECTOR = (1.2, -3.4, 4.5, -1.2)

# CALCULATION
t = np.linspace(0, 2*pi,TIME_VECTOR_SIZE, endpoint=False)
amplitudes_l = []
Carrier = np.sin(t)

for amp in AMPL_VECTOR:
      
    # modulation
    Tx = np.array([])  
    Tx = np.append(Tx, amp * Carrier)

    # channel
    Rx=Tx # ideal one    
    
    # demodulation
    dot  = np.dot(Carrier,Rx)
    ampl = 2*(dot/PERIOD_VECTOR_SIZE)
    amplitudes_l.append(ampl)

# PRESENTATION  

plt.plot(Rx)
plt.axhline(y=0,color='black')
plt.grid(axis='y')
plt.show()

#  
print(f'received amplitudes: {amplitudes_l}')



