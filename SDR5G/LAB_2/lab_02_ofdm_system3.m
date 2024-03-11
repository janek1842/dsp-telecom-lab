% lab_02_ofdm_system3.m - przyklad modelu transmisji OFDM z uzyciem Telecomm Toolbox
clear all; clc;

% parametry konfiguracyjne
Q_m = 64;      % 64-QAM, nie zmieniac!
SNR = 20000;      % SNR w jednostkach dB
N_FFT = 256;   % rozmiar FFT
N_CP =  18;    % dlugosc cyklicznego prefiksu: 22 (1st), 18 (other) 
SCRAMBLING_ENABLED = true;

% zakoduj wiadomosc uzywajac 64 znakow ASCII z zakresu od 32 do 95,
% czyli tylko duze litery plus czesc dodatkowych znakow alfanumerycznych
tx_message = uint8('LITWO, OJCZYZNO MOJA! TY JESTES JAK ZDROWIE; ILE CIE TRZEBA CENIC, TEN TYLKO SIE DOWIE, KTO CIE STRACIL. DZIS PIEKNOSC TWA W CALEJ OZDOBIE WIDZE I OPISUJE, BO TESKNIE PO TOBIE. LOREM IPSUM IS SIMPLY DUMMY TEXT OF THE PRINTING AND TYPESETTING INDUSTRY. LOREM IPSUM HAS BEEN THE INDUSTRY STANDARD DUMMY TEXT EVER SINCE THE 1500S, WHEN AN UNKNOWN PRINTER TOOK A GALLEY OF TYPE AND SCRAMBLED IT TO MAKE A TYPE SPECIMEN BOOK. IT HAS SURVIVED NOT ONLY FIVE CENTURIES, BUT ALSO THE LEAP INTO ELECTRONIC TYPESETTING, REMAINING ESSENTIALLY UNCHANGED. IT WAS POPULARISED IN THE 1960S WITH THE RELEASE OF LETRASET SHEETS CONTAINING LOREM IPSUM PASSAGES.');
tx_bits = tx_message - 32;

% dodaj zera na koncu wiadomosci tak aby dopelnic wektor do wielokrotnosci rozmiaru FFT
tx_bits( end+1 : end+ceil(numel(tx_message)/N_FFT )*N_FFT - numel(tx_message) ) = 0;

% skrambling (oryginalne liczby [0-63] XOR losowe liczby [0-63] )
scramble_sequence = uint8( randi( Q_m-1, size(tx_bits) ) );

if SCRAMBLING_ENABLED
    tx_bits_scrambled = bitxor( tx_bits, scramble_sequence );
else
    tx_bits_scrambled = tx_bits; % switching off scrambling and descrambling
end

% modulacja QAM (bity do zespolonych punktow konstelacji IQ)
tx_iq = qammod( tx_bits_scrambled, Q_m );

% wykres konstelacji nadajnika
subplot(1,2,1); plot(tx_iq, 'x'); title('TX IQ')

% modulacja OFDM
tx_td  = ofdmmod( reshape(tx_iq, N_FFT, []), N_FFT, N_CP );

% KANAL, ZAKLOCENIA I INTERFERENCJE, BLEDY SPRZETU
rx_td = disturbances( tx_td, N_FFT );

% demodulacja OFDM
% ---ZASTAP WLASNA IMPLEMENTACJA---
%rx_iq = ofdmdemod(rx_td, N_FFT, N_CP);
rx_iq=ofdmdemod_janka(rx_td, N_FFT, N_CP);

rx_iq = reshape(rx_iq, 1, []);

% wykres konstelacji odbiornika
subplot(1,2,2); plot(rx_iq, 'x'); title('RX IQ')

% demodulacja (punkty konstelacji do bitow)
rx_bits = qamdemod(rx_iq, Q_m);

% de-skrambling
if SCRAMBLING_ENABLED
    rx_bits_descrambled = bitxor(uint8(rx_bits), scramble_sequence);
else
    rx_bits_descrambled = rx_bits;
end

rx_message = char(uint8(rx_bits_descrambled)) + 32;
fprintf('\nReceived message:\n%s\n\n', rx_message);

numDifferences = 0;
            
for i = 1:length(tx_message)
    if tx_message(1,i) ~= rx_message(1,i)
        numDifferences = numDifferences + 1; % Increment the counter for differences
    end
end
fprintf('ERROR_NUMBER %d \n', numDifferences);
