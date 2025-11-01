function [ iq, cfo ] = estim_correct_cfo(iq, N_fft, N_cp,jj)
% CFO estimation and correction

% estimate fractional CFO using only one OFDM symol (after its earlier synchronization)
  cfo = 1/(2*pi) * mean( angle(conj(iq( 1 : N_cp )) .*  iq( 1+N_fft : N_cp+N_fft)) );
  
  cfo = cfo + jj*cfo;

% correct fractional CFO in the whole input signal
  iq = iq .* exp( -1i * 2*pi*(0:numel(iq)-1)' * cfo / N_fft);

end
