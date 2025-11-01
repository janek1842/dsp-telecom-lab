%[fd] = ofdma_demod_final(td, N_fft, N_sc, N_symbols_per_slot, N_cp_1st, N_cp_other)
%
% Demodulate OFDM modulated data vector td using specified FFT 
% size and cyclic prefix configuration. Data vector start
% must be aligned to slot start.
% 
% Arguments:
%  td        - time domain data
%  N_fft     - FFT size
%  N_sc      - number of subcarriers allocated for transmission
%  N_symbols_per_slot - number of symbols in a slot
%  N_cp_1st   - cyclic prefix length of the first symbol in a slot
%  N_cp_other - cyclic prefix length of the other symbol in a slot
%
% Returns:
%  fd    - frequency domain carrier data

function [fd] = ofdma_demod(td, N_fft, N_sc, N_symbols_per_slot, N_cp_1st, N_cp_other)
  guards = (N_fft - N_sc) / 2;

  fd = [];
  idx = 1;
  n_sym = 1;
  N_cp = N_cp_1st;

  while idx + N_fft + N_cp - 1 <= length(td)
    tdrs = td(idx+N_cp : idx+N_cp+N_fft-1);
    tdrs(end+1:end) = td(idx+N_cp:idx+N_cp-1);

    fds = fftshift(fft(tdrs)) / sqrt(N_fft);

    fd(:,n_sym) = fds(guards+1:guards+N_sc);

    idx = idx + N_fft + N_cp;
    n_sym = n_sym + 1;

    if mod(n_sym, N_symbols_per_slot) == 1
      N_cp = N_cp_1st;
    else
      N_cp = N_cp_other;
    end
  end
end