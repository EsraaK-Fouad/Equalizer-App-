# ****************************************Libraries*****************************************************************#
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import wave
from pylab import *
import librosa
import numpy as np
import pyqtgraph as pg
import sounddevice as sd
from numpy.fft import fft, fftfreq
from pyqtgraph import PlotWidget, plot
from scipy import signal
from scipy.io import wavfile
from scipy.signal import butter, lfilter
from PyQt5 import QtCore, QtGui, QtWidgets
from UI import Ui_MainWindow

# **********************************************************code implemented****************************************#
class MainWindowUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        global fs, data , gainArray
        self.flag = 2
        self.UI=Ui_MainWindow()
        self.UI.setupUi(self)
        self.UI.Popupwindow.triggered.connect(self.newwindowfunc)
        self.UI.Hanning.triggered.connect(self.Hanningfunc)
        self.UI.Rect.triggered.connect(self.Rectfunc)
        self.UI.Hamming.triggered.connect(self.Hammingfunc)
        self.UI.OpenAction.triggered.connect(self.OpenFile)
        self.UI.playAction.triggered.connect(self.Play)
        self.UI.stopAction.triggered.connect(self.stop)
        self.UI.save.triggered.connect(self.savefunc)
        self.loopslider()

    # *******************************************************functions of menuebar***************************
    def OpenFile(self):
        self.filepath = QtWidgets.QFileDialog.getOpenFileName()
        self.path = self.filepath[0]
    # =======================================================================================================
    def savefunc(self):
        array=self.changeslidervalue()
        audio = self.audioRun(self.flag,*array)
        m = np.max(np.abs(audio))
        sig = (audio / m).astype(np.float32)
        name="audiofile{}.wav"
        name=name.format(self.flag)
        save = wavfile.write(name, int(fs), sig)
        subplot(211)
        plot(audio)
        
    # =======================================================================================
    def newwindowfunc(self):
        array=self.changeslidervalue()
        self.SW = SecondWindow(data, fs,self.flag,*array)
        self.SW.show()
 
    # =============================================================
    def stop(self):
        sd.stop()
   
    #==============================================================
    def Play(self):
        global fs, data
        data, fs = librosa.load(self.path, sr=None, duration=20.0)
        print(data)
        print(fs)
        self.datafft = fft(data)
        self.fftabs = abs(self.datafft)
        self.freqs = fftfreq(len(self.fftabs), 1 / fs)
        self.N = len(self.fftabs)
        self.T = int(self.N / fs)
        print(self.T)
        self.t = 1 / fs * np.arange(self.N)
        self.UI.pcArray[1].plot(self.freqs[:int(self.freqs.size / 2)], self.fftabs[:int(self.freqs.size / 2)], pen='b')
        self.UI.pcArray[0].plot(data[:self.T * fs], pen='b')
        self.changeslidervalue()
     #================================================================
    def Hanningfunc(self):
        global i  
        i=0
        while i<4 :
            self.UI.pcArray[i].clear()
            i+=1
        self.flag = 2
        self.Play()
    
    #===================================================================================
    def Hammingfunc(self):
        global i
        i=0
        while i<4 :
            self.UI.pcArray[i].clear()
            i+=1
        self.flag = 0
        self.Play()
     
    # ==============================================================
    def Rectfunc(self):
        global i
        i=0
        while i<4 :
            self.UI.pcArray[i].clear()
            i+=1
        self.flag = 1
        self.Play()
    

    # ===========================================================================
    def loopslider(self):
        global i
        i = 0
        while i < 10:
            self.UI.sliderArray[i].valueChanged.connect(self.changeslidervalue)
            i += 1

    # ============================================================================
    def bandpass_filter(self, datanyquistfreq, lowcut, highcut, fs, order=5):
        nyquistfreq = 0.5 * fs
        low = lowcut / nyquistfreq
        high = highcut / nyquistfreq
        b, a = butter(order, [low, high], btype='band', analog=False)
        filtered = lfilter(b, a, data)
        return filtered

    def hammingprocessing(self, data, begin, end,fs,order):
        band = self.bandpass_filter(data, begin, end, fs, order=order)
        bandsize = len(band)
        rand = data[:int(bandsize / 2)]
        window = signal.windows.hamming(int(2 * bandsize))
        banda = np.concatenate((rand, band, rand), axis=0) * window
        bandafterwindowing = banda[int(bandsize / 2):int(3 * bandsize/2 )]
        return bandafterwindowing

    def processHammingAudio(self, data, fs, gain1, gain2, gain3, gain4, gain5, gain6, gain7, gain8, gain9, gain10):
        freq = np.arange(fs * 0.5)
        size = len(freq) / 10
        band1 = self.hammingprocessing(data, freq[21], freq[int(size)], fs,4) * 10 ** (gain1 / 20)
        band2 = self.hammingprocessing(data, freq[int(size)], freq[2 * int(size)], fs,4) * 10 ** (gain2 / 20)
        band3 = self.hammingprocessing(data, freq[2 * int(size)], freq[3 * int(size)], fs, 4) * 10 ** (gain3 / 20)
        band4 = self.hammingprocessing(data, freq[3 * int(size)], freq[4 * int(size)], fs, 4) * 10 ** (gain4 / 20)
        band5 = self.hammingprocessing(data, freq[4 * int(size)], freq[5 * int(size)], fs,4) * 10 ** (gain5 / 20)
        band6 = self.hammingprocessing(data, freq[5 * int(size)], freq[6 * int(size)], fs, 4) * 10 ** (gain6 / 20)
        band7 = self.hammingprocessing(data, freq[6 * int(size)], freq[7 * int(size)], fs, 4) * 10 ** (gain7 / 20)
        band8 = self.hammingprocessing(data, freq[7 * int(size)], freq[8 * int(size)], fs, 4) * 10 ** (gain8 / 20)
        band9 = self.hammingprocessing(data, freq[8 * int(size)], freq[9 * int(size)], fs, 4) * 10 ** (gain9 / 20)
        band10 = self.hammingprocessing(data, freq[9 * int(size)], freq[-1], fs, order=3) * 10 ** (gain10 / 20)
        Hsignal = band1 + band2 + band3 + band4 + band5 + band6 + band7 + band8 + band9 + band10
        return Hsignal
    
    def hanningprocessing(self, data, begin, end,fs,order):
        band = self.bandpass_filter(data, begin, end, fs, order=order)
        bandsize = len(band)
        rand = data[:int(bandsize / 2)]
        window = signal.windows.hann(int(2 * bandsize))
        banda = np.concatenate((rand, band, rand), axis=0) * window
        bandafterwindowing = banda[int(bandsize / 2):int(3 * bandsize/2 )]
        return bandafterwindowing

    def processHanningAudio(self, data, fs, gain1, gain2, gain3, gain4, gain5, gain6, gain7, gain8, gain9, gain10):
        freq = np.arange(fs * 0.5)
        size = len(freq) / 10
        band1 = self.hanningprocessing(data, freq[21], freq[int(size)], fs,4) * 10 ** (gain1 / 20)
        band2 = self.hanningprocessing(data, freq[int(size)], freq[2 * int(size)], fs,4) * 10 ** (gain2 / 20)
        band3 = self.hanningprocessing(data, freq[2 * int(size)], freq[3 * int(size)], fs, 4) * 10 ** (gain3 / 20)
        band4 = self.hanningprocessing(data, freq[3 * int(size)], freq[4 * int(size)], fs, 4) * 10 ** (gain4 / 20)
        band5 = self.hanningprocessing(data, freq[4 * int(size)], freq[5 * int(size)], fs,4) * 10 ** (gain5 / 20)
        band6 = self.hanningprocessing(data, freq[5 * int(size)], freq[6 * int(size)], fs, 4) * 10 ** (gain6 / 20)
        band7 = self.hanningprocessing(data, freq[6 * int(size)], freq[7 * int(size)], fs, 4) * 10 ** (gain7 / 20)
        band8 = self.hanningprocessing(data, freq[7 * int(size)], freq[8 * int(size)], fs, 4) * 10 ** (gain8 / 20)
        band9 = self.hanningprocessing(data, freq[8 * int(size)], freq[9 * int(size)], fs, 4) * 10 ** (gain9 / 20)
        band10 = self.hanningprocessing(data, freq[9 * int(size)], freq[-1], fs, order=3) * 10 ** (gain10 / 20)
        Hsignal = band1 + band2 + band3 + band4 + band5 + band6 + band7 + band8 + band9 + band10
        return Hsignal




    def processAudio(self, data, fs, gain1, gain2, gain3, gain4, gain5, gain6, gain7, gain8, gain9, gain10):
        freq = np.arange(fs * 0.5)
        size = len(freq) / 10
        band1 = self.bandpass_filter(data, freq[21], freq[int(size)], fs, order=4) * 10 ** (gain1 / 20)
        band2 = self.bandpass_filter(data, freq[int(size)], freq[2 * int(size)], fs, order=4) * 10 ** (gain2 / 20)
        band3 = self.bandpass_filter(data, freq[2 * int(size)], freq[3 * int(size)], fs, order=4) * 10 ** (gain3 / 20)
        band4 = self.bandpass_filter(data, freq[3 * int(size)], freq[4 * int(size)], fs, order=4) * 10 ** (gain4 / 20)
        band5 = self.bandpass_filter(data, freq[4 * int(size)], freq[5 * int(size)], fs, order=4) * 10 ** (gain5 / 20)
        band6 = self.bandpass_filter(data, freq[5 * int(size)], freq[6 * int(size)], fs, order=4) * 10 ** (gain6 / 20)
        band7 = self.bandpass_filter(data, freq[6 * int(size)], freq[7 * int(size)], fs, order=4) * 10 ** (gain7 / 20)
        band8 = self.bandpass_filter(data, freq[7 * int(size)], freq[8 * int(size)], fs, order=4) * 10 ** (gain8 / 20)
        band9 = self.bandpass_filter(data, freq[8 * int(size)], freq[9 * int(size)], fs, order=4) * 10 ** (gain9 / 20)
        band10 = self.bandpass_filter(data, freq[9 * int(size)], freq[-1], fs, order=3) * 10 ** (gain10 / 20)
        osignal = band1 + band2 + band3 + band4 + band5 + band6 + band7 + band8 + band9 + band10
        return osignal
