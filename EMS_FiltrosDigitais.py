#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 12:27:29 2022

@author: carolinaazevedo
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sg

#############
#  NOTCH
#############
def notchFilter_func(noisySignal):
    
    print("NOTCH FILTER")

    samp_freq = 1000
    notch_freq = 50.0
    quality_factor = 80.0

    # Create the notch filter
    b_notch, a_notch = sg.iirnotch(notch_freq, quality_factor, samp_freq)
    #freq, h = sg.freqz(b_notch, a_notch, fs=2*np.pi)
    freq, h = sg.freqz(b_notch, a_notch, samp_freq)

    # plt.figure(1)
    # plt.subplot(1, 1, 1)
    # plt.plot(0.5 * samp_freq * freq / np.pi, np.abs(h), 'b')
    # plt.plot(notch_freq, 0.5 * np.sqrt(2), 'ko')
    # plt.axvline(notch_freq, color='r')
    # plt.xlim(0, 0.5 * samp_freq)
    # plt.title("Notch Filter Frequency Response")
    # plt.xlabel('Frequency [Hz]')
    # plt.grid()

    # Applying the filter to the signal
    outputSignal1 = sg.filtfilt(b_notch, a_notch, noisySignal)
    outputSignal2 = sg.filtfilt(b_notch, a_notch, outputSignal1)
    outputSignal3 = sg.filtfilt(b_notch, a_notch, outputSignal2)
    outputSignal4= sg.filtfilt(b_notch, a_notch, outputSignal3)
    outputSignal5= sg.filtfilt(b_notch, a_notch, outputSignal4)
    outputSignal6= sg.filtfilt(b_notch, a_notch, outputSignal5)

    return outputSignal6

##############
#   HIGH PASS
##############
def high_passFilter_func(signal):
    
    print("HIGH PASS FILTER")
    
    fs = 1000
    cutoff = 0.05

    order = 4
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq

    b_high, a_high = sg.butter(
        order, normal_cutoff, btype='high', analog=False)
    
    #freq, h = sg.freqz(b_high, a_high, fs=2*np.pi)
    freq, h = sg.freqz(b_high, a_high, fs)
    
    # plt.subplot(1, 1, 2)
    # plt.plot(0.5 * fs * freq / np.pi, np.abs(h), 'b')
    # plt.plot(cutoff, 0.5 * np.sqrt(2), 'ko')
    # plt.axvline(cutoff, color='r')
    # plt.xlim(0, 150)
    # plt.title("High Filter Frequency Response")
    # plt.xlabel('Frequency [Hz]')
    # plt.grid()

    outputSignal = sg.filtfilt(b_high, a_high, signal)

    return outputSignal

##############
#   LOW PASS
##############
def low_passFilter_func(data):
    
    print("LOW PASS FILTER ")
    
    order = 4
    fs = 1000
    nyq = 0.5 * fs  #Nyquist Frequency
    cutoff = 100
    normal_cutoff = cutoff / nyq
    
    # Get the filter coefficients 
    b_low, a_low  = sg.butter(order, normal_cutoff, btype='low', analog=False)
    
    freq, h = sg.freqz(b_low, a_low, fs)
    
    # plt.subplot(1, 1, 3)
    # plt.plot(0.5 * fs * freq / np.pi, np.abs(h), 'b')
    # plt.plot(cutoff, 0.5 * np.sqrt(2), 'ko')
    # plt.axvline(cutoff, color='r')
    # plt.xlim(0, 150)
    # plt.title("Low Filter Frequency Response")
    # plt.xlabel('Frequency [Hz]')
    # plt.grid()
    
    y = sg.filtfilt(b_low, a_low, data)
    
    return y