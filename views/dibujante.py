# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------------------------------#
#Esto va a dibujar las gráficas y controlar el tema de la animación
#-----------------------------------------------------------------------------------------------------------------------------------------------#
from PyQt4.QtGui import * #Para la interfáz gráfica
from PyQt4.QtCore import * #Para la interfáz gráfica
from PyQt4 import QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas #Clase para dibujar las gráficas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar #Clase para dibujar la barra de herramientas de navegación
import threading
import random

from models.figura import figura as fm

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class dibujante(QMainWindow):

    def __init__(self, parent = None, matrix = None, dominio=None):#Hay que pasarle la ventana que lo invoca

        QMainWindow.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.fm = fm(matrix, dominio)
        ran = random.randint(1, 10)
        self.fm.plotU(ran)
        self.fm.plotD(ran, 0)
        self.fm.plotT(ran, 0)
        self.fm.plotC(ran, 0)
        self.main_frame = QWidget()
        self.setWindowTitle(u'Gráficas')
        self.setMaximumSize(self.fm.fig.get_figwidth() * self.fm.fig.get_dpi(), self.fm.fig.get_figheight() * self.fm.fig.get_dpi() + 43)
        self.setMinimumSize(self.fm.fig.get_figwidth() * self.fm.fig.get_dpi(), self.fm.fig.get_figheight() * self.fm.fig.get_dpi() + 43)
        print 'Figure: width: ' + str(self.fm.fig.get_figwidth() * self.fm.fig.get_dpi()) + ', height: ' +str(self.fm.fig.get_figheight() * self.fm.fig.get_dpi()) + ', dpi: ' + str(self.fm.fig.get_dpi())
        self.center()
        self.canvas = FigureCanvas(self.fm.fig)
        self.canvas.setParent(self.main_frame)
        #self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        separador = QFrame()
        separador.setFrameShadow(QFrame.Sunken)
        separador.setFrameShape(QFrame.HLine)
        separador.setLineWidth(576)

        reproducirb = QPushButton()
        reproducirb.setMinimumSize(32, 32)
        reproducirb.setMaximumSize(32, 32)
        reproducirb.setIcon(QIcon('content/images/reproducir.png'))
        self.reproducirb = reproducirb
        QtCore.QObject.connect(self.reproducirb, QtCore.SIGNAL(_fromUtf8('released()')), self.reproducir)

        guardarb = QPushButton()
        guardarb.setMinimumSize(32, 32)
        guardarb.setMaximumSize(32, 32)
        guardarb.setIcon(QIcon('content/images/guardar.png'))
        self.guardarb = guardarb
        QtCore.QObject.connect(self.guardarb, QtCore.SIGNAL(_fromUtf8('released()')), self.guardar)

        estadob = QSlider(Qt.Horizontal)
        estadob.setMinimumSize(440, 32)
        estadob.setToolTip(u'Próximamente: mostrará el avance de la animación.')

        ##cambie el tmp
        ####se grafica el tiempo 1 
        tmp = self.fm.matrix[1]
        #Habia un tmp -1
        #estadob.setMaximum(tmp[-1])
        estadob.setMaximum(20)
        self.estadob = estadob
        QtCore.QObject.connect(self.estadob, QtCore.SIGNAL(_fromUtf8('sliderReleased()')), self.actualizarSlider)
        QtCore.QObject.connect(self.estadob, QtCore.SIGNAL(_fromUtf8('sliderMoved()')), self.actualizarSlider)
        QtCore.QObject.connect(self.estadob, QtCore.SIGNAL(_fromUtf8('valueChanged(int)')), self.actualizarSlider)

        timlab = QLabel(QString('0/' + str(self.estadob.maximum())))
        #timlab=QLabel(QString('pepe'))
        self.timlab = timlab

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addWidget(separador)
        hbox = QHBoxLayout()
        hbox.addWidget(reproducirb)
        hbox.addWidget(guardarb)
        hbox.addWidget(estadob)
        hbox.addWidget(timlab)
        vbox.addLayout(hbox)
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.reproducirBucle)

    def draw(self):

        self.canvas.draw()
        self.fm.axt.mouse_init()

    def actualizarSlider(self):

        self.estadob.setToolTip(str(self.estadob.value()) + '/' + str(self.estadob.maximum()))
        self.timlab.setText(self.estadob.toolTip())
        print u'Posición: segundo ' + str(self.estadob.value())

    def reproducir(self):

        if self.timer.isActive() == True:

            #Si ya está reproducioendo, entonces pausamos.
            self.timer.stop()
            self.reproducirb.setIcon(QIcon('content/images/reproducir.png'))
            print u'Próximamente: pausar de las gráficas.'

        else:

            self.timer.start()
            self.reproducirb.setIcon(QIcon('content/images/pausar.png'))
            print u'Próximamente: reproducción de las gráficas.'

    def reproducirBucle(self):

        if self.estadob.value() == self.estadob.maximum():

            self.reproducir()
            self.estadob.setValue(0)

        else:

            ran = random.randint(1, 10)
            self.fm.plotD(ran, self.estadob.value()+1)
            self.fm.plotT(ran, self.estadob.value()+1)
            self.fm.plotC(ran, self.estadob.value()+1)
            self.draw()
            self.estadob.setValue(self.estadob.value() + 1)

    def pausar(self):

        t.stop()
        print u'Próximamente: pausa de la animación de las gráficas.'

    def guardar(self):

        print u'Próximamente: guardará la animación de las gráficas en un video.'

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    fv = dibujante()
    fv.show()
    sys.exit(app.exec_())
