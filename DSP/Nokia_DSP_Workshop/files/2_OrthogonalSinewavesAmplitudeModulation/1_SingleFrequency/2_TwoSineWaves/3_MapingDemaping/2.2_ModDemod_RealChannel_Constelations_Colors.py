import numpy as np
import matplotlib.pyplot as plt
pi = np.pi

# PARAMETERS
TIME_VECTOR_SIZE = 60

AMPL_VECTOR_SIN = (1,-1,1,-1)
AMPL_VECTOR_COS = (1,1,-1,-1)

# CALCULATION
t = np.linspace(0, 2*pi,TIME_VECTOR_SIZE, endpoint=False)

carrier_sin = ref_sin = np.sin(t) 
carrier_cos = ref_cos = np.cos(t) 

errors_sin = []
errors_cos = []

NOISE_DEVIATION=6
TRANSMISSION_NR=10

amplitudes_sin = list()
amplitudes_cos = list()

j=0;
for i in range(TRANSMISSION_NR):
    for ampl_sin, ampl_cos in zip(AMPL_VECTOR_SIN, AMPL_VECTOR_COS):
        
        # modulation
        Tx = (ampl_sin*carrier_sin) + (ampl_cos*carrier_cos)     
        
        # real channel
        Rx = Tx + np.random.normal(0,NOISE_DEVIATION,len(Tx))
            
        # demodulation
        ampl_s = (np.dot(Rx,ref_sin)/TIME_VECTOR_SIZE)*2
        errors_sin.append(ampl_s-ampl_sin)
        amplitudes_sin.append(ampl_s)
        
        ampl_c = (np.dot(Rx,ref_cos)/TIME_VECTOR_SIZE)*2  
        errors_cos.append(ampl_c-ampl_cos)
        amplitudes_cos.append(ampl_c)
        
        plt.scatter(ampl_c,ampl_s,color=('red','green','orange','blue')[j%4])
        j=j+1
        
# amplitudes
amplitudes_sin = np.array(amplitudes_sin) # convert list to numpy 1D array
amplitudes_cos = np.array(amplitudes_cos) # ...
errors_sin = np.array(errors_sin)
errors_cos = np.array(errors_cos)

np.set_printoptions(precision=2)          # set numpy array print precision

# PRESENTATION  

plt.title("RX amplitudes")
plt.xlabel("cos ampl.")
plt.ylabel("sin ampl.")
plt.xlim(-4,4)
plt.ylim(-4,4)
plt.axhline(y=0, lw=3, color='k')
plt.axvline(x=0, lw=3, color='k')

plt.axis()
plt.grid()
plt.show()
