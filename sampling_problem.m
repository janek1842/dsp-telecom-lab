clear all; close all;

% Problem 2.2
fs=1000; Nx=10*fs;
dt = 1/fs;
df = 200;
t = dt * (0:Nx-1);
A1=0.5; f1=1;p1=pi/4;
%x1 = A1*sin(2*pi*f1*t+p1);
x = cos(2*pi*(0*t+0.5*df*t.^2));

%% FIRST PART OF THE TASK

% SIGNAL IN TIME DOMAIN
figure(1);
title('fs=1000 Hz ; df=200');
plot(t,x,'o-'); grid; title('Signal x(t)'); xlabel('time [s]'); ylabel('Amplitude');
sound(x,fs);

% OBSERVATION
% The signal is exactly as we generate it until the 2.5s in a moment that
% we break the sampling theorem and starting to sample signal with lower
% freqeuncy as it is in reality. The signal frequency is decreasing until the moment of 5s when we consider it as it would have frequency = 0 Hz
% but in reality it has already reached 1000 Hz !!! Then it again increases
% and then again decreases until 0Hz. The same observation can be made as we listen to the signal. 

% SIGNAL IN FREQ/TIME DOMAIN
figure(2);
title('fs=1000 Hz ; df=200');
spectrogram(x,256,256-64,512,fs)

% EXPLENATION
% The signal is reaching half of the sampling frequency (8000/2) in 2.5s and then
% bad things start to happen, because we increase the frequency but on the spectrogram below (Figure 2), we can see 
% that it gradually decreases until the moment of 5 second, This is due to the so called alliasing, we are breaking the 
% sampling theorem sampling the signal too slow and therefore we consider the signal as it has frequency lower than it has in reality  

pause();
% Attention !
% click enter now in command window while executing the script !!! 

%% SECOND PART OF THE TASK
fs=8000; Nx=10*fs;
dt = 1/fs;
df = 2000;
t = dt * (0:Nx-1);
A1=0.5; f1=1;p1=pi/4;
%x1 = A1*sin(2*pi*f1*t+p1);
x = cos(2*pi*(0*t+0.5*df*t.^2));

% SIGNAL IN TIME DOMAIN
figure(3);
title('fs=8000 Hz ; df=2000');
plot(t,x,'o-'); grid; title('Signal x(t)'); xlabel('time [s]'); ylabel('Amplitude');
sound(x,fs);

% OBSERVATION
% Same as above

% SIGNAL IN FREQ/TIME DOMAIN
figure(4);
title('fs=8000 Hz ; df=2000');
spectrogram(x,256,256-64,512,fs)

% EXPLENATION
% Basically the same things happens here. We generate the signal. It's ok until the 2s. In this moment we start to sample
% the signal that has a higher frequency than 4000 Hz and therefore despite the signal frequency still goes up, in our spectrogram we can see that it goes
% down due to the alliasing. In 4s the signal frequency reaches 8000 Hz that is so high for our poor sampling frequency (8000 Hz) that we consider it as it would have 0Hz.
% The same situation happens periodically despite the signal frequency is
% higher and higher our sampling frequency remains constant all the time
% (8000 Hz) and therefore we are not able to capture the real frequency of
% the signal


