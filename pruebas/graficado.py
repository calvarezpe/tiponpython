import sys
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.axes3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pylab as p
import mpl_toolkits.mplot3d.axes3d as p3


nix=5
niy=10;

nix=nix+1;
niy=niy+1;

xx = np.linspace(0,5,nix);
yy = np.linspace(10,0,niy);
X, Y = np.meshgrid(xx, yy) 

print xx
print yy


h0=np.zeros((niy,nix), float);


print h0

for i in range(0,nix):
    for j in range (0,niy):
        #la matriz a generar se indexa primero en el eje y y dps en el x
        h0[j,i]=yy[j];

fig=p.figure()
#fig = plt.figure()

ax = p3.Axes3D(fig)

#ax.plot_surface(x,y,z)
surf = ax.plot_surface(X, Y, h0)
ax.contour(X,Y,h0)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
p.show()

#ax = fig.add_subplot(111, projection='3d')


#ax.show()


    


