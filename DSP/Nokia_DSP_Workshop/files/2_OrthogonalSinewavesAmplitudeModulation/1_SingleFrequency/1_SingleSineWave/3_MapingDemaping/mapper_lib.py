def symbol_to_ampl(symbol_nr, symbol_val):        

    if symbol_nr==2:
        if symbol_val==0: return -1.00
        if symbol_val==1: return +1.00 
        
    if symbol_nr==4:
        if symbol_val==0: return -1.00
        if symbol_val==1: return -0.33 
        if symbol_val==2: return +0.33
        if symbol_val==3: return +1.00 
        
    if symbol_nr==8:
        if symbol_val==0: return -1.000
        if symbol_val==1: return -0.714
        if symbol_val==2: return -0.429
        if symbol_val==3: return -0.143
        if symbol_val==4: return +0.143
        if symbol_val==5: return +0.429
        if symbol_val==6: return +0.714
        if symbol_val==7: return +1.000

def ampl_to_symbol(symbol_nr, ampl):        

    if symbol_nr==2:
        if      ampl < 0 : return 0 
        if  0 < ampl     : return 1 

    if symbol_nr==4:
        if         ampl < -0.66: return 0 
        if -0.66 < ampl <  0.00: return 1
        if  0.00 < ampl < +0.66: return 2 
        if +0.66 < ampl        : return 3  

    if symbol_nr==8:
        if          ampl < -0.857: return 0
        if -0.857 < ampl < -0.571: return 1
        if -0.571 < ampl < -0.286: return 2
        if -0.286 < ampl < +0.000: return 3
        if +0.000 < ampl < +0.286: return 4
        if +0.286 < ampl < +0.571: return 5
        if +0.571 < ampl < +0.857: return 6
        if +0.857 < ampl         : return 7
          