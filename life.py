import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.image as mpimg
from scipy.signal import convolve2d

'''
Conway's Game of Life

1. Any live cell with fewer than two live neighbors dies, as if by under population.
2. Any live cell with two or three live neighbors lives on to the next generation.
3. Any live cell with more than three live neighbors dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

'''

dim = (40,40)
speed = 0.3
UseImage = True
save = False

if UseImage:
    grid_init = mpimg.imread('img.png')
    grid_init[grid_init<1]=0
    grid_init = (grid_init+1) % 2
    dim = np.shape(grid_init)
else:
    grid_init = np.random.randint(0,2,dim)

def life(grid):
    # sum up cells to the left and right
    h_neighbors = np.copy(grid)
    h_neighbors[:,:-1] += grid[:,1:] 
    h_neighbors[:,1:]  += grid[:,:-1]

    # sum up the three cells on top and bottom
    neighbors = h_neighbors - grid
    neighbors[:-1,:] += h_neighbors[1:,:] 
    neighbors[1:,:]  += h_neighbors[:-1,:]

    # neighbors contains the number of neighbors
    new_grid = np.copy(grid)
    new_grid[(grid==1) & (neighbors>3)]  = 0
    new_grid[(grid==1) & (neighbors<2)]  = 0 
    new_grid[(grid==0) & (neighbors==3)] = 1 
    
    return new_grid

# convolve not yet working
def life2(grid):
    neighbors = convolve2d(grid,np.ones((3,3)),mode='same')-grid
    new_grid = np.copy(grid)
    new_grid[(grid==1) & (neighbors>3)]  = 0
    new_grid[(grid==1) & (neighbors<2)]  = 0 
    new_grid[(grid==0) & (neighbors==3)] = 1 

    return new_grid


fig = plt.figure(figsize=(12/max(dim)*dim[0],12/max(dim)*dim[1]))
plt.axis('off')
im=plt.imshow(grid_init,cmap='binary_r')

def init():
    im.set_data(grid_init)
    return [im]

def animate(i):
    grid=im.get_array()
    # maybe try grid[:,:,0]
    im.set_array(life(grid))
    return [im]

animation = FuncAnimation(fig, animate, init_func=init,interval=1e3*speed,blit=True)
if save: animation.save('life.mp4', writer="ffmpeg")
plt.show()
