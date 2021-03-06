# -*- coding: cp1252 -*-
"""
	tiponpython Simulacion de ensayos de acuiferos
	Copyright 2012 Andres Pias, Sebastian Daloia, Jesus Guibert
	
	This file is part of tiponpython.

	tiponpython is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	any later version.

	tiponpython is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with tiponpython.  If not, see http://www.gnu.org/licenses/gpl.txt.


Esta es la vista que definira la GUI del dominio.
Con sus clases, y codigo auxiliar.

Creado por TIPONPYTHON Cooperative

"""

from PyQt4 import QtCore, QtGui
import sys
import numpy as np
import asociarEnsayos
import vistaoptimizacion
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


"""
La clase elemento dominio contiene codigo auxiliar. Es una clase
de caracter global.

Sus atributos, a modo de banderas, van a ser aprovechados por las
instancias de la clases boton y box, gbCoordenadas y menu.

Los valores por defecto de estos atributos sonfocusOutEvent

elementoDominio = 0
existe = False
idElemento = 1000

---

Descripcion de elementoDominio

Es una bandera de control, que le dice a la aplicacion que tipo de
elemento se esta arrastrando al dominio para ser creado.

Valores de los elementos actuals

elementoDominio = 0

Es usado para insertar un pozo

elementoDominio = 1

Es usado para insertar una barrera

elementoDominio es cambiado en la funcion mouseMoveEvent de la clase
boton, mientras que es evaluado en la funcion dropEvent de la clase
box.

---

Descripcion de existe

Es una bandera de control binaria que le dice a la aplicacion si el
elemento que esta siendo arrastrado, sobre el dominio, es un nuevo
elemento a crear o si es un elemento que ya existe en el dominio y solo
requiere una nueva ubicacion.

Esta bifurcacion es necesaria para saber si el elemento debe de ser creado
o modificado.

existe es cambiado en la funcion mouseMoveEvent de la clase boton, mientras
que es evaluado en la funcion dropEvent de la clase box.

---

Descripcion de idElemento

Es una bandera de control que le dice a la aplicacion cual es el elemento,
dentro de la lista de elementos, que esta siendo arrastrado sobre
el dominio. Se guarda el identificador del elemento.

idElemento es cambiado en la funcion mouseMoveEvent, y es evaluada en
la funcion dropEvent de la clase box.
-----------

Descripcion de  reloj y transicion

Son banderas de control que le dice a la aplicacion, dependiendo de sus
estados, cuando se puede comenzar a arrastrar un boton.

El estado inicial de estos elementos en cada boton es:

reloj = False
transicion = False

Para cada boton, estas banderas comenzaran a cambiar en el momento en
que se presione el boton. En la funcion mousePressEvent.

El estado luego de este evento es:

reloj = True
transicion = True

La funcion apagar, tiene como cometido liberar el bloqueo del arrastre
seteando los siguientes estados:

reloj = True
transicion = False

En la funcion mouseMoveEvent se encuentra el control necesario de dichos estados.
Para que el usuario pueda arrastrar el boton una vez finalizado el tiempo.

Cuando el usuario suelta el boton en el objeto de la clase box, o cuando presiona
y luego libera el boton el estado es el siguiente:

reloj = False
transicion = False

-----

Descripcion de ConEnsayo

B�sicamente se guarda la instancia del controlador global creado en
el archivo principal. Este hace las veces de controlador, por ende las
operaciones con los modelos se hacen delegandole dichas tareas a este.

------

Descripcion de menuMouse

Es una instancia global de la clase menu(QtGui.QListView)

En su funcion de inicio se setean las acciones estaticas, como
salir o eliminar.

la funcion selectionChanged es sobre escrita para identificar cual
ha sido la accion seleccionado por el usuario.

----------------

Descripcion de selectedMenuMouse

Contiene una referencia al tipo de elemento en el dominio sobre el cual
el usuario hubo aplicacdo un click derecho.
selectedMenuMouse es un diccionario que contiene las claves/valor:

Tipo = ['Punto' | 'Barrera']
id = Identificador del elemento

Esto permite identificar al elemento del dominio sobe el cual se deben
de efectuar las acciones del menu desplegado.

--------------


"""

class elementoDominio(object):

    elementoDominio = 0

    existe = False

    idElemento = 1000

    reloj = False

    transicion = False

    ContEnsayo = ""

    menuMouse = ""

    selectedMenuMouse = {}

    gbCoord = ""

    Dominio = ""

    #Pozo candidato a ser agregado
    pozoCandidato = ""
    hayPozoCandidato = False

    pozoSeleccionado = 0

    
    def __init__(self):
        super(elementoDominio, self).__init__()



class scrollArea(QtGui.QScrollArea):
	def __init__(self, parent):
		super(scrollArea, self).__init__(parent)
		self.setAcceptDrops(True)
		 
	#Sobreescribimos dragEnterEvent para pemitir
	#la accion de este evento.
	def dragEnterEvent(self, e):
		e.accept()

