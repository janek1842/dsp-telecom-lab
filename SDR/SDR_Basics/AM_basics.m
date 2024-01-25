clear all; close all; clc;

% Input Data
fs=5000; Nx=fs;
dt = 1/fs;
t = dt*(0:Nx-1);
A = 1;
kA = 0.25;
fA = 4;
fc = 100;

f = sin(2*pi*fc*t); % Carrier
m = sin(2*pi*fA*t); % Modulated signal

xAM = A*(1+kA*m).*f; % AM signal, with A: Amplitude,
% kA: Amplitude index, m: Modulated signal and f is the carrier
freq = (-fs/2:fs/2-1);

% Plotting signal in time domain
figure(1);
plot(t,m,'-x');
xlabel('t [s]');
grid on;

% Plotting signal in frequency domain
figure(2);
Y = abs(fftshift(fft(m)));
stem(freq,Y,'-x');
xlabel('f [Hz]');
grid on;

% Plotting AM in time domain
figure(3);
plot(t,xAM,'-x');
xlabel('t [s]');
grid on;

% Plotting AM in frequency domain
figure(4);
Y = abs(fftshift(fft(xAM)));
stem(freq,Y,'-x');
xlabel('f [Hz]');
grid on;
