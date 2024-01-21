# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 00:21:37 2023

@author: janfi
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 23:41:00 2023

@author: janfi
"""

import numpy as np
import matplotlib.pyplot as plt
from mapper_lib import ampl_to_symbol

ampl_l = np.linspace(-1.5,1.5,1000)


for symbol_nr in 2,4,8:
    symbols_l=[]
    for ampl in ampl_l:
        symbol = ampl_to_symbol(symbol_nr,ampl)
        symbols_l.append(symbol)    
    plt.plot(ampl_l,symbols_l,label="symbol nr = "+str(symbol_nr))    
     
plt.grid()
plt.legend()
plt.xlabel('Amplitude')
plt.ylabel('Symbol')


