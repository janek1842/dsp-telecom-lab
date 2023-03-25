clear all; close all; clc;

pskModulator = comm.PSKModulator;

modData = pskModulator(randi([0 7],2000,1));

channel = comm.AWGNChannel('EbNo',20,'BitsPerSymbol',5);

channelOutput = channel(modData);

scatterplot(modData)

scatterplot(channelOutput)

channel.EbNo = 10;

channelOutput = channel(modData);

scatterplot(channelOutput)