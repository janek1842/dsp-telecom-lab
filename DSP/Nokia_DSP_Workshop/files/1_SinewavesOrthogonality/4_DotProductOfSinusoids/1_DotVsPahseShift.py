import numpy as np
import matplotlib.pyplot as plt
pi = np.pi

phases = [0]
for p in range(1,10):
    phases.append(pi*p/10)

dot_products = []

t = np.linspace(0, 2*pi,30, endpoint=False)

for PHASE_SHIFT in phases:
    Ref = np.sin(t)
    Shifted = np.sin(t+PHASE_SHIFT)
    Ref_mult_Shifted = Ref * Shifted
    
    dot_product = np.dot(Ref, Shifted)
    dot_products.append(dot_product)
    
plt.plot(phases, dot_products,'o-',color='blue')
plt.title('Dot product vs phase_shift')
plt.grid()
plt.xlim(0,3)
plt.xlabel('shift')
plt.ylabel('dot')
plt.show()
