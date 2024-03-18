% lab03_ofdm_cp1.m - simple example of 4-QAM OFDM-based transmission
% with cyclic prefix-based OFDM symbol synchronization and CFO correction
  clear all; close all;

%% Parameters
scs = 30e+3;             % sub-carrier spacing in Hz
Nfft = 256;              % number of sub-carriers, i.e. FFT length of the OFDM symbol
Ncp = 18;                % Cyclic Prefix (CP) length, e.g. 18 (short), 22 (long)
SNR = 3000;                % Signal-to-Noise-Ratio in dB
G  = [1.0,  0.5,     0.25   ];  % channel gains: 1, 0.9, 0.75, 0.5, ...5
ph = [-pi/20, -pi/5, -pi/7];  % channel phase shifts: 0, -pi/20, -pi/10, -pi/4, -pi/2, ... 
D = 0;                   % channel delay in samples: -2,-1,0,1,2,...
dD = 0;                % channel delay in fraction of samples: 0.01, 0.1, 0.25, ...
df = 9000;               % carrier freqiency offset (CFO) [Hz]: 0, 10, 100, 1000, ...
shifted_indices=[-3,-2,-1,0,1,2,3];
added_cfo_percentage=[0.001,0.005,0.01,0.02,0.05,0.1,0.5];

fs = scs*Nfft;           % sampling frequency
Nsymb = Ncp + Nfft;      % OFDM symbol length with cyclic prefix

