clear all; close all; 

Nx = 2000;
fs = 2000; 
fc = 200;
fm = 2; df = 50;

dt = 1/fs;
t = dt * (0:Nx-1);

xm = sin(2*pi*fm*t);
x = exp (1i * (2*pi*0*t + 2*pi*df/fs*cumsum(xm)));

plot(t,x)

c = cos (2*pi*fc*t);
s = sin (2*pi*fc*t);

xUp = x.*(c+1i*s);
xUpReal = real(xUp);