"""
Clase boton, hereda de QPushButton elemento del modulo QtGui
basicamente es un boton para presionar y generar acciones.

Contiene una referencia al elemento global elementoDominio.
Por defecto el identificador de toda instancia es 1000

1000 = Boton Pozo
1001 = Boton Recta

"""
class boton(QtGui.QPushButton):

    global elementoDominio

    id = 1000  

    posicion = 0

    accionCoord = {}
    
    def __init__(self, icono, texto, padre, tooltip):
        super(boton, self).__init__(icono, texto, padre)
        self.init(tooltip)

    def init(self, tooltip):
        
        #Seteo inicial del boton
        self.setAcceptDrops(True)        
        self.tooltip = tooltip       
        self.setGeometry(QtCore.QRect(50, 20, 41, 23))
        self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.setMouseTracking(True)
        self.setToolTip(QtGui.QApplication.translate("Form", tooltip, None, QtGui.QApplication.UnicodeUTF8))
      

    def mousePressEvent(self, e):
        
       if e.button() == QtCore.Qt.LeftButton:
            
            #Cambiamos el cursor, y luego procedemos a evaluar estado del reloj
            #Si no existe creamos un temporizador, cuando alcanze el tiempo dado
            #el usuario va a poder arrastrar el boton.
            self.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))

            if self.id == 1000:
                elementoDominio.gbCoord.setPozo()

		#Volvemos al color normal del pozo seleccionado
		for boton in elementoDominio.Dominio.botones:
			boton.setIcon(QtGui.QIcon("content/images/blackDotIcon.png"))
			
            elif self.id == 1001:
                elementoDominio.gbCoord.setRecta()
            
            if elementoDominio.reloj == False:
                reloj = QtCore.QTimer()
                reloj.singleShot(800, self.apagar)
                elementoDominio.transicion = True
                elementoDominio.reloj = True

            if self.id != 1000 and self.id != 1001:                
                #Se muestran sus coordenadas
                elementoDominio.gbCoord.setPozoExistente(self.id)

                elementoDominio.pozoSeleccionado = self.id                                       
                elementoDominio.gbCoord.actualizarCoordenadasPozo(self.id)
                elementoDominio.Dominio.rectaSeleccionada['id'] = 0 
		
		for pozo in elementoDominio.Dominio.botones:
		    if pozo.id != self.id:
		        pozo.setIcon(QtGui.QIcon("content/images/blackDotIcon.png"))

		self.setIcon(QtGui.QIcon("content/images/redDotIcon.png"))

            else:
                #Reseteo de recta seleccionada
                elementoDominio.Dominio.rectaSeleccionada['id'] = 0
                self.update()
                elementoDominio.gbCoord.eliminarPlacebos()


       else:
           elementoDominio.selectedMenuMouse["tipo"] = "punto"
           elementoDominio.selectedMenuMouse["id"] = self.id
          
           elementoDominio.menuMouse.move(self.pos())

          
           elementoDominio.menuMouse.show()
           
    def mouseMoveEvent(self, e):
        #Evaluacion que se entiende como, 'El usuario puede comenzar a arrastrar el boton'
        if elementoDominio.reloj == True and elementoDominio.transicion == False:
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            mimedata = QtCore.QMimeData()                             
            drag = QtGui.QDrag(self)

            #Sentencia que representa en el margen superior
            #izquierdo del mouse al elemento que esta siendo
            #arrastrado por la ventana.
            
            if self.tooltip == "pozo":
                pixmap = QtGui.QPixmap("content/images/blackDotIcon.png")                                    
                drag.setPixmap(pixmap)
                elementoDominio.elementoDominio = 0                
            else:
                pixmap = QtGui.QPixmap("content/images/blackBarrera.png")                                    
                drag.setPixmap(pixmap)
                elementoDominio.elementoDominio = 1


            #Como se describiese en la enunciacion de la clase elementoDominio
            # se evalua si el elemento es nuevo o ya existe en el dominio.
            #dependiendo de la evaluacion el atrinuto existe sera verdadero o falso
            
            if self.id == 1000 or self.id == 1001:           
                elementoDominio.existe = False  
            else:
                elementoDominio.existe = True

                
            elementoDominio.idElemento = self.id

            drag.setMimeData(mimedata)
            drag.setHotSpot(e.pos() - self.rect().topLeft())
            dropAction = drag.start(QtCore.Qt.MoveAction)

        if self.id != 1000 and self.id != 1001:
            #Se muestran sus coordenadas
            elementoDominio.gbCoord.setPozoExistente(self.id)

    def apagar(self):
        elementoDominio.transicion = False

    #Cuando se suelta el mouse luego de un arrastre
    #incondicionalmente se setean las banderas globales con los siguientes
    #valores
    def mouseReleaseEvent(self, e):        
        elementoDominio.transicion = False
        elementoDominio.reloj = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

