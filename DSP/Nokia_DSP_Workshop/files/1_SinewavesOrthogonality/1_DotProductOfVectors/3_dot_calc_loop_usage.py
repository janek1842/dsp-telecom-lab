green = [0.080,0.080,0.080,0.398,0.477,0.000,-0.477,-0.398,-0.080,-0.080,-0.080]
blue  = [0.088,0.088,0.088,0.442,0.530,0.000,-0.530,-0.442,-0.088,-0.088,-0.088]

dot_product = 0
for i in range(len(green)): # i = 0,..len(green)-1 
    dot_product += green[i] * blue[i]

print(round(dot_product,6))

