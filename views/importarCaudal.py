# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogo.ui'
#
# Created: Thu Dec 08 19:14:05 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import bombeo
import ensayobombeo
import sys
import zipfile
import xml.dom.minidom

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(QtGui.QDialog):
    def setupUi(self, Dialog, cont):
        ##Se recupera el controlador instanciado en el main
        ##Se usa ContEnsayo(el mismo nombre) para no marear
        ##el nombre del parametro tiene que ser otro sino salta la 3 al ser global y local
        global ContEnsayo
        ContEnsayo=cont
        self.archivo=""
        
        Dialog.setObjectName(_fromUtf8("ImportarCaudalBombeado"))
        Dialog.resize(572, 130)
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Importar Caudal Bombeado", None, QtGui.QApplication.UnicodeUTF8))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 30, 46, 13))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Archivito", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.textEdit = QtGui.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(113, 20, 331, 31))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(460, 20, 75, 23))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Explorar", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.aceptar = QtGui.QPushButton(Dialog)
        self.aceptar.setGeometry(QtCore.QRect(200, 70, 75, 23))
        self.aceptar.setText(QtGui.QApplication.translate("Dialog", "Aceptar", None, QtGui.QApplication.UnicodeUTF8))
        self.aceptar.setObjectName(_fromUtf8("aceptar"))
        self.cancelar = QtGui.QPushButton(Dialog)
        self.cancelar.setGeometry(QtCore.QRect(290, 70, 75, 23))
        self.cancelar.setText(QtGui.QApplication.translate("Dialog", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelar.setObjectName(_fromUtf8("cancelar"))
        self.guardar=Dialog

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.browse)
        QtCore.QObject.connect(self.aceptar, QtCore.SIGNAL(_fromUtf8("clicked()")), self.accionaceptar)
        QtCore.QObject.connect(self.cancelar, QtCore.SIGNAL(_fromUtf8("clicked()")), self.accioncancelar) 
        
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        pass

    def browse(self):
        print "navegar"
        self.archivo = QtGui.QFileDialog.getOpenFileName(
                         self,
                         "Elegir un archivo para abrir",
                         "C:\wamp\www\prueba",
                         "Fichero de datos (*.txt *.ods)");
        print self.archivo
        partes=self.archivo.split(".")
        ext=partes[len(partes)-1]
        if ext!="txt" and ext!="ods" :
            self.archivo=""
            self.textEdit.setText("")
            QtGui.QMessageBox.information(self,
                "Informacion",
                "El tipo de archivo ingresado no es correcto")
        else:
            self.textEdit.setText(self.archivo)
            self.ext=ext

    def accionaceptar(self):
        print "aceptar"
##      se inicializa el array de bombeos        
        bombeos=[]
        global ContEnsayo

        if self.ext=="txt":
        
##          Se abre el archivo
            f=open(self.archivo)
                
##          Lectura del archivo de los bombeos
##          Se dividen las lineas separadas por \n
            contenido=f.readlines()

##          print "El id inicial es: " + str(ContEnsayo.traerid())        
            for linea in contenido:
##              print linea
##              Se separa la linea por el tabulador
                datos=linea.split("\t")
##              Se esa lina tiene dos columnas se procesa si no no
                if (len(datos)>=2):
                    t=int(datos[0])
                    c=float(datos[1])
                    print "tiempo: "+str(t)
                    print "caudal: "+str(c)
                    b=bombeo.bombeo(t,c)
                    bombeos.append(b)
        else:
            
            f= zipfile.ZipFile((str(self.archivo))) 
            fcontent = f.read('content.xml')
            contenido = xml.dom.minidom.parseString(fcontent)

            datos = contenido.getElementsByTagName('text:p')
            i=0
            for p in datos:
                for ch in p.childNodes:
                    if ch.nodeType == ch.TEXT_NODE:
                        if i==0 :
                            t=int(ch.data)
                            print "tiempo: "+str(t)
                            i=1
                        else:
                            c=float(ch.data)
                            print "caudal: "+str(c)
                            b=bombeo.bombeo(t,c)
                            bombeos.append(b)                            
                            i=0                   

##      Se manda al controlador los bombeos y te retorna el ultimo ensayo creado
        e=ContEnsayo.agregarEnsayo(bombeos)
          
        reply = QtGui.QMessageBox.information(self,
                "Informacion",
                "Se ha creado un nuevo ensayo de bombeo en el sistema. El id es: " + str(e.id))
        
        if reply == QtGui.QMessageBox.Ok:
            print "OK"
            self.guardar.close()            
        else:
            print "Escape"

####        for b in e.devolverB():
##            print "bombeo "+ str(e.id)
##            for i in range(2):
##                print "at " + str(b.devolverAt(i))
     
 
    def accioncancelar(self):
        print "chau"        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    frmImpProyecto = QtGui.QWidget()
    ui = Ui_Dialog()
    ui.setupUi(frmImpProyecto)
    frmImpProyecto.show()
    sys.exit(app.exec_())


