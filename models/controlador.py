from PyQt4 import QtCore, QtGui
from pozo  import pozo
from barrera import barrera
import numpy as np
import observacion
import observacionesensayo
import bombeo
import ensayobombeo
import dominio

class Proyecto(object):
    
    def __init__(self):        
        self.ultimoIdEns=0
        self.ultimoIdObs=0
        self.ensayos=[]
        self.observaciones=[]
        self.dominio = dominio.dominio()

        #Lista que guardan pozo y recta
        self.listaPozo = []
        self.listaRecta = []

        #Ultima recta y pozo agregados
        self.idP = 0
        self.idR = 0
        
    def agregarEnsayo(self, bombeos):
        self.ultimoIdEns=self.ultimoIdEns + 1
        e=ensayobombeo.ensayobombeo(bombeos, self.ultimoIdEns)
        self.ensayos.append(e)
        return e

    def agregarObservacion(self, observaciones):
        self.ultimoIdObs=self.ultimoIdObs + 1
        obse=observacionesensayo.observacionesensayo(observaciones, self.ultimoIdObs)
        self.observaciones.append(obse)
        return obse

    #CRUD de pozos
    def agregarPozo(self, identificador, x, y):        
        p = pozo(x, y)
        self.idP = self.idP + 1
        p.id = self.idP
        self.listaPozo.append(p)
        return p.id
                

    def moverPozo(self, idElemento, x, y):
        for x in self.listaPozo:
            if x.id == idElemento:
                x.actualizarCoordenadas(x, y)
                return
            
    def removerPozo(self, idElemento):
        print "Identificador a eliminar", idElemento

        for p in self.listaPozo:
            print "Identificadores de los pozos", p.id
            
        for x in self.listaPozo:
            if x.id == idElemento:
                self.listaPozo.remove(x)
                print "Pozo eliminado"

        for x in self.listaPozo:
            print x.id

    def retornarCoordenadas(self, idElemento):
        listaRetorno = {}

        for x in self.listaPozo:
            if x.id == idElemento:
                listaRetorno["x"] = x.x
                listaRetorno["y"] = x.y
                
                return listaRetorno
            
        print "NADA HE ENCONTRADO"
        return listaRetorno
        

    #CRUD de barreras
    def agregarRecta(self, tipo, x1, y1, x2, y2):        
        r = barrera(x1, x2, y1, y2, tipo)
        r.id = len(self.listaRecta)
        self.listaRecta.append(r)        

    def dibujarRecta(self):
        return self.listaRecta
            
    def buscarPuntoEnRecta(self, x, y):

        #print "X = ", x, " Y = ", y
        
        for barrera in self.listaRecta:

            recta = QtCore.QLine(barrera.x1, barrera.y1, barrera.x2, barrera.y2)

            puntoP = QtCore.QPoint(x, y)
            puntoQ = QtCore.QPoint(recta.x1(), recta.y1())

            rectay = QtCore.QLine(puntoP, puntoQ)           

            puntoR = QtCore.QPoint(recta.x2(), recta.y2())

            rectaw = QtCore.QLine(puntoP, puntoR)           

            valor1 = np.absolute(recta.dx() /2)
            valor2 = np.absolute(recta.dy() /2)
            #print "Valor absoluto de la recta recta recta.dx() =", valor1, " recta.dy() = ", valor2    
            
            #Recta prozima a las x
            if  np.absolute(rectay.dx()) < np.absolute(recta.dx() /2) and  np.absolute(rectay.dy()) < np.absolute((recta.dy() / 2)):               
                lista = {}
                lista['punto'] = puntoQ
                lista['eje'] = "x"
                lista['id'] = barrera.id
                return lista
            
            #Recta proxima a las y
            if np.absolute(rectaw.dx()) < np.absolute(recta.dx() /2) and  np.absolute(rectaw.dy()) < np.absolute((recta.dy() / 2)):
                lista = {}
                lista['punto'] = puntoR
                lista['eje'] = "y"
                lista['id'] = barrera.id
                return lista
        lista = {}
        return lista

    def actualizarRecta(self, idRecta, x, y, tipoPunto):
        for barrera in self.listaRecta:
            if barrera.id == idRecta:
                
                if tipoPunto == "R":                    
                    recta = QtCore.QLine(barrera.x1, barrera.y1, x, y)
                    
                    if np.absolute(recta.dy()) > 1 and  np.absolute(recta.dx()) > 1:
                        barrera.x2 = x
                        barrera.y2 = y
                    
                else:                
                    recta = QtCore.QLine(x, y, barrera.x2, barrera.y2)
                    
                    if np.absolute(recta.dx()) > 1 and np.absolute(recta.dy()) > 1:
                        barrera.x1 = x
                        barrera.y1 = y
                