function [max_corr_index, r] = find_symbol_start(iq, N_FFT, N_CP_1st, N_CP_other)
% finding position of the strongest OFDM symbol with long prefix

  N_BLOCK = (N_CP_1st+N_FFT) + 13*(N_CP_other+N_FFT);   % length of 14 OFDM symbols
  N = min( length(iq), N_BLOCK );                       % number of tested samples 
  r = zeros(1,N);                                       % xcorr initialzation
  for n = 1 : (N-(N_FFT+N_CP_1st-1))                    % xcorr coefs calculation
      r(n) = corr( iq( n : n+N_CP_1st-1 ), iq(n+N_FFT : n+N_FFT+N_CP_1st-1 ) );
  end
  [ max_corr_value, max_corr_index ] = max( abs(r) );   % max(abs(xcorr))
  %figure; plot(abs(r)); grid; title('CP corr(n)');      % figure of xcorr
end
