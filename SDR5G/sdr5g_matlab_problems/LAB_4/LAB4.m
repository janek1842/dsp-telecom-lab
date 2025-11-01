% lab04_ofdm_sigref3_rayleigh.m
% Example of OFDM transmission over simulated Rayleigh fading channel.
% Multiple OFDM symbols are generated. Reference and data subcarriers are 
% separated in different symbols. 
% This example assumes:
%   1) perfect time synchronization
%   2) perfect frequency synchronization (no CFO)
%   3) multipath, time-varying fading chnannel with Rayleigh distribution

clc;clear all; close all; 

N_slots = 4;   % simulation takes 3 slots
SNRS = [-700,-600,-500,-400,-300,-200,-100,100,200,300,400,500,600,700];      % assumed Signal-to-Noise Ratio
MaximumDopplerShifts = [100,400,800,1200,1600,2000,2400,2800,3200,3600,4000];
scss = [15e3,30e3,45e3,60e3,75e3,90e3,105e3,130e3,145e3,160e3,175e3,190e3,205e3,220e3,235e3,250e3];
CPs = [2,4,8,12,16,20,24,28,32];

no_of_errors_snrs = [];
no_of_errors_shifts = [];
no_of_errors_scss = [];

for i = 1:length(SNRS)

    % OFDM system parameters
    scs = 15e3;                % subcarrier spacing [Hz]
    N_fft = 256;               % FFT size
    N_sc = 132;                % number of subcarriers used for data transmissions
    N_cp_1st = 22;             % cyclic prefix length of the first symbol in slot
    N_cp_other = 18;           % cyclic prefix length of the other symbol in slot
    N_symbols_per_slot = 14;   % number of symbols in slot
    F_s = scs * N_fft;         % sampling frequency
    
    % Initialize Rayleigh fading channel model object
    PathDelays = [0, 4, 10] / F_s;    % tap delays of multipath propagation channel
    AveragePathGains = [0, -4, -10];  % tap gains (in dB) of multipath propagation channel
    MaximumDopplerShift = 2500;        % maximum Doppler shift for the user (note Doppler shift maps to user velocity)
    rayleigh = comm.RayleighChannel('SampleRate', scs*N_fft, 'PathDelays', PathDelays, ...
              'AveragePathGains', AveragePathGains, 'MaximumDopplerShift', MaximumDopplerShift);
    
    % % % % % % % %
    % Transmitter 
    
    QAM4 = [ -1-1i; -1+1i; 1-1i; 1+1i ] / sqrt(2); % IQ states for QPSK modulation
 
    pilot_symbol_idx = 1 : (N_symbols_per_slot/2) : N_slots*N_symbols_per_slot;
    numTXref = randi( [0,3], N_sc, numel(pilot_symbol_idx) );  % REF pilot IQ
    iqTXref  = QAM4( numTXref+1 );                             % REF TX IQ freq states
    
    % fill the time-frequency array in the transmitted by IQ samples for pilots
    % and data
    iqTX( :, pilot_symbol_idx ) = iqTXref;
    
    for n = 1 : N_slots * N_symbols_per_slot
       if ~ismember( n, pilot_symbol_idx )
          % data symbol - generate random QAM data
          iqTX(:,n) = QAM4( randi([0,3], N_sc, 1) + 1 );
       end
    end

    % OFDM modulation
    sigTX = ofdma_mod_final( iqTX, N_fft, N_sc, N_symbols_per_slot, N_cp_1st, N_cp_other );
    
    % % % % % % % %
    % Channel
    
    % apply Rayleigh fading channel (multipath and mobility)
    % assume no time and frequency synchronization errors
    sigRX = rayleigh( sigTX );     % function from Comm Toolbox
    sigRX = awgn( sigRX, SNRS(i) );    % Matlab function
    
    % % % % % % % %
    % Receiver 
    
    % no time and frequency synchronization done (for simplicity)
    iqRX = ofdma_demod_final( sigRX, N_fft, N_sc, N_symbols_per_slot, N_cp_1st, N_cp_other );
    
    % Extract pilot subcarriers
    iqRXref = iqRX(:, pilot_symbol_idx);
    
    % Channel Estimation (Least Squares)
    H_est = iqRXref ./ iqTXref;
    
    % Interpolation of channel estimation in time and frequency
    X = repmat( reshape( pilot_symbol_idx, 1, [] ), [N_sc 1] );
    Y = repmat( reshape( 1:N_sc, [], 1), [1 length(pilot_symbol_idx)] );
    Xq = repmat(  1:size(iqRX,2),   [size(iqRX,1) 1] );
    Yq = repmat( (1:size(iqRX,1))', [1 size(iqRX,2)] );
    
    H_est_int = interp2( X, Y, H_est, Xq, Yq, 'spline');
    H_est_linear = interp2( X, Y, H_est, Xq, Yq, 'linear');
    H_est_nearest = interp2( X, Y, H_est, Xq, Yq, 'nearest');
    H_est_cubic = interp2( X, Y, H_est, Xq, Yq, 'cubic');

    % Equalization
    iqRX_eq_s = iqRX ./ H_est_int;
    iqRX_eq_l = iqRX ./ H_est_linear;
    iqRX_eq_n = iqRX ./ H_est_nearest;
    iqRX_eq_c = iqRX ./ H_est_cubic;

    % calculate and plot error averaged per symbol
    error_per_symbol_s = mean(abs(iqTX - iqRX_eq_s));
    error_per_symbol_l = mean(abs(iqTX - iqRX_eq_l));
    error_per_symbol_n = mean(abs(iqTX - iqRX_eq_n));
    error_per_symbol_c = mean(abs(iqTX - iqRX_eq_c));

    no_of_errors_snr_s(i) = max(error_per_symbol_s);
    no_of_errors_snr_l(i) = max(error_per_symbol_l);
    no_of_errors_snr_n(i) = max(error_per_symbol_n);
    no_of_errors_snr_c(i) = max(error_per_symbol_c);

end

figure(1)
subplot(2,1,1); 
plot(SNRS,no_of_errors_snr_s,'o-'); grid;
hold on;
plot(SNRS,no_of_errors_snr_l,'x-'); grid;
hold on;
plot(SNRS,no_of_errors_snr_n,'o--'); grid;
hold on;
plot(SNRS,no_of_errors_snr_c,'x--'); grid;
legend('spline','linear','nearest','cubic');
xlabel('SNRs')
ylabel('Max no. of errors per symbol')
title('No. of Errors SNR Analysis Per Symbol');

subplot(2,1,2); 
plot(error_per_symbol_s,'o-'); grid;
hold on;
plot(error_per_symbol_l,'x-'); grid;
hold on;
plot(error_per_symbol_n,'o--'); grid;
hold on;
plot(error_per_symbol_c,'x--'); grid;
legend('spline','linear','nearest','cubic');
xlabel('Id of Symbol')
ylabel('Mean no. of errors per symbol')
title('No. of Errors Analysis Per Symbol');

%% Analysis of SCS Impact

for i = 1:length(scss)

    SNR = 15e3;
    % OFDM system parameters
    scs = scss(i);                % subcarrier spacing [Hz]
    N_fft = 256;               % FFT size
    N_sc = 132;                % number of subcarriers used for data transmissions
    N_cp_1st = 22;             % cyclic prefix length of the first symbol in slot
    N_cp_other = 18;           % cyclic prefix length of the other symbol in slot
    N_symbols_per_slot = 14;   % number of symbols in slot
    F_s = scs * N_fft;         % sampling frequency
    
    % Initialize Rayleigh fading channel model object
    PathDelays = [0, 4, 10] / F_s;    % tap delays of multipath propagation channel
    AveragePathGains = [0, -4, -10];  % tap gains (in dB) of multipath propagation channel
    MaximumDopplerShift = 2500;        % maximum Doppler shift for the user (note Doppler shift maps to user velocity)
    rayleigh = comm.RayleighChannel('SampleRate', scs*N_fft, 'PathDelays', PathDelays, ...
              'AveragePathGains', AveragePathGains, 'MaximumDopplerShift', MaximumDopplerShift);
    
    % % % % % % % %
    % Transmitter 
    
    QAM4 = [ -1-1i; -1+1i; 1-1i; 1+1i ] / sqrt(2); % IQ states for QPSK modulation
 
    pilot_symbol_idx = 1 : (N_symbols_per_slot/2) : N_slots*N_symbols_per_slot;
    numTXref = randi( [0,3], N_sc, numel(pilot_symbol_idx) );  % REF pilot IQ
    iqTXref  = QAM4( numTXref+1 );                             % REF TX IQ freq states
    
    % fill the time-frequency array in the transmitted by IQ samples for pilots
    % and data
    iqTX( :, pilot_symbol_idx ) = iqTXref;
    
    for n = 1 : N_slots * N_symbols_per_slot
       if ~ismember( n, pilot_symbol_idx )
          % data symbol - generate random QAM data
          iqTX(:,n) = QAM4( randi([0,3], N_sc, 1) + 1 );
       end
    end

    % OFDM modulation
    sigTX = ofdma_mod_final( iqTX, N_fft, N_sc, N_symbols_per_slot, N_cp_1st, N_cp_other );
    
    % % % % % % % %
    % Channel
    
    % apply Rayleigh fading channel (multipath and mobility)
    % assume no time and frequency synchronization errors
    sigRX = rayleigh( sigTX );     % function from Comm Toolbox
    sigRX = awgn( sigRX, SNR );    % Matlab function
    
    % % % % % % % %
    % Receiver 
    
    % no time and frequency synchronization done (for simplicity)
    iqRX = ofdma_demod_final( sigRX, N_fft, N_sc, N_symbols_per_slot, N_cp_1st, N_cp_other );
    
    % Extract pilot subcarriers
    iqRXref = iqRX(:, pilot_symbol_idx);
    
    % Channel Estimation (Least Squares)
    H_est = iqRXref ./ iqTXref;
    
    % Interpolation of channel estimation in time and frequency
    X = repmat( reshape( pilot_symbol_idx, 1, [] ), [N_sc 1] );
    Y = repmat( reshape( 1:N_sc, [], 1), [1 length(pilot_symbol_idx)] );
    Xq = repmat(  1:size(iqRX,2),   [size(iqRX,1) 1] );
    Yq = repmat( (1:size(iqRX,1))', [1 size(iqRX,2)] );
    
    H_est_int = interp2( X, Y, H_est, Xq, Yq, 'spline');
    H_est_int_linear = interp2( X, Y, H_est, Xq, Yq, 'linear');
    H_est_int_nearest = interp2( X, Y, H_est, Xq, Yq, 'nearest');
    H_est_int_cubic = interp2( X, Y, H_est, Xq, Yq, 'cubic');

    % Equalization
    iqRX_eq_s = iqRX ./ H_est_int;
    iqRX_eq_l = iqRX ./ H_est_int_linear;
    iqRX_eq_n = iqRX ./ H_est_int_nearest;
    iqRX_eq_c = iqRX ./ H_est_int_cubic;

    % calculate and plot error averaged per symbol
    error_per_symbol_s = mean(abs(iqTX - iqRX_eq_s));
    error_per_symbol_l = mean(abs(iqTX - iqRX_eq_l));
    error_per_symbol_n = mean(abs(iqTX - iqRX_eq_n));
    error_per_symbol_c = mean(abs(iqTX - iqRX_eq_c));

    no_of_errors_scs_s(i) = max(error_per_symbol_s);
    no_of_errors_scs_l(i) = max(error_per_symbol_l);
    no_of_errors_scs_n(i) = max(error_per_symbol_n);
    no_of_errors_scs_c(i) = max(error_per_symbol_c);
end

figure(2)
subplot(2,1,1); 
plot(scss,no_of_errors_scs_s,'o-'); grid;
hold on;
plot(scss,no_of_errors_scs_l,'x-'); grid;
hold on;
plot(scss,no_of_errors_scs_n,'o--'); grid;
hold on;
plot(scss,no_of_errors_scs_c,'x--'); grid;
legend('spline','linear','nearest','cubic');
xlabel('SCS')
ylabel('Max no. of errors per symbol')
title('No. of Errors SCS Analysis Per Symbol');

subplot(2,1,2); 
plot(error_per_symbol_s,'o-'); grid;
hold on;
plot(error_per_symbol_l,'x-'); grid;
hold on;
plot(error_per_symbol_n,'o--'); grid;
hold on;
plot(error_per_symbol_c,'x--'); grid;
legend('spline','linear','nearest','cubic');
xlabel('Id of Symbol')
ylabel('Mean no of errors per symbol')
title('No. of Errors Analysis Per Symbol');

%% Analysis of Max Doppler Shift Impact

for i = 1:length(MaximumDopplerShifts)

    SNR = 15e3;
    % OFDM system parameters
    scs = 15e3;                % subcarrier spacing [Hz]
    N_fft = 256;               % FFT size
    N_sc = 132;                % number of subcarriers used for data transmissions
    N_cp_1st = 22;             % cyclic prefix length of the first symbol in slot
    N_cp_other = 18;           % cyclic prefix length of the other symbol in slot
    N_symbols_per_slot = 14;   % number of symbols in slot
    F_s = scs * N_fft;         % sampling frequency
    
    % Initialize Rayleigh fading channel model object
    PathDelays = [0, 4, 10] / F_s;    % tap delays of multipath propagation channel
    AveragePathGains = [0, -4, -10];  % tap gains (in dB) of multipath propagation channel
    MaximumDopplerShift = MaximumDopplerShifts(i);        % maximum Doppler shift for the user (note Doppler shift maps to user velocity)
    rayleigh = comm.RayleighChannel('SampleRate', scs*N_fft, 'PathDelays', PathDelays, ...
              'AveragePathGains', AveragePathGains, 'MaximumDopplerShift', MaximumDopplerShift);
    
    % % % % % % % %
    % Transmitter 
    
    QAM4 = [ -1-1i; -1+1i; 1-1i; 1+1i ] / sqrt(2); % IQ states for QPSK modulation
 
    pilot_symbol_idx = 1 : (N_symbols_per_slot/2) : N_slots*N_symbols_per_slot;
    numTXref = randi( [0,3], N_sc, numel(pilot_symbol_idx) );  % REF pilot IQ
    iqTXref  = QAM4( numTXref+1 );                             % REF TX IQ freq states
    
    % fill the time-frequency array in the transmitted by IQ samples for pilots
    % and data
    iqTX( :, pilot_symbol_idx ) = iqTXref;
    
    for n = 1 : N_slots * N_symbols_per_slot
       if ~ismember( n, pilot_symbol_idx )
          % data symbol - generate random QAM data
          iqTX(:,n) = QAM4( randi([0,3], N_sc, 1) + 1 );
       end
    end

    % OFDM modulation
    sigTX = ofdma_mod_final( iqTX, N_fft, N_sc, N_symbols_per_slot, N_cp_1st, N_cp_other );
    
    % % % % % % % %
    % Channel
    
    % apply Rayleigh fading channel (multipath and mobility)
    % assume no time and frequency synchronization errors
    sigRX = rayleigh( sigTX );     % function from Comm Toolbox
    sigRX = awgn( sigRX, SNR );    % Matlab function
    
    % % % % % % % %
    % Receiver 
    
    % no time and frequency synchronization done (for simplicity)
    iqRX = ofdma_demod_final( sigRX, N_fft, N_sc, N_symbols_per_slot, N_cp_1st, N_cp_other );
    
    % Extract pilot subcarriers
    iqRXref = iqRX(:, pilot_symbol_idx);
    
    % Channel Estimation (Least Squares)
    H_est = iqRXref ./ iqTXref;
    
    % Interpolation of channel estimation in time and frequency
    X = repmat( reshape( pilot_symbol_idx, 1, [] ), [N_sc 1] );
    Y = repmat( reshape( 1:N_sc, [], 1), [1 length(pilot_symbol_idx)] );
    Xq = repmat(  1:size(iqRX,2),   [size(iqRX,1) 1] );
    Yq = repmat( (1:size(iqRX,1))', [1 size(iqRX,2)] );
    
    H_est_int = interp2( X, Y, H_est, Xq, Yq, 'spline');
    H_est_int_linear = interp2( X, Y, H_est, Xq, Yq, 'linear');
    H_est_int_nearest = interp2( X, Y, H_est, Xq, Yq, 'nearest');
    H_est_int_cubic = interp2( X, Y, H_est, Xq, Yq, 'cubic');

    % Equalization
    iqRX_eq_s = iqRX ./ H_est_int;
    iqRX_eq_l = iqRX ./ H_est_int_linear;
    iqRX_eq_n = iqRX ./ H_est_int_nearest;
    iqRX_eq_c = iqRX ./ H_est_int_cubic;

    % calculate and plot error averaged per symbol
    error_per_symbol_s = mean(abs(iqTX - iqRX_eq_s));
    error_per_symbol_l = mean(abs(iqTX - iqRX_eq_l));
    error_per_symbol_n = mean(abs(iqTX - iqRX_eq_n));
    error_per_symbol_c = mean(abs(iqTX - iqRX_eq_c));

    no_of_errors_shifts_s(i) = max(error_per_symbol_s);
    no_of_errors_shifts_l(i) = max(error_per_symbol_l);
    no_of_errors_shifts_n(i) = max(error_per_symbol_n);
    no_of_errors_shifts_c(i) = max(error_per_symbol_c);
end

figure(3)
subplot(2,1,1); 
plot(MaximumDopplerShifts,no_of_errors_shifts_s,'o-'); grid;
hold on;
plot(MaximumDopplerShifts,no_of_errors_shifts_l,'x-'); grid;
hold on;
plot(MaximumDopplerShifts,no_of_errors_shifts_n,'o--'); grid;
hold on;
plot(MaximumDopplerShifts,no_of_errors_shifts_c,'x--'); grid;
legend('spline','linear','nearest','cubic');
xlabel('MaximumDopplerShifts')
ylabel('Max no. of errors per symbol')
title('No. of Errors SCS Analysis Per Symbol');

subplot(2,1,2); 
plot(error_per_symbol_s,'o-'); grid;
hold on;
plot(error_per_symbol_l,'x-'); grid;
hold on;
plot(error_per_symbol_n,'o--'); grid;
hold on;
plot(error_per_symbol_c,'x--'); grid;
legend('spline','linear','nearest','cubic');
xlabel('Id of Symbol')
ylabel('Mean. no of errors per symbol')
title('No. of Errors Analysis Per Symbol');

%% CP Prefix length vs channel response analysis
for i = 1:length(CPs)

    % OFDM system parameters
    scs = 15e3;                % subcarrier spacing [Hz]
    N_fft = 256;               % FFT size
    N_sc = 132;                % number of subcarriers used for data transmissions
    N_cp_1st = CPs(i);             % cyclic prefix length of the first symbol in slot
    N_cp_other = CPs(i)-1;           % cyclic prefix length of the other symbol in slot
    N_symbols_per_slot = 14;   % number of symbols in slot
    F_s = scs * N_fft;         % sampling frequency
    
    % Initialize Rayleigh fading channel model object
    PathDelays = [0, 4, 10] / F_s;    % tap delays of multipath propagation channel
    AveragePathGains = [0, -4, -10];  % tap gains (in dB) of multipath propagation channel
    MaximumDopplerShift = 2500;        % maximum Doppler shift for the user (note Doppler shift maps to user velocity)
    rayleigh = comm.RayleighChannel('SampleRate', scs*N_fft, 'PathDelays', PathDelays, ...
              'AveragePathGains', AveragePathGains, 'MaximumDopplerShift', MaximumDopplerShift);
    
    % % % % % % % %
    % Transmitter 
    
    QAM4 = [ -1-1i; -1+1i; 1-1i; 1+1i ] / sqrt(2); % IQ states for QPSK modulation
 
    pilot_symbol_idx = 1 : (N_symbols_per_slot/2) : N_slots*N_symbols_per_slot;
    numTXref = randi( [0,3], N_sc, numel(pilot_symbol_idx) );  % REF pilot IQ
    iqTXref  = QAM4( numTXref+1 );                             % REF TX IQ freq states
    
    % fill the time-frequency array in the transmitted by IQ samples for pilots
    % and data
    iqTX( :, pilot_symbol_idx ) = iqTXref;
    
    for n = 1 : N_slots * N_symbols_per_slot
       if ~ismember( n, pilot_symbol_idx )
          % data symbol - generate random QAM data
          iqTX(:,n) = QAM4( randi([0,3], N_sc, 1) + 1 );
       end
    end

    % OFDM modulation
    sigTX = ofdma_mod_final( iqTX, N_fft, N_sc, N_symbols_per_slot, N_cp_1st, N_cp_other );
    
    % % % % % % % %
    % Channel
    
    % apply Rayleigh fading channel (multipath and mobility)
    % assume no time and frequency synchronization errors
    sigRX = rayleigh( sigTX );     % function from Comm Toolbox
    sigRX = awgn( sigRX, 250 );    % Matlab function
    
    % % % % % % % %
    % Receiver 
    
    % no time and frequency synchronization done (for simplicity)
    iqRX = ofdma_demod_final( sigRX, N_fft, N_sc, N_symbols_per_slot, N_cp_1st, N_cp_other );
    
    % Extract pilot subcarriers
    iqRXref = iqRX(:, pilot_symbol_idx);
    
    % Channel Estimation (Least Squares)
    H_est = iqRXref ./ iqTXref;
    
    % Interpolation of channel estimation in time and frequency
    X = repmat( reshape( pilot_symbol_idx, 1, [] ), [N_sc 1] );
    Y = repmat( reshape( 1:N_sc, [], 1), [1 length(pilot_symbol_idx)] );
    Xq = repmat(  1:size(iqRX,2),   [size(iqRX,1) 1] );
    Yq = repmat( (1:size(iqRX,1))', [1 size(iqRX,2)] );
    
    H_est_int = interp2( X, Y, H_est, Xq, Yq, 'spline');
    H_est_linear = interp2( X, Y, H_est, Xq, Yq, 'linear');
    H_est_nearest = interp2( X, Y, H_est, Xq, Yq, 'nearest');
    H_est_cubic = interp2( X, Y, H_est, Xq, Yq, 'cubic');

    % Equalization
    iqRX_eq_s = iqRX ./ H_est_int;
    iqRX_eq_l = iqRX ./ H_est_linear;
    iqRX_eq_n = iqRX ./ H_est_nearest;
    iqRX_eq_c = iqRX ./ H_est_cubic;

    % calculate and plot error averaged per symbol
    error_per_symbol_s = mean(abs(iqTX - iqRX_eq_s));
    error_per_symbol_l = mean(abs(iqTX - iqRX_eq_l));
    error_per_symbol_n = mean(abs(iqTX - iqRX_eq_n));
    error_per_symbol_c = mean(abs(iqTX - iqRX_eq_c));

    no_of_errors_s(i) = mean(error_per_symbol_s,'all');
    no_of_errors_l(i) = mean(error_per_symbol_l,'all');
    no_of_errors_n(i) = mean(error_per_symbol_n,'all');
    no_of_errors_c(i) = mean(error_per_symbol_c,'all');
end

figure(4)
plot(CPs,no_of_errors_s,'o-'); grid;
hold on;
plot(CPs,no_of_errors_l,'x-'); grid;
hold on;
plot(CPs,no_of_errors_n,'o--'); grid;
hold on;
plot(CPs,no_of_errors_c,'x--'); grid;
legend('spline','linear','nearest','cubic');
xlabel('CP length')
ylabel('Mean no. of errors per symbol')
title('No. of Errors CP Analysis Per Symbol');



