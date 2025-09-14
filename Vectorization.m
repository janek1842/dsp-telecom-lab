clear all; close all; clc;

%% Drawing the benefits of vectorization using the dot operation

idx=1;
for e = 10000:10000:100000

  % Generating test data
  for f = 1:e
    x(f) = randi(1000);
    y(f) = randi(1000);
  endfor

  dot_prod_iterative =0;

  % 1. Measuring the time of iterative approach
  tic;
  for f = 1:e
    dot_prod_iterative = dot_prod_iterative + (x(f) * y(f));
  endfor
  iterative_time(idx) = toc;

  % 2. Measuring the time of intermediate function
  tic;
  dot_inter = sum (conj (x) .* y);
  inter_time(idx) = toc;

  % 3. Measuring the time of matlab dot function
  tic;
  dot_prod_function = dot(x,y);
  func_time(idx) = toc;

  sizes(idx) = e;
  idx = idx +1;
endfor

figure(1)
plot(sizes,func_time, 'bo',sizes,iterative_time, 'ro', sizes,inter_time, 'go');
legend ('func','iterative','intermediate');
ylabel('Processing time [s]');
xlabel('Vector size');
title("Comparison of two different methods of generating the dot product");
