import numpy as np
import matplotlib.pyplot as plt
from mapper_lib import symbol_to_ampl

SYMBOL_NR = 8

symbols_l = range(SYMBOL_NR)
ampl_l = list()
for symbol in symbols_l:
    ampl = symbol_to_ampl(SYMBOL_NR,symbol)
    ampl_l.append(ampl)    
plt.plot(symbols_l,ampl_l,'p')    
    
plt.grid()
plt.title(f'Symbol nr: {SYMBOL_NR}')
plt.xlabel('Symbol')
plt.ylabel('Amplitude')

