from PyQt4 import QtCore, QtGui
from pozo  import pozo
from barrera import barrera
from calitheis2 import *
from calibracion2 import *
import numpy as np
import observacion
import observacionesensayo
import bombeo
import ensayobombeo
import dominio
from parametros import parametros

class Proyecto(object):
    
    def __init__(self):        
        self.ultimoIdEns=0
        self.ultimoIdObs=0
        self.ensayos=[]
        self.observaciones=[]
        self.ensayosCopia=[]
        self.observacionesCopia=[]
        self.dominio = dominio.dominio()
        self.metodo=None

        #Lista que guardan pozo y recta
##      self.listaPozo = []
        #self.listaRecta = []

        #Ultima recta y pozo agregados
        self.idP = 0
        self.idR = 0

        #Recta candidata a ser agregada
        self.rectaCandidata = ""
        self.parametros=[]

        ##Inicial la lista de parametros
        self.cargarParametros()

        self.nix=4
        self.niy=4

        self.ti=0.0
        self.tf=0.3
        nit=10
        tfo=1.8        

    def cargarParametros(self):
        ###Si se quiere un parametro nuevo se tiene q agregar        
        self.parametros.append(parametros('S','m^2/d'))    #parametro 0
        self.parametros.append(parametros('T',''))    #parametro 1
        
    def leerParametros(self):
        for p in self.parametros:
            print p.nombre
                
    def agregarEnsayo(self, bombeos, nombre):
        self.ultimoIdEns=self.ultimoIdEns + 1
        e=ensayobombeo.ensayobombeo(bombeos, self.ultimoIdEns, nombre)
        self.ensayos.append(e)
        return e

    def restaurarEnsayo(self, e):
        self.ensayos.append(e) 

    def eliminarEnsayo(self, e):
        self.ensayos.remove(e)

    def agregarObservacion(self, observaciones, nombre):
        self.ultimoIdObs=self.ultimoIdObs + 1
        obse=observacionesensayo.observacionesensayo(observaciones, self.ultimoIdObs, nombre)
        self.observaciones.append(obse)
        return obse

    def restaurarObservacion(self, obse):
        self.observaciones.append(obse)

    def copiarObservacionesEnsayos(self):
        self.ensayosCopia=[]
        self.observacionesCopia=[]        
        for e in self.ensayos:
                self.ensayosCopia.append(e.copiaSuperficial())
        for o in self.observaciones:
                self.observacionesCopia.append(o.copiaSuperficial())

    def restaurarObservacionesEnsayos(self):
        self.ensayos=[]
        self.observaciones=[]        
        for e in self.ensayosCopia:
                self.ensayos.append(e.copiaSuperficial())
        for o in self.observacionesCopia:
                self.observaciones.append(o.copiaSuperficial())                 

    def eliminarObservaciones(self, obse):
        self.observaciones.remove(obse)

    def setearValoresDiscretizaciones(self, nix, niy, ti, tf, nit, tfo):
        self.nix=nix
        self.niy=niy
        self.ti=ti
        self.tf=tf
        self.nit=nit
        self.tfo=tfo      

    def devolverValoresDiscretizaciones(self):
        return [self.nix, self.niy, self.ti, self.tf, self.nit, self.tfo] 

    def verificarFormato(self,lista, t):
        control=True
        i=0
        print "control "
        while( i<len(lista) and control  ):
            control=t>lista[i].tiempo
            print "tiempo "+str(t)+" tiempo vector "+str(lista[i].tiempo) + " control "+str(control)
            i=i+1
        return control

    def obtenerDominio(self):
        return self.dominio
    

    #CRUD de pozos
    def agregarPozo(self, x, y):        
        p = pozo(x, y)
        self.idP = self.idP + 1
        p.id = self.idP
        self.dominio.listaPozo.append(p)
        return p.id
                

    def moverPozo(self, idElemento, x, y):
        
        for pozo in self.dominio.listaPozo:
            if pozo.id == idElemento:
                pozo.actualizarCoordenadas(x, y)
                return

    def buscarPozo(self, idElemento):
        for p in self.dominio.listaPozo:
            if p.id == int(idElemento):
                return p
         
    def removerPozo(self, idElemento):            
        for x in self.dominio.listaPozo:
            if x.id == idElemento:
                self.dominio.listaPozo.remove(x)
    def optimizacioneslistar(self):
        self.optimizaciones = QtCore.QStringList()
        
        self.optimizaciones << "CaliTheis2" << "calibracion2"
         
        return self.optimizaciones
    def optimizacioneslistarmenos(self,nolistar):
        self.opt = QtCore.QStringList()
        for x in self.optimizaciones:
            if x != nolistar:
                #print "muestro " + x
                self.opt << x
        
        return self.opt
    def asociarPozoOptimiazion(self,idElemento,metodo):
        for pozo in self.dominio.listaPozo:
            if pozo.id == idElemento:
                #en self.dominio.listaPozoOptimiza[idElemento] ahi 
                #que guardar una instancia de un objeto, cuyo tipo tiene que ser
                #determinado por el valor de metodo
                print "instancio:" + metodo
                ui = eval(str(metodo) + "()")
                ui.setpozo(pozo)
                #con el metodo getparametros obtengo la lista de parametros del metodo
                #print str(ui.getparametros())
                #for p in ui.getparametros():
                #    print p
                self.dominio.listaPozoOptimiza[idElemento]= ui
        print "se agrego a la lista de optimizaciones"

    def listarPozosParaOptimizar(self):
        return self.dominio.listaPozoOptimiza


    def retornarCoordenadas(self, idElemento):
        listaRetorno = {}
        listaRetorno["x"] = 0
        listaRetorno["y"] = 0

        for pozo in self.dominio.listaPozo:
            if pozo.id == idElemento:
                listaRetorno["x"] = pozo.x
                listaRetorno["y"] = pozo.y
                
                return listaRetorno
            
        return listaRetorno
       

    #CRUD de barreras
    def agregarRecta(self, tipo, x1, y1, x2, y2, alto, ancho):

        r = barrera(x1, x2, y1, y2, tipo, alto, ancho)



        self.idR = self.idR + 1
        r.id = self.idR
	self.dominio.listaRecta.append(r)
	return r.id

        self.dominio.listaRecta.append(r)

    def buscarRecta(self, idElemento):
        for recta in self.dominio.listaRecta:
            if recta.id == idElemento:
                return recta

    def dibujarRecta(self):
        return self.dominio.listaRecta

    def buscarPuntoEnRecta(self, x, y):

        for barrera in self.dominio.listaRecta:

            recta = QtCore.QLine(barrera.x1, barrera.y1, barrera.x2, barrera.y2)

            puntoP = QtCore.QPoint(x, y)
            puntoQ = QtCore.QPoint(recta.x1(), recta.y1())

            rectay = QtCore.QLine(puntoP, puntoQ)           

            puntoR = QtCore.QPoint(recta.x2(), recta.y2())

            rectaw = QtCore.QLine(puntoP, puntoR)           

            valor1 = np.absolute(recta.dx() /2)
            valor2 = np.absolute(recta.dy() /2)
            
            #Recta proxima a las x
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


    def buscarPuntoRecta(self, x, y, identificador):
        
        for barrera in self.dominio.listaRecta:

            if barrera.id == identificador:
                recta = QtCore.QLine(barrera.x1, barrera.y1, barrera.x2, barrera.y2)

                puntoP = QtCore.QPoint(x, y)
                puntoQ = QtCore.QPoint(recta.x1(), recta.y1())

                rectay = QtCore.QLine(puntoP, puntoQ)           

                puntoR = QtCore.QPoint(recta.x2(), recta.y2())

                rectaw = QtCore.QLine(puntoP, puntoR)           

                valor1 = np.absolute(recta.dx() /2)
                valor2 = np.absolute(recta.dy() /2)

                #Recta proxima a las x
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
	lista['eje'] = "z"
        return lista


    def actualizarRecta(self, idRecta, x, y, tipoPunto, alto, ancho):
        for barrera in self.dominio.listaRecta:
            if barrera.id == idRecta:
                if tipoPunto == "Y":
                    barrera.actualizarBarrera3(barrera.x1, x, barrera.y1, y, alto, ancho)
                else:
		    print " VALOR DE X ", x, " DE Y", y
                    barrera.actualizarBarrera3(x, barrera.x2,  y, barrera.y2, alto, ancho)
		    print " VALOR DE X ", barrera.x1, " DE Y", barrera.y1

    def actualizarRectaCoord(self, idElemento, x1, y1, x2, y2, tipo):
        for recta in self.dominio.listaRecta:
            if recta.id == idElemento:
                recta.actualizarBarrera(x1, x2, y1, y2, tipo)
                return

    def actualizarRectaCoordenada(self, idElemento, x1, y1, x2, y2):
        for recta in self.dominio.listaRecta:
            if recta.id == idElemento:
                recta.actualizarBarrera2(x1, x2, y1, y2)
                return

    def actualizarRectaC(self, idElemento, x1, y1, x2, y2, alto, ancho):
        for recta in self.dominio.listaRecta:
            if recta.id == idElemento:
                recta.actualizarBarrera3(x1, x2, y1, y2, alto, ancho)
                return

                
                
    def buscarPuntoPorQ(self, x, y):
        for Q in self.dominio.listaRecta:
            
            recta = QtCore.QLine(Q.x1, Q.y1, Q.x2, Q.y2)

            puntoP = QtCore.QPoint(x, y)

            puntoQ = QtCore.QPoint(recta.x1(), recta.y1())

            rectax = QtCore.QLine(puntoP, puntoQ)   

            #Recta proxima a las x
            if  np.absolute(rectax.dx()) < np.absolute(recta.dx() /2) and  np.absolute(rectax.dy()) < np.absolute((recta.dy() / 2)):               

                return Q.id

    def buscarPuntoPorR(self, x, y):
        for R in self.dominio.listaRecta:
            
            recta = QtCore.QLine(R.x1, R.y1, R.x2, R.y2)

            puntoP = QtCore.QPoint(x, y)

            puntoR = QtCore.QPoint(recta.x2(), recta.y2())

            rectay = QtCore.QLine(puntoP, puntoR)   

            #Recta proxima a las x
            if  np.absolute(rectay.dx()) < np.absolute(recta.dx() /2) and  np.absolute(rectay.dy()) < np.absolute((recta.dy() / 2)):
                
                return R.id

    def eliminarRecta(self, idElemento):
        for recta in self.dominio.listaRecta:
            if recta.id == idElemento:
                self.dominio.listaRecta.remove(recta)

    def agregarRectaCandidata(self, tipo, x1, y1, x2, y2, alto, ancho):
        self.rectaCandidata = barrera(x1, x2, y1, y2, tipo, alto, ancho)

    def actualizarRectaCandidata(self, x1, y1, x2, y2, alto, ancho):
		self.rectaCandidata.actualizarBarrera3(x1, x2, y1, y2, alto, ancho)


    def hayRectaCandidata(self):

        if self.rectaCandidata:
            return True

        return False

    def eliminarRectaCandidata(self):
        self.rectaCandidata = ""

    def incluirCandidata(self, signo):
        self.idR = self.idR + 1
        self.rectaCandidata.id = self.idR
	self.rectaCandidata.tipo = signo
        self.dominio.listaRecta.append(self.rectaCandidata)
        self.rectaCandidata = None
	return self.idR