#====================================================================================================
    def audioRun(self, flag, *gainArray):
        if (flag==0):
            Hs = self.processHammingAudio(data, fs,*gainArray)
            self.plot(Hs, fs)
            return Hs 
        elif (flag == 1 ):
            Rs = self.processAudio(data, fs, *gainArray)
            self.plot(Rs,fs)
            return Rs
        else:
            hs=self.processHanningAudio(data, fs,*gainArray)
            self.plot(hs, fs)
            return hs 
#=====================================================================================
    def plot(self,signal, sample_rate):
        global i
        i=2
        while i<4 :
            self.UI.pcArray[i].clear()
            i+=1          
        datafftafter = fft(signal)
        fftabsafter = abs(datafftafter)
        freqsa = fftfreq(len(datafftafter), 1 / sample_rate)
        self.UI.pcArray[3].plot(freqsa[:int(freqsa.size / 2)], fftabsafter[:int(freqsa.size / 2)], pen='r')
        N1 = len(signal)
        T1 = int(N1 / sample_rate)
        self.UI.pcArray[2].plot(signal[:T1 * sample_rate], pen='r')
        sd.play(signal, sample_rate)
     
# ====================================================================================================
    def changeslidervalue(self):
        global i
        i = 0
        gainArray = []
        while i < 10:
            gainArray.append(self.UI.sliderArray[i].value())
            i += 1
        print(gainArray)
        self.audioRun(self.flag,*gainArray)
        return gainArray
       
       

