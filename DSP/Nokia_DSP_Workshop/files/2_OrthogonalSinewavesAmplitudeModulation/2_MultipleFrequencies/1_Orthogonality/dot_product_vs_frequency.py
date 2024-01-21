import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 2*np.pi,30, endpoint=False)
sin_blue  = np.cos(t)

dot_l = list()
freq_l = np.linspace(0, 3, 100)

for freq in freq_l:    
    sin_green = np.cos(t*freq)
    dot_l.append(np.dot(sin_blue,sin_green))
    
plt.plot(freq_l, dot_l)
plt.axhline(y=0,color='black')
plt.title('dot of "blue" and "green" frequencies when "blue" frequency equals to 1')
plt.xlabel('"green" frequency')
plt.ylabel('dot')
plt.grid()
plt.show()

