% lab_01_ofdm_intro3.m - simple transmission of 8 bits using QAM4 modulation
clc; clear all; close all;

Nfft = 512; % number of subcarriers

%---------------------------------------------------------------

% QPSK
iqTAB5=exp(j*pi/4*[ 5 3 7 1 ]); % corresponding IQ carrier states for QPSK

% 8-PSK
iqTAB8=exp(1i*pi/8*[ 11 9 5 7 13 15 3 1 ]); % corresponding IQ carrier states for PSK-8

% 8-PAM
iqTAB1=[ -7 -5 -1 -3 7 5 1 3 ]; % corresponding IQ carrier states for PAM-8

% 4-PAM
iqTAB2=[ -3 -1 3 1 ]; % corresponding IQ carrier states for PAM-4

% QAM-4
iqTAB4 = [-1-j,-1+j,+1-j,+1+j ];    % corresponding IQ carrier states for QAM-4

% QAM-16
iqTAB16 = [ -3-3*j, -3-1*j, -3+3*j, -3+1*j, ...
                                     -1-3*j, -1-1*1i, -1+3*j, -1+1*j, ...
                                     +3-3*j, +3-1*j, +3+3*j, +3+1*j, ...
                                     +1-3*j, +1-1*j, +1+3*j, +1+1*j]; % corresponding IQ carrier states for QAM-16

SNRS = [-70,-60,-50,-40,-30,-25,-20,-15,-10,-5,0];
results=zeros(size(SNRS,2),6);

myText = 'testtesttesttesttesttesttesttesttesttesttesttest';
repetitions=10;

for mm = 1:6
    for r = 1:repetitions
        for z = 1:length(SNRS)
            tic
            finaltext = ''; % decoded text
            
            SNR = SNRS(z);
            if mm==1
                iqTAB = iqTAB4;
                mod = '4QAM';
                N_BITS_PER_SYMBOL=2;
            elseif mm==2
                iqTAB = iqTAB16;
                mod = '16QAM';
                N_BITS_PER_SYMBOL=4;
            elseif mm==3
                iqTAB = iqTAB2;
                mod = '4PAM';
                N_BITS_PER_SYMBOL=2;
            elseif mm==4
                iqTAB = iqTAB1;
                mod = '8PAM';
                N_BITS_PER_SYMBOL=3;
            elseif mm==5
                iqTAB = iqTAB5;
                mod = 'QPSK';
                N_BITS_PER_SYMBOL=2;
            elseif mm==6
                iqTAB = iqTAB8;
                mod = '8PSK';
                N_BITS_PER_SYMBOL=3;
            end

            Ns = length(iqTAB);                           % length of the IQ states table
            numTX=text2numbers(myText,N_BITS_PER_SYMBOL); % Transforming input text to numbers
            
            numTX = numTX(1:end-1,:);     
            iqTX = numbers2IQ(numTX,mod,iqTAB);           % IQ carrier states for selected letter
            X = zeros(Nfft,1);
           
            for i = 1:Ns:length(iqTX)    
                
                X(1:Ns,1) = iqTX(i:i+Ns-1);      % mapping IQ states to carriers
                
                x = ifft(ifftshift(X));                     % TX: signal synthesis and transmission  
                y = awgn(x,SNR,'measured');                            % channel: addition of noise for given SNR [dB]
                
                Y = fftshift( fft( y ) );                   % RX: signal analysis
                iqRX = Y(1:Ns);                             % demapping IQ states from carriers
                
                mynumb= numbers2text(IQ2numbers(iqRX,mod),N_BITS_PER_SYMBOL); % Transforming bits to text
            
                finaltext = append(finaltext,mynumb);    
            end
                    
            numDifferences = 0;
            
            for i = 1:strlength(finaltext)
                if myText(1,i) ~= finaltext(1,i)
                    numDifferences = numDifferences + 1; % Increment the counter for differences
                end
            end
            
            % Display the number of errors
            fprintf('Number of errors for %s modulation: %d\n', mod,numDifferences);
            fprintf('%s %s\n', "DECODED TEXT:", finaltext);
            results(z,mm)=(results(z,mm)+numDifferences);
        end
    end
end

figure(1)
plot(SNRS,results(:,1)/repetitions,'ro-');
hold on
plot(SNRS,results(:,2)/repetitions,'bx-');
hold on
plot(SNRS,results(:,3)/repetitions,'gx-');
hold on
plot(SNRS,results(:,4)/repetitions,'blo-');
hold on
plot(SNRS,results(:,5)/repetitions,'c*-');
hold on
plot(SNRS,results(:,6)/repetitions,'o--');
legend('4QAM','16QAM','4PAM','8PAM','QPSK','8PSK')
xlabel('SNR [db]');
ylabel('Number of errors');
hold off



