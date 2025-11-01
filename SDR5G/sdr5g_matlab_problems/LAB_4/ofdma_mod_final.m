%[td] = ofdma_mod_final(fd, N_fft, N_sc, N_symbols_per_slot, cp_first, cp_other)
%
% Apply OFDM modulation to input frequency domain data vector
% fd using specified FFT size. Number of subcarriers and 
% guardbands is derived form FFT size.
% 
% Arguments:
%  fd        - frequency domain modulation data
%  N_fft     - FFT size
%  N_sc      - number of subcarriers allocated for transmission
%  N_symbols_per_slot - number of symbols in a slot
%  N_cp_1st   - cyclic prefix length of the first symbol in a slot
%  N_cp_other - cyclic prefix length of the other symbol in a slot
%
% Returns:
%  td    - time domain samples

function td = ofdma_mod(fd, N_fft, N_sc, N_symbols_per_slot, N_cp_1st, N_cp_other)
  assert(mod(numel(fd), N_sc) == 0, 'number of elements in fd must be a multiple of subcarriers for specified N_fft');

  if (mod(numel(fd), N_sc) ~= 0)
    warning('input data vector length is not a multiple of symbol size (N_sc)');
  end

  N_sym = numel(fd) / N_sc;
  guards = (N_fft - N_sc) / 2;

  fd = reshape(fd, N_sc, []);

  td = [];

  for n_sym = 1 : N_sym
    tds = ifft(ifftshift([zeros(guards,1); fd(:,n_sym); zeros(guards,1)])) * sqrt(N_fft);

    if mod(n_sym-1, N_symbols_per_slot) == 0
      N_cp = N_cp_1st;
    else
      N_cp = N_cp_other;
    end

    % add cyclic prefix and insert data
    td(end+1:end+N_cp,1) = tds(end-N_cp+1:end);
    td(end+1:end+N_fft,1)= tds;
  end
end