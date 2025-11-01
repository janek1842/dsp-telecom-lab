function rx_td = disturbances( tx_td, Nfft )
% Wplyw kanalu, zaklocenia, bledy sprzetu
% Usuwaj znaki komentarza, zmieniaj wartosci parametrow

% 1) idealny - ta opcja powinna byc zawsze wlaczona
     rx_td = tx_td; Nrx = length(rx_td);
% 2) dodanie szumu (kanal AWGN)
%    if( 1 ) % opcja #1
%        rx_td = awgn( rx_td, SNR, 'measured' );
%    else    % opca #2
%        s = rx_td; scale = sqrt( sum(s.*conj(s)) / (2*length(s)*10^(SNR/10)) ); clear s
%        rx_td = rx_td + scale * (randn(1,Nrx)+j*randn(1,Nrx));
%    end
% 3) tylko tlumienie i przesuniecie fazowe (kanal plaski)
%    G = 0.98*exp( -j*pi/21 ); rx_td = G * rx_td;
% 4) splot z odpowiedzia impulsowa kanalu (kanal z odbiciami - zanikami selektywnymi)
%    rx_td = conv( rx_td, [0.99*exp(-j*pi/9), 0, 0, 0.88*exp(-j*pi/8)], 'same' )
% 5) opcjonalne opoznienie o D=1,2,3,... probek
%    D=1; rx_td = [ rx_td(end-D+1:end); rx_td(1:end-D) ];
% 6) opcjonalne opoznienie o ulamek okresu probkowania: dD = 0.01, 0.1, 0.25, 0.5
%    (niezsynchronizowane przetworniki ADC w nadajniku i odbiorniku)
%    dD = 0.1;
%    if( dD ~= 0)
%       rx_td = interp1( [0:1:Nrx-1]', rx_td(1:Nrx), [0-dD:1:Nrx-1-dD]','spline');
%    end
% 7) offset czestotliwosci nosnej o df hercow: a) blad konwerterów UP/DOWN czestotliwosci,
%   b) blad czestotliwosci probkowania przetwornikow, zalezacy od ich jakosci (wartosc PPM)
%  df=1000; fs=3.84e+6; dt=1/fs; rx_td = rx_td .* exp( j*2*pi*df * dt*(0:Nrx-1)' ); 

% 8) efekt Dopplera, czyli suma opoznionych i przesunietych w czestotliwosci kopii sygnalu
%    C = [ 0.77*exp(+j*66/180*pi), 0.55*exp(j*44/180*pi), 0.33*exp(j*22/180*pi) ]; % wsp. odbicia
%    D  = [ 1,    3,    5    ];     % opoznienie w probkach (okresach probkowania)
%    dD = [ 0.54, 0.43, 0.34 ];     % opoznienie w ulamkach okresu probkowania
%    V  = [ 1,    3,    5    ];     % przesuniecie w czestotliwosci w prazkach DFT
%    dV = [ 0.54, 0.43, 0.34 ];     % przesuniecie w czestotliwosci w ulamkach prazkow DFT
%    Kpaths = 1;                            % przyjeta liczba odbic (z powyzej zdefinowanych)
%    x = tx_td; y = zeros(Nrx,1);           % inicjalizacja
%    for k = 1 : Kpaths                     % PETLA #######################
%        yk = circshift( x, D(k) );         % integer time shift
%        if( dD(k) ~= 0)                    % fractional time shift
%            yk = interp1( [0:1:Nrx-1]', yk(1:Nrx), [0-dD(k) : 1 : Nrx-1-dD(k)]','spline');
%        end                                % Doppler shift, integer and fractional
%        yk = C(k) * yk .* exp( j*2*pi/Nfft *(V(k)+dV(k)) *(0-(D(k)+dD(k)) : Nrx-1-(D(k)+dD(k))) ).';
%        y = y + yk;                        % akumulacja wyniku
%    end                                    % KONIEC PETLI ################
%    rx_td = y;                     % koncowe podstawienie
    
end