"""    
Definimos clase que agrupa elementos, junto con la sobreescritura
de los eventos dragEnterEvent y dropEvent para manejar arrastre y tirada
sobre el elemento
"""        
class box(QtGui.QGroupBox):

    global elementoDominio

    id = 0
   
    def __init__(self, padre):
        super(box, self).__init__(padre)
        self.init()

    #Propiedades y atributos iniciales del QGroupBox
    def init(self):
        self.setAcceptDrops(True)
        self.setMouseTracking(True) 
        self.setGeometry(QtCore.QRect(20, 27, elementoDominio.ContEnsayo.dominio.ancho, elementoDominio.ContEnsayo.dominio.alto))
        self.setTitle(QtGui.QApplication.translate("Form", "Dominio", None, QtGui.QApplication.UnicodeUTF8))
        self.setObjectName(_fromUtf8("Dominio"))


        self.presionandoRecta = False

        self.idRecta = 1000

        self.botones = []

        self.bGiratorios = []

        self.rectaSeleccionada = {}
        self.rectaSeleccionada['id'] = 0

        
    #Sobreescribimos dragEnterEvent para pemitir
    #la accion de este evento.
    def dragEnterEvent(self, e):
        e.accept()
                
    #Evento que es llamado cuando se suelta un elemento
    #dentro del groupbox
    def dropEvent(self, e):
        elementoDominio.reloj = False
        #Obtenemos la posicion relativa del lugar en que el
        #elemento es soltado
        position = e.pos()       

        #Si el elemento no existe creamos uno nuevo, en caso contrario
        #arrastramos el elemento ya existente a una nueva posicion en el
        #dominio.
        if elementoDominio.existe == False:
            if elementoDominio.elementoDominio == 0:        

                b = boton(QtGui.QIcon("content/images/blackDotIcon.png"), "", self, "pozo")
                b.id = elementoDominio.ContEnsayo.agregarPozo(position.x(), position.y())   
		b.setStyleSheet("border: none")             
                b.setGeometry(QtCore.QRect(position.x(), position.y(), 24, 24))
                 
                self.botones.append(b)
                b.show()           

            else:

                r = QtCore.QLineF(position.x(), position.y(), (position.x() + 30), (position.y() + 30))
		elementoDominio.ContEnsayo.agregarRecta(elementoDominio.gbCoord.cbTipo.currentText(), np.float32(r.x1()), np.float32(r.y1()), np.float32(r.x2()), np.float32(r.y2()))                

        else:
            for x in self.botones:
                if x.id == elementoDominio.idElemento:
                    x.move(position)
                    if x.tooltip == "pozo":
                        elementoDominio.ContEnsayo.moverPozo(x.id, position.x(), position.y())
		        elementoDominio.gbCoord.actualizarCoordenadasPozo(x.id)


        elementoDominio.transicion = False
        elementoDominio.reloj = False

        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()
        
    #Definicion de la funcion para comenzar a dibujar
    def paintEvent(self, e):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setBrush(QtGui.QColor(0, 255, 127)) 
        painter.setBackground(painter.brush())
        painter.setBackgroundMode(QtCore.Qt.OpaqueMode)
        self.dibujarRectas(painter)
        painter.end()
        
    #Funcion de dibujado de lineas
    def dibujarRectas(self, painter):
        self.rectas = elementoDominio.ContEnsayo.dibujarRecta()
        for x in self.rectas:  
            if len(self.rectaSeleccionada) > 0:
                if self.rectaSeleccionada['id'] == x.id:
                    painter.setPen(QtCore.Qt.red)
                    painter.drawLine(QtCore.QLineF( x.x1, x.y1, x.x2, x.y2 ))
                    if x.x1 < x.x2 :                        
                        painter.drawLine(QtCore.QLineF( x.x1, x.y1, x.x3, x.y3))
                        painter.drawLine(QtCore.QLineF( x.x4, x.y4, x.x2, x.y2))
                    else:
                        painter.drawLine(QtCore.QLineF( x.x1, x.y1, x.x4, x.y4))
                        painter.drawLine(QtCore.QLineF( x.x3, x.y3, x.x2, x.y2))
                else:
                    painter.setPen(QtCore.Qt.blue)
                    painter.drawLine(QtCore.QLineF( x.x1, x.y1, x.x2, x.y2))
                    if x.x1 < x.x2 :
                        painter.drawLine(QtCore.QLineF( x.x1, x.y1, x.x3, x.y3))
                        painter.drawLine(QtCore.QLineF( x.x4, x.y4, x.x2, x.y2))
                    else:
                        painter.drawLine(QtCore.QLineF( x.x1, x.y1, x.x4, x.y4))
                        painter.drawLine(QtCore.QLineF( x.x3, x.y3, x.x2, x.y2))
            else:                
                painter.setPen(QtCore.Qt.blue)
                painter.drawLine(QtCore.QLineF( x.x1, x.y1, x.x2, x.y2))
                if x.x1 < x.x2 :
                      painter.drawLine(QtCore.QLineF( x.x1, x.y1, x.x3, x.y3))
                      painter.drawLine(QtCore.QLineF( x.x4, x.y4, x.x2, x.y2))
                else:
                      painter.drawLine(QtCore.QLineF( x.x1, x.y1, x.x4, x.y4))
                      painter.drawLine(QtCore.QLineF( x.x3, x.y3, x.x2, x.y2))

        if elementoDominio.ContEnsayo.hayRectaCandidata():

            painter.drawLine(elementoDominio.ContEnsayo.rectaCandidata.x1, elementoDominio.ContEnsayo.rectaCandidata.y1,
                             elementoDominio.ContEnsayo.rectaCandidata.x2, elementoDominio.ContEnsayo.rectaCandidata.y2)

        self.update()

    def mouseMoveEvent(self, e):
	print self.width(), self.height()
	elementoDominio.coordenadas.setText("x ->" + QtCore.QString.number(e.pos().x(), 10) + " y -> " + QtCore.QString.number(e.pos().y(), 10) )

        #Buscamos si las coordenadas actuales estan cerca de algun punto de alguna recta
        lista = elementoDominio.ContEnsayo.buscarPuntoEnRecta(np.float32(e.pos().x()), np.float32(e.pos().y()))
        
        botonGiratorio = boton(QtGui.QIcon("content/images/redDotIcon.png"), "",  elementoDominio.Dominio, "pozo")
	#QtGui.QPushButton(self)
        #Si hay puntos entonces cambiamos icono del mouse, y mostramos boton. De lo contrario
        #eliminamos el boton mostrado.
        if  len(lista) > 0:
            if lista['eje'] == "x":
                self.setCursor(QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))
            else:
                self.setCursor(QtGui.QCursor(QtCore.Qt.SizeBDiagCursor))

            #Enviamos identificador a funcion que expresa las coordenadas de manera grafica
            elementoDominio.gbCoord.setRectaExistente(lista['id'], self.rectaSeleccionada['id'])

            botonGiratorio.setGeometry (lista['punto'].x(), lista['punto'].y(), 10, 10)
            self.bGiratorios.append(botonGiratorio)
            botonGiratorio.show()
            self.idRecta = lista['id']
        else:
            if not self.presionandoRecta:
                self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            botonGiratorio.hide()
            self.aEliminar = []
            for x in self.bGiratorios:                
                x.hide()
                self.aEliminar.append(x)

            for x in self.aEliminar:
                try:
                    self.bGiratorios.remove(x)
                    break
                except ValueError:
                    print "Sobrepaso de rangos, advertencia simple"

    def mousePressEvent(self, e):

        if e.button() == QtCore.Qt.RightButton:

            elementoDominio.selectedMenuMouse["tipo"] = "recta"
            elementoDominio.selectedMenuMouse["id"] = 0


            if np.int(self.cursor().shape()) == 8:
                elementoDominio.selectedMenuMouse["id"] = elementoDominio.ContEnsayo.buscarPuntoPorQ(e.pos().x(), e.pos().y())
                 

            if np.int(self.cursor().shape()) == 7:
                elementoDominio.selectedMenuMouse["id"] = elementoDominio.ContEnsayo.buscarPuntoPorR(e.pos().x(), e.pos().y())
            
            if elementoDominio.selectedMenuMouse["id"]  != 0:     
                elementoDominio.menuMouse.move(e.pos())                
                elementoDominio.menuMouse.show()

        else:

            #Si el dominio esta comenzado a ser presionado por un cursor que sea
            #utilizado cuando se trabaja con barreras, entonces se setea el atributo
            #self.presionandoRecta a verdadero.
            if np.int(self.cursor().shape()) == 8 or np.int(self.cursor().shape()) == 7:
                self.presionandoRecta = True
                
                recta = elementoDominio.ContEnsayo.buscarPuntoEnRecta(e.pos().x(), e.pos().y())
                
                if len(recta) > 0:
                    self.rectaSeleccionada['id'] = recta['id']

                    for pozo in elementoDominio.Dominio.botones:
                	    if pozo.id == elementoDominio.pozoSeleccionado:                 
				    pozo.setIcon(QtGui.QIcon("content/images/blackDotIcon.png"))
				    elementoDominio.pozoSeleccionado = 0
                    

    def mouseReleaseEvent(self, e):
        #Dependiendo del tipo de cursos con el que se este modificando la recta
        #se sabra cual es el punto en la misma que hay que modificar
        if e.button() == QtCore.Qt.LeftButton:
            if np.int(self.cursor().shape()) == 8:
                self.presionandoRecta = False
                elementoDominio.ContEnsayo.actualizarRecta(self.idRecta, e.pos().x(), e.pos().y(), "Q")
                self.update()
            if np.int(self.cursor().shape()) == 7:
                self.presionandoRecta = False
                elementoDominio.ContEnsayo.actualizarRecta(self.idRecta, e.pos().x(), e.pos().y(), "R")
                self.update()


