"""
	tiponpython Simulacion de ensayos de acuiferos
	Copyright 2012 Andres Pias, Jesus Guibert
	
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
"""

import sys
sys.path.append("views")
sys.path.append("models")

import metodoSolucion
from scipy.special import kn,expn
import numpy as np
import controlador
import scipy

class DiferenciaFinita(metodoSolucion.metodoNumerico):

    def __init__(self, dominio, parametros, asociar=None):
        
        ##Lista de cardinales de los parametros que utiliza el metodo
        ##Parametros 0: S, parametro 1:T, parametro 2:c
        self.paramcard=[0,1]
        #### Llamar al constructor del metodo de solucion
        ## probar llamar al metodo padre        
        metodoSolucion.metodoNumerico.__init__(self,dominio,parametros, asociar)
        #print 'Se creo el loco hantush'
        ##Hasntush que no acepta barrera        
        self.aceptaBarrera=False       
        self.optimizaciones=['']

    def calcular(self,tiempos, ti, tf,dt, nix, niy, x,y, X, Y):
        acuiT=float(self.listaParametros[0].valoresParametro.valor)
        acuiS=float(self.listaParametros[1].valoresParametro.valor)
        m=nix
        n=niy
        l=n*m
        i=range(m)
        j=range(n)
        self.d=self.dominio
        lx=self.d.ancho
        ly=self.d.alto
        A=np.identity(len(i)*len(j), float)

        if self.aceptaBarrera==True:
            Todoslospbombeo=self.d.obtenerPBombeoYVirtuales()            
        else:
            Todoslospbombeo=self.d.obtenerPozosdeBombeo()
        Np=len(Todoslospbombeo)
        Q=[]
        xps=[]
        yps=[]
        for p in Todoslospbombeo:
            for b in p.ensayos[0].devolverBProc():
                Q=np.concatenate((Q,[b.caudal]))
            #ingresamos los valores del pozo
            xps.append(p.x)
            yps.append(p.y)
            
        #creando los intervalos
        #Ax=np.zeros(1,m-1);
        Ax=np.zeros((m-1),float)
        #for j=1:m-1;

        #print "m ", m
        #print "x56 ",x[56]
        for j in range(m-1):
            #print "j-",j
            Ax[j]=x[j+1]-x[j]

        Ay=np.zeros((n-1),float)
        for i in range(n-1):
            Ay[i]=y[i+1]-y[i]

        #creando la matriz de transmisividad
        T=np.ones((len(x)*len(y)),float)*acuiT

        #creando matriz de niveles incial
        h0=np.zeros((niy,nix),float)
        for i in range(nix):
            for j in range(niy):
                #print "xi",x[i], "yj ", y[j]
                #dominio.H0a*x(i) +dominio.H0b*y(j) + dominio.H0c;
                h0[j,i]=self.d.calcularH0(x[i], y[j])

        #Para el elemento 1,1
        ##Aca jess donde tenes que tirar lineas a bocha!
        A1=np.zeros((l),float)
        A1[0]=-1/Ax[0]*(2*(T[0]*T[n]/(T[0]+T[n])))-1/Ay[0]*(2*(T[0]*T[1]/(T[0]+T[1])))
        A1[1]=1/Ay[n-2]*(2*(T[0]*T[1]/(T[0]+T[1])))        
        A1[n]=1/Ax[m-2]*(2*(T[0]*T[n]/(T[0]+T[n])))
        A[0,0:l]=A1

        #Para el elemento n,1
        An=np.zeros((l),float)
        An[n-1]=-1/Ax[0]*(2*(T[n-1]*T[n+n-1]/(T[n-1]+T[n+n-1])))-1/Ay[0]*(2*(T[n-1]*T[n-2]/(T[n-1]+T[n-2])))
        An[n-2]=1/Ay[0]*(2*(T[n-1]*T[n-2]/(T[n-1]+T[n-2])))
        An[n+n-1]=1/Ax[0]*(2*(T[n-1]*T[n+n-1]/(T[n-1]+T[n+n-1])))
        A[n-1,0:l]=An

        #Para los elementos comprendidos entre 1,2 y 1,m-1     
        for k in range(1,m-1):
            A[k*n,k*n]=-1/Ay[n-2]*(2*(T[k*n]*T[k*n+1]/(T[k*n]+T[k*n+1])))
            A[k*n,k*n+1]=1/Ay[n-2]*(2*(T[k*n]*T[k*n+1]/(T[k*n]+T[k*n+1])))

        #Para el elemento 1,m
        Am=np.zeros((l),float)
        Am[l-n]=-1/Ax[m-2]*(2*(T[l-2*n]*T[l-n]/(T[l-2*n]+T[l-n])))-1/Ay[n-2]*(2*(T[l-n+1]*T[l-n]/(T[l-n+1]+T[l-n])))
        Am[l-2*n]=1/Ax[m-2]*(2*(T[l-2*n]*T[l-n]/(T[l-2*n]+T[l-n])))
        Am[l-n+1]=1/Ay[n-2]*(2*(T[l-n+1]*T[l-n]/(T[l-n+1]+T[l-n])))
        A[l-n,0:l]=Am

        #Para los elementos comprendidos entre 2,m y n-1,m 
        for k in range(n-2):
            A[l-n+1+k,l-n+1+k]=-1/Ax[m-2]*(2*(T[l-n+1+k]*T[l-2*n+1+k]/(T[l-n+1+k]+T[l-2*n+1+k])))
            A[l-n+1+k,l-2*n+1+k]=1/Ax[m-2]*(2*(T[l-n+1+k]*T[l-2*n+1+k]/(T[l-n+1+k]+T[l-2*n+1+k])))

        #Para el elemento n,m
        Anm=np.zeros((l),float)
        Anm[l-1]=-1/Ax[m-2]*(2*(T[l-1]*T[l-n-1]/(T[l-1]+T[l-n-1])))-1/Ay[0]*(2*(T[l-1]*T[l-2]/(T[l-1]+T[l-2])))
        Anm[l-2]=1/Ay[0]*(2*(T[l-1]*T[l-2]/(T[l-1]+T[l-2])))
        Anm[l-n-1]=1/Ax[m-2]*(2*(T[l-1]*T[l-n-1]/(T[l-1]+T[l-n-1])))
        A[l-1,0:l]=Anm

        #Para los elementos comprendidos entre 2,1 y n-1,1 
        for k in range(n-2):
            A[k+1,k+1]=-1/Ax[0]*(2*(T[k+1]*T[k+n+1]/(T[k+1]+T[k+n+1])))
            A[k+1,k+n+1]=1/Ax[0]*(2*(T[k+1]*T[k+n+1]/(T[k+1]+T[k+n+1])))

        #Para los elementos comprendidos entre n,2 y n,m-1 
        for k in range(1,m-1):
            A[(1+k)*n-1,(1+k)*n-1]=-1/Ay[0]*(2*(T[(1+k)*n-1]*T[(1+k)*n-2])/(T[(1+k)*n-1]+T[(1+k)*n-2]))
            A[(1+k)*n-1,(1+k)*n-2]=1/Ay[0]*(2*(T[(1+k)*n-1]*T[(1+k)*n-2])/(T[(1+k)*n-1]+T[(1+k)*n-2]))

        #Para los elementos comprendidos entre 2,2 y n-1,m-1 
        for i in range(1,m-1):
            for j in range(n-2):
                A[(i)*n+1+j,(i)*n+1+j]=-1/Ax[i-1]*2/(Ax[i-1]+Ax[i])*(2*(T[(i)*n+1+j]*T[(i)*n+1+j-n]/(T[(i)*n+1+j]+T[(i)*n+1+j-n])))-(1/Ax[i])*2/(Ax[i-1]+Ax[i])*(2*(T[(i)*n+1+j]*T[(i)*n+1+j+n]/(T[(i)*n+1+j]+T[(i)*n+1+j+n])))+(-1/Ay[n-j-2])*2/(Ay[n-j-2]+Ay[n-j-1-2])*(2*(T[(i)*n+1+j]*T[(i)*n+j]/(T[(i)*n+1+j]+T[(i)*n+j])))-(1/Ay[n-j-1-2])*2/(Ay[n-j-2]+Ay[n-j-1-2])*(2*(T[(i)*n+1+j]*T[(i)*n+2+j]/(T[(i)*n+1+j]+T[(i)*n+2+j])))
                A[(i)*n+1+j,(i)*n+2+j]=(1/Ay[n-j-1-2])*2/(Ay[n-j-2]+Ay[n-j-1-2])*(2*(T[(i)*n+1+j]*T[(i)*n+2+j]/(T[(i)*n+1+j]+T[(i)*n+2+j])))
                #hasta ak revision
                #A((i)*n+1+j,(i)*n+j)=(1/Ay(n-j))*2/(Ay(n-j)+Ay(n-j-1))*(2*(T((i)*n+1+j)*T((i)*n+j)/(T((i)*n+1+j)+T((i)*n+j))));
                A[(i)*n+1+j,(i)*n+j]=(1/Ay[n-j-2])*2/(Ay[n-j-2]+Ay[n-j-1-2])*(2*(T[(i)*n+1+j]*T[(i)*n+j]/(T[(i)*n+1+j]+T[(i)*n+j])))
                #A((i)*n+1+j,(i)*n+1+j-n)=(1/Ax(i))*2/(Ax(i)+Ax(i+1))*(2*(T((i)*n+1+j)*T((i)*n+1+j-n)/(T((i)*n+1+j)+T((i)*n+1+j-n))));
                A[(i)*n+1+j,(i)*n+1+j-n]=(1/Ax[i-1])*2/(Ax[i-1]+Ax[i])*(2*(T[(i)*n+1+j]*T[(i)*n+1+j-n]/(T[(i)*n+1+j]+T[(i)*n+1+j-n])))
                #A((i)*n+1+j,(i)*n+1+j+n)=(1/Ax(i+1))*2/(Ax(i)+Ax(i+1))*(2*(T((i)*n+1+j)*T((i)*n+1+j+n)/(T((i)*n+1+j)+T((i)*n+1+j+n))));                
                A[(i)*n+1+j,(i)*n+1+j+n]=(1/Ax[i])*2/(Ax[i-1]+Ax[i])*(2*(T[(i)*n+1+j]*T[(i)*n+1+j+n]/(T[(i)*n+1+j]+T[(i)*n+1+j+n])))


        print('Calculando, espere...')
        #Generamos el termino independiente
        #Creando matriz de almacenamiento

        S=np.identity(l,float)*acuiS

        #calculando decensos funcion del tiempo
        x1=np.zeros((l,l),float)
        At=dt
        h=np.ones((l),float)*10
        for i in range(m):
            h[n*i:n+n*i]=h0[0:n,i]

        tetha=0.66
        E=A*tetha-S/(At)

        #Para los elementos conocidos
        #for k=[1:n:l-n+1]; 
        for k in range(0,l-n+1,n):  #arriba
            E[k,0:l]=np.zeros((1,l),float)
            E[k,k]=1
            
        for k in range(l-n,l):    #derecha
            E[k,0:l]=np.zeros((1,l),float)
            E[k,k]=1

        #[1,n:n:l]
        for k in np.concatenate(([0],range(n-1,l,n))):  #abajo
            E[k,0:l]=np.zeros((1,l),float)
            E[k,k]=1

        for k in range(n):        #izq
            E[k,0:l]=np.zeros((1,l),float)
            E[k,k]=1
            
        B=np.linalg.inv(E)
        x2=np.zeros((len(tiempos),l),float)
        for t1 in range(len(tiempos)):            
            #b(1:l)=0
            b=np.zeros((l),float) 
            for i in range(Np):       
                xp=xps[i]
                yp=yps[i]
                b2=self.generab(lx,ly,Ax,Ay,n,m,xp,yp,l,x,y)
                Qt=Q[i]
                #if t1==0:
                    #for w in range(1621, 1630):
                        #print 'pos ',w,'bw ',b2[w]                
                #print "b2 ", b2,'-Qt-',Qt
                #print '-Qt-',Qt                
                b=b+b2*Qt

            #print 'b--',b                
                #for w in range(1621, 1630):
                    #print 'pos ',w,'bw ',b[w]
               
            b1=np.dot((A*(tetha-1)-S/(At)),h)+b

            #if t1==0:
                #aux1=(A*(tetha-1)-S/(At))
                #aux2=np.dot(aux1,h)
                #aux3=aux2+b
                

            #if t1==0:
            #    print "b1 ", b1, "A ", A            

            #print "b1 ", b1[0:l-n+1:n],"- h0 -", h0[0,0:m]                
            #g(1:2:6) -> g[0:6:2]
            b1[0:l-n+1:n]=h0[0,0:m]   #arriba            
            b1[l-n:l]=h0[0:n,m-1]     #derecha
            b1[n-1:l:n]=h0[n-1,0:m]   #abajo
            b1[0:n]=h0[0:n,0]         #izq

            h=np.dot(B,b1)
            x2[t1,0:l]=h



        """print 'Asi quedo aux1'
        for i in range(m):
            for j in range(n):
                if aux1[j,i]!=0:
                   print 'j ',j,'i ',i,'aux1[w]::',aux1[j,i]

        print 'Asi quedo aux2' 
        for w in range (len(aux2)):
            if aux2[w]!=0:
                print "indice::",w,"aux2[w]::",aux2[w]

        print 'Asi quedo aux3' 
        for w in range (len(aux3)):
            if aux3[w]!=0:
                print "indice::",w,"aux3[w]::",aux3[w]"""                
                   

        #print "A[0,0] ",A[0,0]

        #print "A", A
        #print 'Asi quedo S '
        #print S

        #print 'Asi quedo S ', S
        
        #print 'tetha ',tetha
        #print 'At ',At

        ##Esto va a lo ultimo de todo y esta en otros scripts de Matlab

        ##Obtener todos los pozos de observacion
        TodoslospozosObservacion=self.d.obtenerPozosdeObservacion()
        ##Se instancias de una para todos los tiempos una lista de Observaciones solucionadas para cada pozo de observacion
        for pozoObservacion in TodoslospozosObservacion:
            pozoObservacion.instanciarSolucionadas(self.d.calcularH0(pozoObservacion.x, pozoObservacion.y), tiempos)

            xo=pozoObservacion.x
            yo=pozoObservacion.y
            pb=np.zeros((2,2),float)
            for j in range(m):
                if xo<x[j]:
                    pb[0,0]=x[j-1]
                    pb[0,1]=x[j]
                    break
            for i in range(n):
                if yo<y[i]:
                    pb[1,0]=y[i-1]
                    pb[1,1]=y[i]
                    break
            io=i
            jo=j
            
        self.matrizDescenso=np.zeros((len(tiempos),n,m), float)
        self.gyh=np.zeros((len(tiempos),n,m), float)
        self.gxh=np.zeros((len(tiempos),n,m), float)       
        
        for i in range(len(tiempos)):
            #de 0 a l-1 igual que matlab de 1 a l
            x1=x2[i,0:l];
            for k in range(n):
                #hr(k+1,1:m)=x1(k+1:n:l-n+k+1);
                #g(1:2:6) -> g[0:6:2]
                self.matrizDescenso[i,k,0:m]=x1[k:l-n+k+1:n]                
                #[gxh(:,:,i),gyh(:,:,i)] = gradient(-hr(:,:),Ax(1),Ay(1));
                [self.gyh[i,:,:],self.gxh[i,:,:]] = np.gradient(-self.matrizDescenso[i,:,:],Ax[0],Ay[0])

                for j in range(m):
                    if self.matrizDescenso[i,k,j]>self.max:
                        self.max=self.matrizDescenso[i,k,j]
                    if self.matrizDescenso[i,k,j]<self.min:
                        self.min=self.matrizDescenso[i,k,j]

            #Calculo para todos los pozos de observacion
            for pozoObservacion in TodoslospozosObservacion:
                hs1=x1[io+n*(jo)]
                aa=io+n*(jo)
                #print aa
                #hs2=x1(io+n*(jo-1)-1);
                hs2=x1[io+n*(jo)-1]
                aa=(io+n*(jo)-1)
                #print aa
                hs3=x1[io+n*(jo-1)]
                aa=io+n*(jo-1)
                #print aa
                hs4=x1[io+n*(jo-1)-1]
                aa=(io+n*(jo-1)-1)
                #print aa
                #hsm(i,t)=(hs1+hs2+hs3+hs4)/4                
                #Se actualizan solo las observaciones solucionadas
                pozoObservacion.obssolucionadas[i]=(hs1+hs2+hs3+hs4)/4

                #print 'tiempo::',i,'-hsm::', pozoObservacion.obssolucionadas[i]

        return self.matrizDescenso

    def generab(self,lx,ly,Ax,Ay,n,m,xp,yp,l,x,y):
        
        #print "lx ",lx,"ly ",ly,"n ",n,"m ",m,"xp ",xp,"yp ",yp,"l ",l,"x ",x,"y ",y
        #print "Ax ",Ax,"Ay ",Ay
        
        #b2(1:l)=0;
        b2=np.zeros((l),float)          
        pb=np.zeros((2,2),float)
        for j in range(m):
            if  xp<x[j]:
                pb[0,0]=x[j-1]
                pb[0,1]=x[j]
                break
            
        for i in range(n):
            if yp<y[i]:
                pb[1,0]=y[i-1]
                pb[1,1]=y[i]
                break

        #Luego las distancias a los nodos:
        d1=self.distancia(xp,yp,pb[0,1],pb[1,1])
        d2=self.distancia(xp,yp,pb[0,0],pb[1,1])
        d3=self.distancia(xp,yp,pb[0,1],pb[1,0])
        d4=self.distancia(xp,yp,pb[0,0],pb[1,0])
        d=[d1,d2,d3,d4]

        ff=np.zeros((4),float)
        for k in range(4):
            if d[k]<min(Ax)/100 or d[k]<min(Ay)/100:
                ff=np.zeros((4),float)
                ff[k]=1
                break
            else:
                ff[0]=(1/d1)/(1/d1+1/d2+1/d3+1/d4)
                ff[1]=(1/d2)/(1/d1+1/d2+1/d3+1/d4)
                ff[2]=(1/d3)/(1/d1+1/d2+1/d3+1/d4)
                ff[3]=(1/d4)/(1/d1+1/d2+1/d3+1/d4)

        b2[i+n*(j)]=ff[0]/((pb[0,1]-pb[0,0])*(pb[1,1]-pb[1,0]))
        #print 'indice ',i+n*(j)
        b2[i+n*(j)-1]=ff[1]/((pb[0,1]-pb[0,0])*(pb[1,1]-pb[1,0]))
        b2[i+n*(j-1)]=ff[2]/((pb[0,1]-pb[0,0])*(pb[1,1]-pb[1,0]))
        b2[i+n*(j-1)-1]=ff[3]/((pb[0,1]-pb[0,0])*(pb[1,1]-pb[1,0]))

        return b2
    

    def distancia(self, x1,y1,x2,y2 ):
        
        d=np.sqrt(np.square(x1-x2) + np.square(y1-y2))
        return d
           

if __name__ == "__main__":
    cont=1
    ui = Hantush(cont,1)
    s=ui.calcularpozoGenerico(1,0.2,500,1000,0.0001,600)
    print s

    


