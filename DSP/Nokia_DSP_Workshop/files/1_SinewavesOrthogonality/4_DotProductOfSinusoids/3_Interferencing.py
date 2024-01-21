import numpy as np
import matplotlib.pyplot as plt
pi = np.pi

# PARAMETERS
TIME_VECTOR_SIZE = 30
A_tx = 1
A_int = 30
A_int_phi =  2*np.pi

# CALCULATION
t = np.linspace(0, 2*np.pi,TIME_VECTOR_SIZE, endpoint=False)

# modulation
Tx   = A_tx  * np.sin(t) 

#channel
Interfer = A_int * np.sin(t+A_int_phi)
Rx       =  Tx * Interfer

# demodulation
Rx_mul_Sin = Rx*1*np.cos(t)
Rx_dot_Sin  = np.dot(np.sin(t),Rx_mul_Sin) # Use Rx_mul_Sin please

A_rx = 2*(Rx_dot_Sin /TIME_VECTOR_SIZE);

# PRESENTATION
plt.plot(t,Tx,  '-' , label='Tx', color='green')
plt.plot(t,Interfer, '-',  label='Interfer',color='blue')
plt.plot(t,Rx,       '-' , label='Rx',      color='gray', linewidth=1)
plt.ylim(-3.1, 3.1)
plt.legend()
plt.grid()
plt.axhline(y=0,color='black')
plt.show()

plt.fill_between(t,0,Rx_mul_Sin, label='Rx_mul_Sin', color='red',alpha=0.5)
plt.ylim(-3.1, 3.1)
plt.legend()
plt.grid()
plt.axhline(y=0,color='black')
plt.show()

print(f'A_tx={A_tx}')
print(f'A_int={A_int}')
print(f'A_int_phi={A_int_phi:0.2f}')
print(f'Rx_dot_Sin={Rx_dot_Sin:0.1f}')
print(f'A_rx={A_rx:0.1f}')


#=========================================
#figure(figsize=(12, 6), dpi=80)

# plt.plot(modulated_signal,color='blue')
# plt.plot(carier_x_modulated,color='red')

# plt.show()

# periods = np.reshape(,[30,-1]) 


# dots.append(np.dot(sin,sin_shift))