# ====================================================Pop up window ===================================================================
class SecondWindow(QtWidgets.QMainWindow):
    def __init__(self, data, fs,flag,*array):
        super(SecondWindow, self).__init__()
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle("Difference")
        self.FRAME_A = QtWidgets.QFrame(self)
        self.FRAME_A.setStyleSheet("QWidget { background-color: %s }" % QtGui.QColor(210, 210, 235, 255).name())
        self.LAYOUT_A = QtWidgets.QGridLayout()
        self.FRAME_A.setLayout(self.LAYOUT_A)
        self.setCentralWidget(self.FRAME_A)

        self.pw = pg.PlotWidget()
        self.pc = pg.PlotDataItem()
        self.pw.addItem(self.pc)
        self.LAYOUT_A.addWidget(self.pw, *(0, 0))
        N = len(data)
        t = 1 / fs * np.arange(N)
        f = fs / N * np.arange(N)
        self.x =  MainWindowUI()
        equalized = self.x.audioRun(flag,*array)
        print (equalized)
        datafft = fft(equalized)
        datafft2 = fft(data)
        diff = datafft - datafft2
        fftabs = abs(diff)
        freqs = fftfreq(len(diff), 1 / fs)
        self.pw.plot(freqs[:int(freqs.size / 2)], fftabs[:int(freqs.size / 2)])
        self.pw.show()

# ========================================Execute code===============================================================================
def main():
	app = QtWidgets.QApplication(sys.argv)
	application =MainWindowUI()
	application .show()
	app.exec_()


if __name__ == '__main__':
	main()



