# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------------------------------#
#
#-----------------------------------------------------------------------------------------------------------------------------------------------#
from PyQt4.QtGui import * 
from PyQt4.QtCore import * 
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

import theis as fm

class dibujante2(QMainWindow):

    def __init__(self, parent, cont):#Hay que pasarle la ventana que lo invoca

        QMainWindow.__init__(self, parent)
        self.fm = cont.dominio.metodo
        self.fm.calcular()

        #self.fm.calcularpozo(1,1,500)
        #self.fm.calcularpozo(10,0.2,10)


        self.main_frame = QWidget()
        self.setWindowTitle(u'Gráficas')

        self.canvas = FigureCanvas(self.fm.fig)
        self.canvas.setParent(self.main_frame)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        self.setCentralWidget(self.main_frame)
        self.fm.axt.mouse_init()

    def draw(self):

        self.canvas.draw()

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    fv = dibujante()
    fv.show()
    sys.exit(app.exec_())
