function y = ofdmdemod_janka(sigTX, Nfft, Ncp)
    N_sym = numel(sigTX) / Nfft;
    Nsymb = Ncp + Nfft;      % OFDM symbol length
    y = [];

    for n_sym = 1 : N_sym

        sigRX = sigTX( (n_sym-1)*Nsymb+1 : (n_sym-1)*Nsymb+Nsymb, 1 );          % extracting the OFDM symbol         
        sigRX = sigRX( Ncp+1 : Ncp+1+(Nfft-1) );            % removing cyclic prefix
        iqRX  = fftshift(fft( sigRX ));                               % going to freq domain (demod)
        
        y(end+1:end+Nfft,1)= iqRX;
    end
end