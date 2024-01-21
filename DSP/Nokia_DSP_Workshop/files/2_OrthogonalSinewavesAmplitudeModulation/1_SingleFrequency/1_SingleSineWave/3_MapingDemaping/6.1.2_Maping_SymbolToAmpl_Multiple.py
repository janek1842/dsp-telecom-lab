import numpy as np
import matplotlib.pyplot as plt
from mapper_lib import symbol_to_ampl

for symbol_nr in 2,4,8:
    symbols_l = range(8)
    ampl_l = list()
    for symbol in symbols_l:
        ampl = symbol_to_ampl(symbol_nr,symbol)
        ampl_l.append(ampl)    
    plt.plot(symbols_l,ampl_l,'p', label="symbol nr = "+str(symbol_nr))    
    
plt.legend()    
plt.grid()
plt.xlabel('Symbol')
plt.ylabel('Amplitude')



