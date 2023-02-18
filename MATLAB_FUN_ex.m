clear all; close all; clc;


e = input('Wybierz rodzaj badanej funkcji 1-liniowa 2-kwadratowa ');


if (e == 1)
    %% Argument oraz przeciwdziedzina
    a = input ('Wprowadz wartosc wspolczynnika kierunkowego a ');
    b = input ('Wprowadz wartosc wyrazu wolnego b ');
    c = input ('Wprowadz zakres dolny ');
    d = input ('Wprowadz zakres gorny ');
    
    j = 1; 
    for i = c:d
        x(j) = i;
        y(j) = a * x(j) + b;
        j = j + 1;
    end
    
    %% Wykreslanie funkcji liniowej
    figure(1)
    plot(x,y);
    title('Funkcja liniowa');
    xlabel('x');
    ylabel('y (x)');
    % xlim ([c d]);
    grid on;
    
elseif (e == 2)
    %% Argument oraz przeciwdziedzina
    a = input ('Wprowadz wartosc wspolczynnika  a ');
    b = input ('Wprowadz wartosc wspolczynnika  b ');
    e = input ('Wprowadz wartosc wspolczynnika  c ');

    c = input ('Wprowadz zakres dolny ');
    d = input ('Wprowadz zakres gorny ');
    
    j = 1; 
    i = c;
    while(i<d)
        x(j) = i;
        y(j) = a * x(j) * x(j) + b*x(j) + e;
        j = j + 1;
        i = i + 0.1;
    end
    
    %% Wykreslanie funkcji liniowej
    figure(1)
    plot(x,y);
    title('Funkcja kwadratowa');
    xlabel('x');
    ylabel('y (x)');
    % xlim ([c d]);
    grid on;
end








