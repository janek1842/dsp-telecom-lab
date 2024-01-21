# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 23:41:00 2023

@author: janfi
"""

import numpy as np
import matplotlib.pyplot as plt
from mapper_lib import ampl_to_symbol

symbol_nr = 2
symbols_l=[]
ampl_l = np.linspace(-1.5,1.5,100)

for ampl in ampl_l:
    symbol = ampl_to_symbol(symbol_nr,ampl)
    symbols_l.append(symbol)    
    
plt.plot(ampl_l,symbols_l,'p')    
     
plt.grid()
plt.xlabel('Amplitude')
plt.ylabel('Symbol')