"""
Menun utilizado en definir dominio
Brinda opciones de operacion sobre los elementos
cuando se le aplica a los mismos un click derecho
"""
class menu(QtGui.QListView):
    def __init__(self, padre):
        super(menu, self).__init__(padre)
        self.init()

    def init(self):
        #Valores iniciales del menu, incluido el modelo
        self.items = QtCore.QStringList()
        self.items << "MENU" << "Optimizar" << "Asociar" << "Eliminar" << "Salir"    
        modelo = QtGui.QStringListModel(self.items)
        self.setModel(modelo)        
        self.setGeometry(QtCore.QRect(60, 60, 131, 131))
        self.hide()
    def leaveEvent(self,coso):
        print "Cierro el menu"
        self.reset()
        self.hide()        
    def selectionChanged(self, selected,  deselected):
        #indices es un iterador de la lista de QItemSelection que se retorna
        #al momento de una seleccion en la vista.
        #la funcion first del QItemSelection retorna un QModelIndex
        #que es un indice dentro del mapeo del modelo MVC de Qt
        #Los datos son obtenidos a traves de la funcion data, para la secuencial
        #evaluacion.
        
        for indices in selected.first().indexes():
            valor = indices.data()
            if valor.toString() == "Salir":
                self.reset()
                self.hide()
                return
            if valor.toString() == "Eliminar":
                
                elementoDominio.gbCoord.ocultarFormulario()                
                
                if elementoDominio.selectedMenuMouse["tipo"] == "punto":
                    
                    elementoDominio.ContEnsayo.removerPozo(elementoDominio.selectedMenuMouse["id"])

                    self.aEliminar = []
                    
                    for x in elementoDominio.Dominio.botones:
                        if x.id == elementoDominio.selectedMenuMouse["id"]:
                            x.hide()
                            self.aEliminar.append(x)

                    for x in self.aEliminar:
                        try:
                            elementoDominio.Dominio.botones.remove(x)
                            break
                        except ValueError:
                            print "Punto a eliminar no encontrado, advertencia simple"

                if elementoDominio.selectedMenuMouse["tipo"] == "recta":
                    elementoDominio.ContEnsayo.eliminarRecta(elementoDominio.selectedMenuMouse["id"])
                    self.update()


                elementoDominio.selectedMenuMouse["tipo"] == ""
                elementoDominio.selectedMenuMouse["id"] == -1
                self.reset()
                self.hide()   

            if valor.toString() == "Asociar":
                
	  	frmasociar=QtGui.QDialog()
                ui= asociarEnsayos.Ui_Dialog()
                ui.setupUi(frmasociar, elementoDominio.selectedMenuMouse["id"], elementoDominio.ContEnsayo, False)
                frmasociar.exec_()
                elementoDominio.widget = frmasociar
                self.hide()
            if valor.toString() == "Optimizar":
                i = QtCore.QStringList()
                i << elementoDominio.ContEnsayo.optimizacioneslistar() << "Salir"    
                m = QtGui.QStringListModel(i)              
                #Listo los metodos de optimizacion
                menusito=menu(elementoDominio.Dominio)
                menusito.setModel(m)
                menusito.move(self.pos().x()+30,self.pos().y())           
                menusito.show()                
                #Cierro el menu contextual
                self.reset()
                self.hide()
                return
            #Si no es ninguna opcion predeterminada, las opcoines son para elegir metodos de optimizacion
            if valor.toString() != "Optimizar" and valor.toString() != "Salir" and valor.toString() != "Eliminar" and valor.toString() != "Asociar" :
                print "valor es optimizar"
                #Agrego ala coleccion de pozos para optimizar
                print "Agrego para optimizar el pozo " 
                print elementoDominio.selectedMenuMouse["id"]
                elementoDominio.ContEnsayo.asociarPozoOptimiazion(elementoDominio.selectedMenuMouse["id"],valor.toString())                
                frmopt=QtGui.QDialog()
                ui= vistaoptimizacion.optimizacion(elementoDominio.ContEnsayo,frmopt)
                #ui.setupUi(frmopt,elementoDominio.ContEnsayo)
                #frmopt.show()
                elementoDominio.widget = ui                
                getattr(self,'reset')()
                getattr(self,'hide')()
                return  

