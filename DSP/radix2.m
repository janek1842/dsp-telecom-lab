close all; clc; clear all;

% Calculating difference between recursive radix-2 and MATLAB fft
% for a random noise using different p

j=1;
for p=[2,4,6,8,10,12,14,16]
    x = randn((2^p),1);
    
    startFFT = tic; 
    X1 = fft(x);
    timeX1(j) = toc(startFFT);
     
    startMyRec = tic;    
    X2 = myRecFFT(x)';
    timeX2(j) = toc(startMyRec);
    
    err(j) = max(abs(X1-X2));
    timeComparison(j) = (timeX2(j)-timeX1(j));

    j = j + 1;
end

% Ploting the results
p=[2,4,6,8,10,12,14,16];

figure(1);
plot(p,err,'r*-')
title('Difference between recursive radix-2 and MATLAB fft')
xlabel('p');
ylabel('Error')

% Observation
% An error (difference between MATLAB fft and radix-2 increases with the increase of size of the analyzed signal)

% Conclusion #1 (NOT SURE)
% I think with the increase of vector size (2^p) number of 
% calculation operations performed in myRecFFT function also increases.  
% That's why error increases as the matrix is splitted and joined more and more times

% Conclusion #2 (From prof. book) 
% In this radix-2 method we perform (N/2) * log_2_(N) multiplications

% Conclusion #3 (joining two previous Conclusions)
% Observe that figure 1 has logarythmic shape :) 
% That's what prof proved in conclusion 2 !

% Final conclusion: As the number of operation performed increases logarythmic 
% (in another words exponential)the error also reminds exponential curve 

% BONUS! time comparison between MATLAB fft and radix-2
figure(2);
plot(p,timeComparison,'b*-')
title('Time performance: (radix-2 time) - (MATLAB fft time)')
xlabel('p');
ylabel('Time [s]')

% Observation
% Time comparison between radix-2 and MATLAB. For large matrices (p>12)
% The differeence between radix-2 and MATLAB increases. 
% radix-2 is much slower for these values