for jj = 1:length(shifted_indices)
    errors_IND(jj)=0;
    %% Transmitter
    %         0,    1,   2,   3                         % carrier states numbers
    %         00,   01,  10,  11                        % corresponding bits
    iqTAB = [ -1-j; -1+j; 1-j; 1+j ];                   % IQ states for QAM4 modulation
    
    numTX   = randi([0,3],Nfft,1);                      % random TX symbol numbers
    scrambl = randi([0,3],Nfft,1);                      % random scrambling numbers
    numscTX = double(bitxor( uint8(numTX), uint8(scrambl) ));  % scrambling operation
    iqTX  = iqTAB( numscTX+1 );                         % sequence of TX IQ freq states
    sigTX = ifft( iqTX );                               % sequence of TX time samples
    sigTX = [ sigTX(Nfft-Ncp+1:Nfft); sigTX ];          % addition of cyclic prefix
    sigRND = sigTX( randperm(length(sigTX)) );          % random signal
    sigTX = [ sigRND; sigTX; sigRND  ];                 % transmitted signal (one symbol)
    Ns = length( sigTX );                               % transmitted signal length

    %% Channel influence
    
    for i = 1:3
        sigTXs = awgn(sigTX,SNR,'measured');                 % additive white Gaussian noise
    end
    
    sigTX = circshift( sigTX, D );                      % channel delay in samples
    if( dD ~= 0)                                        % channel delay in fraction of samples
        sigTX = interp1( [0:1:Ns-1]', sigTX(1:Ns), [0-dD:1:Ns-1-dD]','spline');
    end
    %sigTX = G(1)*exp(j*ph(1)) * sigTX;                  % one-path channel influence (gain, shift)
    %sigTX = conv( sigTX,[G(1)*exp(j*ph(1)), G(2)*exp(j*ph(2)), G(3)*exp(j*ph(3))],'same');  % three-path
    
    sigTX = sigTX .* exp(j*2*pi*df/fs*(0:Ns-1)');       % carrier frequency offset
    
    %% ADDED START #############################################################
    
    % Find start sample of the time slot using cyclic prefix 
    [max_corr_index, correlations] = find_symbol_start( sigTX, Nfft, Ncp, Ncp );
    
    max_corr_index = max_corr_index + shifted_indices(jj);

    % Time alignment - start from 1st samples of the OFDM symbol cyclic prefix 
    sigTX = circshift( sigTX, -1*(max_corr_index-1) );
    
    % Carrier frequency offset estimation and correction using cyclic prefix 
    [sigTX, cfo] = estim_correct_cfo( sigTX, Nfft, Ncp,0);
    
    %fprintf('Estimated CFO = %f Hz\n', cfo*scs),
    
    % ADDED STOP ##############################################################
    
    %% Receiver - demodulation and symbol detection (without OFDM symbol synchronization) 
    sigRX = sigTX( 1 : Nsymb );                   % extracting the OFDM symbol         
    sigRX = sigRX( Ncp+1 : Nsymb );               % removing cyclic prefix
    iqRX(jj,:)  = fft( sigRX );                         % going to freq domain (demod)
    numscRX = [];                                                          %
    
    for k = 1 : Nfft                                                       % 
        if( real(iqRX(jj,k))<=0 && imag(iqRX(jj,k))<=0 ) numscRX(k,1) = 0; end   % IQ states 
        if( real(iqRX(jj,k))<=0 && imag(iqRX(jj,k))>=0 ) numscRX(k,1) = 1; end   % detection
        if( real(iqRX(jj,k))>=0 && imag(iqRX(jj,k))<=0 ) numscRX(k,1) = 2; end   %
        if( real(iqRX(jj,k))>=0 && imag(iqRX(jj,k))>=0 ) numscRX(k,1) = 3; end   %
    end                                                                    %
    
    numRX = double( bitxor( uint8(numscRX), uint8(scrambl) ) );  % scrambling operation
    errors_IND(jj) = sum( ~(numTX==numRX) );
end

% Observe in figure that for df~=0 some phase rotation is left which should be cancelled
figure;
sgtitle('Indice Shift CFO Analysis')
subplot(421); plot(iqTX,'bx'); axis square; axis([-3, 3, -3, 3]); title('IQ of TX');
title('TX constellation');
subplot(422); plot(iqRX(1,:),'bx'); axis square; axis([-3, 3, -3, 3]); 
title('RX indice shift: ',shifted_indices(1));
subplot(423); plot(iqRX(2,:),'bx'); axis square; axis([-3, 3, -3, 3]); 
title('RX indice shift: ',shifted_indices(2));
subplot(424); plot(iqRX(3,:),'bx'); axis square; axis([-3, 3, -3, 3]); 
title('RX indice shift: ',shifted_indices(3));
subplot(425); plot(iqRX(4,:),'bx'); axis square; axis([-3, 3, -3, 3]); 
title('RX indice shift: ',shifted_indices(4));
subplot(426); plot(iqRX(5,:),'bx'); axis square; axis([-3, 3, -3, 3]); 
title('RX indice shift: ',shifted_indices(5));
subplot(427); plot(iqRX(6,:),'bx'); axis square; axis([-3, 3, -3, 3]); 
title('RX indice shift: ',shifted_indices(6));
subplot(428); plot(iqRX(7,:),'bx'); axis square; axis([-3, 3, -3, 3]); 
title('RX indice shift: ',shifted_indices(7));

for jj = 1:length(added_cfo_percentage)
    errors_CFO(jj)=0;
    %% Transmitter
    %         0,    1,   2,   3                         % carrier states numbers
    %         00,   01,  10,  11                        % corresponding bits
    iqTAB = [ -1-j; -1+j; 1-j; 1+j ];                   % IQ states for QAM4 modulation
    
    numTX   = randi([0,3],Nfft,1);                      % random TX symbol numbers
    scrambl = randi([0,3],Nfft,1);                      % random scrambling numbers
    numscTX = double(bitxor( uint8(numTX), uint8(scrambl) ));  % scrambling operation
    iqTX  = iqTAB( numscTX+1 );                         % sequence of TX IQ freq states
    sigTX = ifft( iqTX );                               % sequence of TX time samples
    sigTX = [ sigTX(Nfft-Ncp+1:Nfft); sigTX ];          % addition of cyclic prefix
    sigRND = sigTX( randperm(length(sigTX)) );          % random signal
    sigTX = [ sigRND; sigTX; sigRND  ];                 % transmitted signal (one symbol)
    Ns = length( sigTX );                               % transmitted signal length


    %% Channel influence
    
    for i = 1:3
        sigTXs = awgn(sigTX,SNR,'measured');                 % additive white Gaussian noise
    end
    
    sigTX = circshift( sigTX, D );                      % channel delay in samples
    if( dD ~= 0)                                        % channel delay in fraction of samples
        sigTX = interp1( [0:1:Ns-1]', sigTX(1:Ns), [0-dD:1:Ns-1-dD]','spline');
    end
    %sigTX = G(1)*exp(j*ph(1)) * sigTX;                  % one-path channel influence (gain, shift)
    %sigTX = conv( sigTX,[G(1)*exp(j*ph(1)), G(2)*exp(j*ph(2)), G(3)*exp(j*ph(3))],'same');  % three-path
    
    sigTX = sigTX .* exp(j*2*pi*df/fs*(0:Ns-1)');       % carrier frequency offset
    
    %% ADDED START #############################################################
    
    % Find start sample of the time slot using cyclic prefix 
    [max_corr_index, correlations] = find_symbol_start( sigTX, Nfft, Ncp, Ncp );
    
    % Time alignment - start from 1st samples of the OFDM symbol cyclic prefix 
    sigTX = circshift( sigTX, -1*(max_corr_index-1) );
    
    % Carrier frequency offset estimation and correction using cyclic prefix 
    [sigTX, cfo] = estim_correct_cfo( sigTX, Nfft, Ncp , added_cfo_percentage(jj));
    
    %fprintf('Estimated CFO = %f Hz\n', cfo*scs),
    
    % ADDED STOP ##############################################################
    
    %% Receiver - demodulation and symbol detection (without OFDM symbol synchronization) 
    sigRX = sigTX( 1 : Nsymb );                   % extracting the OFDM symbol         
    sigRX = sigRX( Ncp+1 : Nsymb );               % removing cyclic prefix
    iqRX(jj,:)  = fft( sigRX );                         % going to freq domain (demod)
    numscRX = [];                                                          %
    
    for k = 1 : Nfft                                                       % 
        if( real(iqRX(jj,k))<=0 && imag(iqRX(jj,k))<=0 ) numscRX(k,1) = 0; end   % IQ states 
        if( real(iqRX(jj,k))<=0 && imag(iqRX(jj,k))>=0 ) numscRX(k,1) = 1; end   % detection
        if( real(iqRX(jj,k))>=0 && imag(iqRX(jj,k))<=0 ) numscRX(k,1) = 2; end   %
        if( real(iqRX(jj,k))>=0 && imag(iqRX(jj,k))>=0 ) numscRX(k,1) = 3; end   %
    end                                                                    %
    
    numRX = double( bitxor( uint8(numscRX), uint8(scrambl) ) );  % scrambling operation
    errors_CFO(jj) = sum( ~(numTX==numRX) );
end

figure;
sgtitle('CFO Percentage Add ')
subplot(421); plot(iqTX,'bx'); axis square; axis([-3, 3, -3, 3]); title('IQ of TX');
title('TX constellation');
subplot(422); plot(iqRX(1,:),'bx'); axis square; axis([-3, 3, -3, 3]); 
title('RX cfo percentage add:',added_cfo_percentage(1)*100);
subplot(423); plot(iqRX(2,:),'bx'); axis square; axis([-3, 3, -3, 3]);
title('RX cfo percentage add:',added_cfo_percentage(2));
subplot(424); plot(iqRX(3,:),'bx'); axis square; axis([-3, 3, -3, 3]);
title('RX cfo percentage add:',added_cfo_percentage(3));
subplot(425); plot(iqRX(4,:),'bx'); axis square; axis([-3, 3, -3, 3]);
title('RX cfo percentage add:',added_cfo_percentage(4));
subplot(426); plot(iqRX(5,:),'bx'); axis square; axis([-3, 3, -3, 3]);
title('RX cfo percentage add:',added_cfo_percentage(5));
subplot(427); plot(iqRX(6,:),'bx'); axis square; axis([-3, 3, -3, 3]); 
title('RX cfo percentage add:',added_cfo_percentage(6));
subplot(428); plot(iqRX(7,:),'bx'); axis square; axis([-3, 3, -3, 3]); 
title('RX cfo percentage add:',added_cfo_percentage(7));
