function X = myRecFFT(x)

N = length(x); %number of signal samples

if (N==2)
    X(1) = x(1) + x(2);
    X(2) = x(1) - x(2);
else
    X1 = myRecFFT(x(1:2:N));
    X2 = myRecFFT(x(2:2:N));
    X = [X1 X1] + exp(-1i*2*pi/N*(0:N-1)).* [X2 X2];
end