"""
Clase que maneja la interfaz de coordenadas
"""
class gbCoordenadas(QtGui.QGroupBox):
    def __init__(self, padre):
        super(gbCoordenadas, self).__init__(padre)
        self.init()

    def init(self):
        self.setGeometry(QtCore.QRect(260, 110, 151, 181))
        self.setTitle("Coordenadas")

        #Etiqueta de Tipo 
        self.label = QtGui.QLabel(self)
        self.label.setGeometry(QtCore.QRect(10, 20, 91, 16))
        self.label.setText(QtGui.QApplication.translate("Form", "Recta Pozo", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.label.setVisible(False)

        #X1
        self.lineEdit = QtGui.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(40, 50, 25, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit.setVisible(False)

        #Y1
        self.lineEdit_2 = QtGui.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(100, 50, 25, 20))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.lineEdit_2.setVisible(False)

        #X2
        self.lineEdit_3 = QtGui.QLineEdit(self)
        self.lineEdit_3.setGeometry(QtCore.QRect(40, 100, 25, 20))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.lineEdit_3.setVisible(False)

        #Y2
        self.lineEdit_4 = QtGui.QLineEdit(self)
        self.lineEdit_4.setGeometry(QtCore.QRect(100, 100, 25, 20))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.lineEdit_4.setVisible(False)

        #X1
        self.label_2 = QtGui.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 25, 20))
        self.label_2.setText("X1")
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_2.setVisible(False)


        #Y1
        self.label_3 = QtGui.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(75, 50, 25, 20))
        self.label_3.setText("Y1")
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_3.setVisible(False)


        #X2
        self.label_4 = QtGui.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(10, 100, 25, 20))
        self.label_4.setText("X2")
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_4.setVisible(False)

        #Y2
        self.label_5 = QtGui.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(75, 100, 25, 20))
        self.label_5.setText("Y2")
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_5.setVisible(False)
        
        #Combo box
        self.cbTipo = QtGui.QComboBox( self )
        self.cbTipo.setGeometry(QtCore.QRect(60,20, 60, 20))
        listaStrings = QtCore.QStringList()
        listaStrings << "Negativo" << "Positivo"
        
        self.cbTipo.addItems(listaStrings)
        self.cbTipo.setVisible(False)
        


        #Boton Aceptar
        self.btnAceptar = QtGui.QPushButton(self)
        self.btnAceptar.setGeometry(QtCore.QRect(10, 155, 50, 20))
        self.btnAceptar.setText("Aceptar")
        self.btnAceptar.setVisible(False)
           
        #Boton Cancelar
        self.btnCancelar = QtGui.QPushButton(self)
        self.btnCancelar.setGeometry(QtCore.QRect(80, 155, 50, 20))
        self.btnCancelar.setText("Cancelar")
        self.btnCancelar.setVisible(False)

        #Boton de Vista Previa
        self.btnPrevia = QtGui.QPushButton(self)
        self.btnPrevia.setGeometry(QtCore.QRect(10, 130, 100, 20))
        self.btnPrevia.setText("Vista Previa")
        self.btnPrevia.setVisible(False)

        #Boton Actualizar
        self.btnActualizar = QtGui.QPushButton(self)
        self.btnActualizar.setGeometry(QtCore.QRect(10,130, 100, 20))
        self.btnActualizar.setText("Actualizar")
        self.btnActualizar.setVisible(False)

        QtCore.QObject.connect(self.btnAceptar, QtCore.SIGNAL('clicked()'), self.setAceptar)
        QtCore.QObject.connect(self.btnCancelar, QtCore.SIGNAL('clicked()'), self.setCancelar)
        QtCore.QObject.connect(self.btnPrevia, QtCore.SIGNAL('clicked()'), self.setPrevia)
        QtCore.QObject.connect(self.btnActualizar, QtCore.SIGNAL('clicked()'), self.setActualizar)

        #Validacion
        self.validador = QtGui.QIntValidator(-100, 900, self)

        self.lineEdit.setValidator(self.validador)
        self.lineEdit_2.setValidator(self.validador)
        self.lineEdit_3.setValidator(self.validador)
        self.lineEdit_4.setValidator(self.validador)
        
    def setPozo(self):
        #Etiqueta de Tipo 
        self.label.setText(QtGui.QApplication.translate("Form", "Pozo", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setVisible(True)

        #X1
        self.lineEdit.setText(QtGui.QApplication.translate("Form", "", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setVisible(True)

        #Y1
        self.lineEdit_2.setText(QtGui.QApplication.translate("Form", "", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_2.setVisible(True)

        #X2
        self.lineEdit_3.setVisible(False)

        #Y2
        self.lineEdit_4.setVisible(False)

        #X1
        self.label_2.setVisible(True)


        #Y1
        self.label_3.setVisible(True)


        #X2
        self.label_4.setVisible(False)

        #Y2
        self.label_5.setVisible(False)
    
        #Combo
        self.cbTipo.setVisible(False)

        #Boton Aceptar
        self.btnAceptar.setVisible(True)
           
        #Boton Cancelar
        self.btnCancelar.setVisible(True)

        #Vista Previa
        self.btnPrevia.setVisible(True)

        #Boton Actualizar
        self.btnActualizar.setVisible(False)

    def setRecta(self):
        #Etiqueta de Tipo 
        self.label.setText(QtGui.QApplication.translate("Form", "Recta", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setVisible(True)

        #X1
        self.lineEdit.setText(QtGui.QApplication.translate("Form", "", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setVisible(True)

        #Y1
        self.lineEdit_2.setText(QtGui.QApplication.translate("Form", "", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_2.setVisible(True)

        #X2
        self.lineEdit_3.setText(QtGui.QApplication.translate("Form", "", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_3.setVisible(True)

        #Y2
        self.lineEdit_4.setText(QtGui.QApplication.translate("Form", "", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_4.setVisible(True)

        #X1
        self.label_2.setVisible(True)


        #Y1
        self.label_3.setVisible(True)


        #X2
        self.label_4.setVisible(True)

        #Y2
        self.label_5.setVisible(True)

        #Combo
        self.cbTipo.setVisible(True)


        #Boton Aceptar
        self.btnAceptar.setVisible(True)
           
        #Boton Cancelar
        self.btnCancelar.setVisible(True)

        #Vista Previa
        self.btnPrevia.setVisible(True)

        #Boton Actualizar
        self.btnActualizar.setVisible(False)
        
    def setAceptar(self):

        if self.label.text() == "Pozo":

            if self.lineEdit.text() != "" and self.lineEdit_2.text() != "":
                if not elementoDominio.hayPozoCandidato:
                    elementoDominio.pozoCandidato = QtGui.QPushButton(elementoDominio.Dominio)
                    elementoDominio.hayPozoCandidato = True
                    elementoDominio.pozoCandidato.setGeometry(QtCore.QRect(np.int32(self.lineEdit.text()),
                                                                           np.int32(self.lineEdit_2.text()), 25, 20))
                    elementoDominio.pozoCandidato.show()
                            
            
                b = boton(QtGui.QIcon("content/images/blackDotIcon.png"), "", elementoDominio.Dominio, "pozo")

                b.id = elementoDominio.ContEnsayo.agregarPozo(elementoDominio.pozoCandidato.x(), elementoDominio.pozoCandidato.y())                

                elementoDominio.Dominio.botones.append(b)

                b.show()
                elementoDominio.pozoCandidato.hide()
                elementoDominio.pozoCandidato = None
                elementoDominio.hayPozoCandidato = False

            

        else:                                   
            if self.lineEdit.text() != "" and self.lineEdit_2.text() != "" and self.lineEdit_3.text()!= "" and self.lineEdit_4.text() != "":
                if not elementoDominio.ContEnsayo.hayRectaCandidata():
                    elementoDominio.ContEnsayo.agregarRecta(self.cbTipo.currentText(), 
np.int32(self.lineEdit.text()), np.int32(self.lineEdit_2.text()), np.int32(self.lineEdit_3.text()),
                                                                     np.int32(self.lineEdit_4.text()))
                else:
                    elementoDominio.ContEnsayo.incluirCandidata(self.cbTipo.currentText())

                self.update()
                
        #Reseteo de recta seleccionada
        elementoDominio.Dominio.rectaSeleccionada['id'] = 0
        self.update()

        #Etiqueta de Tipo 
        self.label.setText(QtGui.QApplication.translate("Form", "Recta", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setVisible(False)

        #X1
        self.lineEdit.setVisible(False)

        #Y1
        self.lineEdit_2.setVisible(False)

        #X2
        self.lineEdit_3.setVisible(False)

        #Y2
        self.lineEdit_4.setVisible(False)

        #X1
        self.label_2.setVisible(False)


        #Y1
        self.label_3.setVisible(False)


        #X2
        self.label_4.setVisible(False)

        #Y2
        self.label_5.setVisible(False)

        #Combo
        self.cbTipo.setVisible(False)

        #Boton Aceptar
        self.btnAceptar.setVisible(False)
           
        #Boton Cancelar
        self.btnCancelar.setVisible(False)

        #Vista Previa
        self.btnPrevia.setVisible(False)

        
    def setCancelar(self):
        
        #Etiqueta de Tipo 
        self.label.setText(QtGui.QApplication.translate("Form", "Recta", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setVisible(False)

        #X1
        self.lineEdit.setVisible(False)

        #Y1
        self.lineEdit_2.setVisible(False)

        #X2
        self.lineEdit_3.setVisible(False)

        #Y2
        self.lineEdit_4.setVisible(False)

        #X1
        self.label_2.setVisible(False)

        #Y1
        self.label_3.setVisible(False)


        #X2
        self.label_4.setVisible(False)

        #Y2
        self.label_5.setVisible(False)

        #Combo
        self.cbTipo.setVisible(False)

        #Boton Aceptar
        self.btnAceptar.setVisible(False)
           
        #Boton Cancelar
        self.btnCancelar.setVisible(False)

        #Vista Previa
        self.btnPrevia.setVisible(False)


        if elementoDominio.ContEnsayo.hayRectaCandidata:
            elementoDominio.ContEnsayo.eliminarRectaCandidata()
        if elementoDominio.hayPozoCandidato:
            elementoDominio.hayPozoCandidato = False
            elementoDominio.pozoCandidato.hide()
            elementoDominio.pozoCandidato = None

    def setPrevia(self):
        
        if self.label.text() == "Pozo":
            if self.lineEdit.text() != "" and self.lineEdit_2.text() != "":
                if not elementoDominio.hayPozoCandidato:
                    elementoDominio.pozoCandidato = QtGui.QPushButton(elementoDominio.Dominio)
                    elementoDominio.hayPozoCandidato = True
                elementoDominio.pozoCandidato.setGeometry(QtCore.QRect(np.int32(self.lineEdit.text()),
                                                                       np.int32(self.lineEdit_2.text()), 25, 20))
                elementoDominio.pozoCandidato.setIcon(QtGui.QIcon("content/images/redDotIcon.png"))

                
                elementoDominio.pozoCandidato.show()
                 
                

        else:                                   
            if self.lineEdit.text() != "" and self.lineEdit_2.text() != "" and self.lineEdit_3.text()!= "" and self.lineEdit_4.text() != "":
		
                elementoDominio.ContEnsayo.agregarRectaCandidata(self.cbTipo.currentText(), 
np.int32(self.lineEdit.text()), np.int32(self.lineEdit_2.text()), np.int32(self.lineEdit_3.text()),
                                                                 np.int32(self.lineEdit_4.text()))

    def setPozoExistente(self, idPozo):

        if elementoDominio.Dominio.rectaSeleccionada['id'] == 0:

            coordenadas = elementoDominio.ContEnsayo.retornarCoordenadas(idPozo)
            
            if elementoDominio.pozoSeleccionado == 0:
                self.lineEdit.setText(QtCore.QString.number(coordenadas['x'], 10))
                self.lineEdit_2.setText(QtCore.QString.number(coordenadas['y'], 10))                

            self.idElemento = idPozo
            self.tipoElemento = "pozo"
            
            if not self.btnActualizar.isVisible():
                self.btnActualizar.setVisible(True)
                self.btnAceptar.setVisible(False)
                self.btnCancelar.setVisible(False)
                self.btnPrevia.setVisible(False)

                self.lineEdit.setVisible(True)
                self.lineEdit_2.setVisible(True)
                self.eliminarPlacebos()

            self.lineEdit_3.setVisible(False)
            self.lineEdit_4.setVisible(False)
            self.label_4.setVisible(False)
            self.label_5.setVisible(False)
            self.cbTipo.setVisible(False)


            self.label.setText(QtGui.QApplication.translate("Form", "Pozo", None, QtGui.QApplication.UnicodeUTF8))

    def setActualizar(self):
        
        elementoDominio.Dominio.rectaSeleccionada['id'] = 0       
        
        if elementoDominio.pozoSeleccionado != 0:
            for pozo in elementoDominio.Dominio.botones:
                if pozo.id == elementoDominio.pozoSeleccionado:
                    pozo.setIcon(QtGui.QIcon("content/images/blackDotIcon.png"))

                    for pozo in elementoDominio.Dominio.botones:
                        if pozo.id == elementoDominio.pozoSeleccionado:

                            elementoDominio.ContEnsayo.moverPozo(elementoDominio.pozoSeleccionado, np.int32(self.lineEdit.text()), np.int32(self.lineEdit_2.text()))

                            pozo.move(np.int32(self.lineEdit.text()), np.int32(self.lineEdit_2.text()))
                    
                    elementoDominio.pozoSeleccionado = 0
                    return



        if self.tipoElemento == "pozo":
            
            elementoDominio.ContEnsayo.moverPozo(self.idElemento, np.int32(self.lineEdit.text()), np.int32(self.lineEdit_2.text()))

            for pozo in elementoDominio.Dominio.botones:
                if pozo.id == self.idElemento:
                    pozo.move(np.int32(self.lineEdit.text()), np.int32(self.lineEdit_2.text()))

        if self.tipoElemento == "barrera":
             
            elementoDominio.ContEnsayo.actualizarRectaCoord(self.idElemento, np.int32(self.lineEdit.text()),
                                                       np.int32(self.lineEdit_2.text()),  
np.int32(self.lineEdit_3.text()),np.int32(self.lineEdit_4.text()), self.cbTipo.currentText())
            self.update()
            
    def setRectaExistente(self, idElemento, irRE):

        if elementoDominio.pozoSeleccionado == 0:
            self.tipoElemento = "barrera"
            self.idElemento = idElemento

            recta = elementoDominio.ContEnsayo.buscarRecta(self.idElemento)

            if irRE == 0:
                self.lineEdit.setText(QtCore.QString.number(recta.x1, 10))
                self.lineEdit_2.setText(QtCore.QString.number(recta.y1, 10))
                self.lineEdit_3.setText(QtCore.QString.number(recta.x2, 10))
                self.lineEdit_4.setText(QtCore.QString.number(recta.y2, 10))
		 
		if recta.tipo == "Positivo":
		    self.cbTipo.setCurrentIndex(1)
		else:
		    self.cbTipo.setCurrentIndex(0)

            else:
                recta = elementoDominio.ContEnsayo.buscarRecta(irRE)
                
                self.lineEdit.setText(QtCore.QString.number(recta.x1, 10))
                self.lineEdit_2.setText(QtCore.QString.number(recta.y1, 10))
                self.lineEdit_3.setText(QtCore.QString.number(recta.x2, 10))
                self.lineEdit_4.setText(QtCore.QString.number(recta.y2, 10))

		if recta.tipo == "Positivo":
		    self.cbTipo.setCurrentIndex(1)
		else:
		    self.cbTipo.setCurrentIndex(0)
            

            if not self.btnActualizar.isVisible():
                
                self.btnActualizar.setVisible(True)

                self.btnAceptar.setVisible(False)
                self.btnCancelar.setVisible(False)
                self.btnPrevia.setVisible(False)

                self.lineEdit.setVisible(True)
                self.lineEdit_2.setVisible(True)
                self.eliminarPlacebos()

            self.label.setText(QtGui.QApplication.translate("Form", "Recta", None, QtGui.QApplication.UnicodeUTF8))            
            self.lineEdit_3.setVisible(True)
            self.lineEdit_4.setVisible(True)
            self.label_5.setVisible(True)
            self.label_4.setVisible(True)
            self.label_3.setVisible(True)
	    self.label_2.setVisible(True)
            self.label.setVisible(True)
            self.cbTipo.setVisible(True)



    def actualizarCoordenadasPozo(self, idPozo):        
        for pozo in elementoDominio.Dominio.botones:
            if pozo.id == idPozo:
	        self.lineEdit.setText(QtCore.QString.number(pozo.x(), 10))
                self.lineEdit_2.setText(QtCore.QString.number(pozo.y(), 10))
                elementoDominio.Dominio.rectaSeleccionada['id'] = 0
                self.setPozoExistente(idPozo)

    def ocultarFormulario ( self ):
        #Etiqueta de Tipo 
        self.label.setText(QtGui.QApplication.translate("Form", "Recta", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setVisible(False)

        #X1
        self.lineEdit.setText(QtGui.QApplication.translate("Form", "", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setVisible(False)

        #Y1
        self.lineEdit_2.setText(QtGui.QApplication.translate("Form", "", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_2.setVisible(False)

        #X2
        self.lineEdit_3.setText(QtGui.QApplication.translate("Form", "", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_3.setVisible(False)

        #Y2
        self.lineEdit_4.setText(QtGui.QApplication.translate("Form", "", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_4.setVisible(False)

        #X1
        self.label_2.setVisible(False)


        #Y1
        self.label_3.setVisible(False)

        #X2
        self.label_4.setVisible(False)

        #Y2
        self.label_5.setVisible(False)

        #Combo
        self.cbTipo.setVisible(False)


        #Boton Aceptar
        self.btnAceptar.setVisible(False)
           
        #Boton Cancelar
        self.btnCancelar.setVisible(False)

        #Vista Previa
        self.btnPrevia.setVisible(False)

        #Boton Actualizar
        self.btnActualizar.setVisible(False)


    def eliminarPlacebos(self):
        if elementoDominio.ContEnsayo.hayRectaCandidata():
            elementoDominio.ContEnsayo.eliminarRectaCandidata()

        if elementoDominio.hayPozoCandidato:
            elementoDominio.pozoCandidato.hide()
            elementoDominio.pozoCandidato = None
            elementoDominio.hayPozoCandidato = False
 


"""
La clase Ui_Form es invocada en el archivo principal de la aplicacion.
su funcion es agregar los elementos correspondientes a la vista de
crear dominio
"""

class Ui_Form(object):

	def setupUi(self, Form, ContEnsayo):


		elementoDominio.ContEnsayo = ContEnsayo

		#Seteo del formulario que contendra todos los widgets del dominio
		self.frame = QtGui.QFrame(Form)
	 
		self.frame.setGeometry(QtCore.QRect(170, 80, 471, 351))
		self.frame.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
		self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
		self.frame.setFrameShadow(QtGui.QFrame.Raised)
		self.frame.setObjectName(_fromUtf8("frame"))
		self.frame.setEnabled(True)
		self.frame.setStyleSheet("QFrame{background-color: rgb(40, 255, 40); \n"
						"border: 2px solid green; \n"
						"border-radius: 25px}")

		self.groupBoxDominio = QtGui.QGroupBox(self.frame)
		self.groupBoxDominio.setGeometry(QtCore.QRect(20, 27,  elementoDominio.ContEnsayo.dominio.ancho, elementoDominio.ContEnsayo.dominio.alto))
		self.groupBoxDominio.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.groupBoxDominio.setTitle(QtGui.QApplication.translate("Form", "Dominio", None, QtGui.QApplication.UnicodeUTF8))

##		self.groupBoxDominio.setStyleSheet("QGroupBox{background-color: white; \n"
##						" border: 2px solid green;}")


		#Caja de elementos especifica del dominio
		elementoDominio.Dominio = box(self.groupBoxDominio)
		self.caja=elementoDominio.Dominio 

		#Definimos la instancia global del menu y le asociamo
		#un padre.
		elementoDominio.menuMouse = menu(self.frame)       
		
		self.groupBox = QtGui.QGroupBox(self.frame)
		self.groupBox.setGeometry(QtCore.QRect(260, 20, 151, 81))
		self.groupBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.groupBox.setTitle(QtGui.QApplication.translate("Form", "Barra Herramientas", None, QtGui.QApplication.UnicodeUTF8))

		self.groupBox.setStyleSheet("QGroupBox{border: 2px solid green} \n"
					"QPushButton{border: 2px solid red;}")

		self.groupBox.setObjectName(_fromUtf8("groupBox"))

		    
		#Creacion de botones de la barra de herramientas
		self.pozo = boton(QtGui.QIcon("content/images/blackDotIcon.png"), "", self.groupBox, "pozo")
		self.barrera = boton(QtGui.QIcon("content/images/blackBarrera.png"), "", self.groupBox, "barrera")

		self.barrera.setGeometry(QtCore.QRect(50, 50, 41, 20))
		self.barrera.id = 1001
		

		elementoDominio.gbCoord = gbCoordenadas(self.frame)
		elementoDominio.gbCoord.setStyleSheet("QGroupBox{border: 2px solid green} \n"
							"QLabel, QPushButton{border: 2px solid red;}")



		if elementoDominio.ContEnsayo.dominio.ancho > 200 or elementoDominio.ContEnsayo.dominio.alto > 200:
		 	self.scrollArea = scrollArea(self.frame)

			self.scrollArea.setGeometry(QtCore.QRect(20, 27, 235, 300))

			self.scrollArea.setWidget(self.groupBoxDominio)

			self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)

			self.scrollArea.setHorizontalScrollBarPolicy(2)

			self.scrollArea.setVerticalScrollBarPolicy(2)

		self.coordenadas = QtGui.QLabel(self.frame)
		self.coordenadas.setGeometry(QtCore.QRect(100, 325, 140, 20))
		elementoDominio.coordenadas = self.coordenadas
 


		self.frame.show()
		
	def retranslateUi(self, Form):
		pass
 

