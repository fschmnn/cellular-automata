import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.image as mpimg

'''
The Abelian sandpile model

http://www.maths.bath.ac.uk/~aj276/research/sandpile.html

'''

# should be 4*N
Nmax = 8
threshold = Nmax
N = 100
speed = 0.01
UseImage = True
save = False

grid_init = (Nmax-1)*np.ones((N,N))
Ninit = np.sum(grid_init)

fixed = np.zeros((N,N))
#fixed[30,:40] = 1
#fixed[30,43:57] = 1
#fixed[30,60:] = 1

grid_init[50,50] = Nmax

def sandpile(grid,threshold):
    if np.max(grid)<threshold:
        return grid
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
    for j in range(1):
        grid = sandpile(grid,threshold)

    im.set_array(grid)
    timetext.set_text('{:.1f} %, t={}'.format(100-np.sum(grid)/Ninit*100,threshold))
    return im, timetext

animation = FuncAnimation(fig, animate, init_func=init,interval=1e3*speed,blit=True)
plt.show()
