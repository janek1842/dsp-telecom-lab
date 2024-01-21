# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 19:59:49 2023

@author: janfi
"""
import numpy as np
import matplotlib.pyplot as plt

def my_stem_plot(y,title,y_range=None):
    x = np.arange(len(y))    
    plt.stem(x,y,markerfmt='s')

    plt.xticks(x)
    
    if y_range:
        plt.ylim(y_range)
        plt.yticks(np.arange(*y_range))
    
    plt.grid()
    plt.title(title)
    fig = plt.gcf()
    fig.set_size_inches(4, 3.6)
    plt.show()

def myDFT(samples):
    
    t = np.arange(0,2*np.pi,2*np.pi/len(samples))
    
    real = list()
    image = list()
    for f in range(len(samples)):
        real.append(np.dot(samples, np.cos(f * t)))
        image.append(-1 * np.dot(samples, np.sin(f * t)))
           
    return real,image