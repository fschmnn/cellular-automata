'''
The Abelian sandpile model animated

http://www.maths.bath.ac.uk/~aj276/research/sandpile.html

Rules
-----
 * We have a grid with (N,N) cells.
 * Randomly add one grain to a cell
 * If the number of grains in a cell is >=4, the cell is unstable. 
   Reduce the number of grains in this cell by 4 and add 1 grain
   to each direct neighbor. Repeat until all cells are stable.
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.image as mpimg

save = True

# should be 4*N
Nmax = 4
threshold = Nmax
N = 100
speed = 0.01
periodic = True

grid_init = (Nmax-1)*np.ones((N,N))
#grid_init *= 0
grid_init = np.random.randint(1,4,(N,N))
Ninit = np.sum(grid_init)

fixed = np.zeros((N,N))
#fixed[30,:40] = 1
#fixed[30,43:57] = 1
#fixed[30,60:] = 1
#fixed[49:50,49:50] = 1
#fixed[47:52,47:52] = 1

#grid_init[50,50] = Nmax

def sandpile(grid,threshold,periodic=False):
    '''Calculate the next grid'''

    if np.max(grid)<threshold:
        i,j = np.random.randint(0,N,2)
        grid[i,j] += 1
        return grid
    else:
        tmp = np.zeros((N,N))
        tmp[:,:] = grid[:,:]
        tmp[1:,:][grid[:-1,:]>=threshold] += 1
        tmp[:-1,:][grid[1:,:]>=threshold] += 1
        tmp[:,1:][grid[:,:-1]>=threshold] += 1
        tmp[:,:-1][grid[:,1:]>=threshold] += 1
        tmp[grid>=threshold] -= 4
        
        if periodic:
            # periodic conditions
            tmp[0,1:-1][grid[-1,1:-1]>=threshold] += 1
            tmp[-1,1:-1][grid[0,1:-1]>=threshold] += 1
            tmp[:,0][grid[:,-1]>=threshold] += 1
            tmp[:,-1][grid[:,0]>=threshold] += 1

        tmp[fixed==1] = 0

        return tmp[:,:]

fig = plt.figure(figsize=(15,15))
ax = plt.axes()
plt.axis('off')
timetext = ax.text(2,4,'',fontsize=20)
cmap = plt.get_cmap('RdYlBu_r', Nmax+2)
im=plt.imshow(grid_init,cmap=cmap,vmin=-0.5,vmax=Nmax+1.5)
cax = plt.colorbar(ticks=np.arange(0,Nmax+2))

def init():
    im.set_data(grid_init)
    timetext.set_text('i hate sand')
    return im, timetext

def animate(i):
    global threshold

    if ((i+1) % 200==0) and (threshold>=5):
        threshold -= 1 

    grid=im.get_array()
    for j in range(30):
        grid = sandpile(grid,threshold,periodic=True)

    im.set_array(grid)
    timetext.set_text('{:.1f} %, t={}'.format(100-np.sum(grid)/Ninit*100,threshold))
    return im, timetext

animation = FuncAnimation(fig, animate, init_func=init,interval=1e3*speed,blit=True)
if save: animation.save('animations/sandpile.gif', writer="ffmpeg")
plt.show()
