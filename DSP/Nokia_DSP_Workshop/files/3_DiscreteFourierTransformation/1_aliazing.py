import numpy as np
import matplotlib.pyplot as plt

INFINIT_SAMPLE_RATE = 100 # infinity sample rate imitation (analog signal)
FINIT_SAMPLE_RATE = 10    # real (finit) sample rate

SIN_FREQ = 2

t_ideal    = np.linspace(0, 2*np.pi, INFINIT_SAMPLE_RATE, endpoint=False)
t_sampled  = np.linspace(0, 2*np.pi, FINIT_SAMPLE_RATE, endpoint=False)

sin_ideal   =  np.sin(SIN_FREQ*t_ideal)
sin_sampled =  np.sin(SIN_FREQ*t_sampled)

plt.plot(t_ideal,sin_ideal,label="inf")
plt.plot(t_sampled,sin_sampled,'p-',label="low")

plt.axhline(0,color='black', linewidth=1)
plt.title(f'sine frequency = {SIN_FREQ}')
plt.legend()





