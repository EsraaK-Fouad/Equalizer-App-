# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.sliderArray = []
        self.pcArray = []
        self.gridArray = []
        MainWindow.setGeometry(300, 300, 800, 400)
        MainWindow.setWindowTitle("Graphical EQ")
        MainWindow.setWindowIcon(QtGui.QIcon(".icon//Icon.png"))
        self.FRAME_A = QtWidgets.QFrame()
        self.FRAME_A.setStyleSheet("QWidget { background-color: %s }" % QtGui.QColor(0, 0, 5, 5).name())
        self.mainhbox = QtWidgets.QVBoxLayout()
        self.FRAME_A.setLayout(self.mainhbox)
        MainWindow.setCentralWidget(self.FRAME_A)
        self.menubar =  QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(250, 250, 1205, 20))
        MainWindow.setMenuBar(self.menubar)
        self.fileMenu = self.menubar.addMenu('File')
        self.WindowsMenu = self.menubar.addMenu("Windows")
        self.viewMenu = self.menubar.addMenu("Popup window")

        self.Popupwindow = QtWidgets.QAction('difference ', MainWindow)
        self.Hamming = QtWidgets.QAction('Hamming ', MainWindow)
        self.Hanning = QtWidgets.QAction('Hanning ', MainWindow)
        self.Rect = QtWidgets.QAction('Rectangular ', MainWindow)
        self.OpenAction = QtWidgets.QAction('Open' ,MainWindow )
        
        self.viewMenu.addAction(self.Popupwindow)
        self.WindowsMenu.addAction(self.Hanning)
        self.WindowsMenu.addAction(self.Hamming )
        self.WindowsMenu.addAction(self.Rect)
        self.fileMenu.addAction(self.OpenAction)


        self.toolbar = QtWidgets.QToolBar(MainWindow)
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)

        self.playAction = QtWidgets.QAction(QtGui.QIcon(".img//fi.png"), 'play', MainWindow)
        self.stopAction = QtWidgets.QAction(QtGui.QIcon(".img//images.png"), 'stop', MainWindow)
        self.save = QtWidgets.QAction(QtGui.QIcon(".img//images.png"), 'save', MainWindow)


        self.toolbar.addAction(self.playAction)
        self.toolbar.addAction(self.stopAction)
        self.toolbar.addAction(self.save)

    
        self.grid()
        self.creategraphwidget()
        self.hbox = QtWidgets.QHBoxLayout()
        self.mainhbox.addLayout(self.hbox, 1)
        self.createslider()
      
  # ***************************************************Design*********************************************#
    def grid(self):
        global i
        i = 0
        while i < 2:
            self.grid = QtWidgets.QGridLayout()
            self.mainhbox.addLayout(self.grid, 1)
            self.gridArray.append(self.grid)
            i += 1

    # ***************************************************Graphwindow**********************************#
    def creategraphwidget(self):
        global i
        i = 0
        while i < 4:
            self.pw = pg.PlotWidget()
            self.pcArray.append(self.pw)
            if i <= 1:
                self.gridArray[0].addWidget(self.pcArray[i], *(0, i))
            else:
                self.gridArray[1].addWidget(self.pcArray[i], *(0, i - 2))

            i += 1

  # ********************************************Equalizer functions***************************************
    def createslider(self):
        global i
        i = 0
        while i < 10:
            self.slider =QtWidgets.QSlider(QtCore.Qt.Vertical)
            self.slider.setTickPosition(QtWidgets.QSlider.TicksRight)
            self.slider.setMinimum(-50)
            self.slider.setMaximum(50)
            self.slider.setValue(0)
            self.slider.setTickInterval(10)
            self.hbox.addWidget(self.slider)
            self.slider.setSingleStep(1)
            self.sliderArray.append(self.slider)
            i += 1





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

