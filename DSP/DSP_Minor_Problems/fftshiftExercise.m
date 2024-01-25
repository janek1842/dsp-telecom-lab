% SOURCE:
% Cyfrowe przetwarzanie sygnalow. Podstawy, multimedia, transmisja. PWN, Warszawa, 2014.

clc;     clear;    close all;

% Exemplary discrete data
N1=2^4-1;
x=mod(0:N1-1,4);                                 

% DFT of the data (discrete)
X1=fft(x);                                       

% DTFT (analog signal)
K=64; N2=K*N1;                                   
X2=fft(x,N2);                                    

% Data for X axis description
fpr=10;   df1=fpr/N1;    df2=fpr/N2;             
f1=0:df1:(N1-1)*df1; f2=0:df2:(N2-1)*df2;        

% FFTSHIFT transformation
sX1=fftshift(X1);                                
if N1/2==round(N1/2)                            
    sf1=[f1(N1/2+1:end)-fpr,f1(1:N1/2)];         
else                                             
    sf1=[f1((N1+1)/2+1:end)-fpr,f1(1:(N1+1)/2)]; 
end

sX2=fftshift(X2);                                
if N2/2==round(N2/2)
    sf2=[f2(N2/2+1:end)-fpr,f2(1:N2/2)];         
else
    sf2=[f2((N2+1)/2+1:end)-fpr,f2(1:(N2+1)/2)]; 
end

% Plotting the data
figure(1);
subplot(3,1,1); 
        stem(0:N1-1,x);         xlim([0,N1-1]);         grid on;
            set(gca,'fontsize',12,'xtick',0:N1-1);      xlabel('n','fontsize',18);
            
subplot(3,1,2); 
        plot(f2,abs(X2),'b.-');         grid on;        hold on;
        plot(f1,abs(X1),'ro','linewidth',2,'markerface','r');
            set(gca,'fontsize',12);     xlabel('f [Hz]','fontsize',18);
            legend('DTFT','DFT');
            
subplot(3,1,3); 
        plot(sf2,abs(sX2),'b.-');       grid on;        hold on;
        plot(sf1,abs(sX1),'ro','linewidth',2,'markerface','r');
            set(gca,'fontsize',12);     xlabel('f [Hz]','fontsize',18);
            legend('DTFT','DFT');      
                    