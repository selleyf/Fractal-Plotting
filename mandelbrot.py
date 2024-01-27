#######################
### Fractal plotter ###
#######################

## Plot the Mandelbrot/Burning ship fractal
## Call fractal_png(x, y, width, height, gridsize) for a view of the fractal with
## - center x + i*y
## - a png image of size (2*width + 1) X (2*height + 1)
## - with a distance of 'gridsize' of two pixels on the complex plain

import matplotlib as mpl
import cv2
import numpy as np
import os
import imageio

FRACTAL = 'burning_ship'

MAX_ITER = 60

# Create colormap
# See https://matplotlib.org/stable/users/explain/colors/colormaps.html for more choices
cmap = mpl.colormaps['turbo']._resample(MAX_ITER)
temp_colormap = cmap(range(MAX_ITER)).tolist()
COLORMAP = [[color[0]*255, color[1]*255, color[2]*255] for color in temp_colormap]

def escape_time_pixel(x, y):
# Assign color to pixel based on escape time
    c = complex(x,y)
    z = complex(0,0)
    escape_time = MAX_ITER

    for i in range(MAX_ITER + 1):
        if abs(z) >= 2:
            if i == 0:
                escape_time = 0
                break
            else:
                escape_time = i-1
                break
        else:
            #z = z**2 + c # uncomment for the Mandelbrot set
            z = (complex(abs(z.real), abs(z.imag)))**2 + c # uncomment for the Burning ship fractal

    if escape_time == MAX_ITER:
        return [0, 0, 0]
    else:
        return COLORMAP[escape_time]

    
def create_grid(x, y, width, height, gridsize):
# Create the following discretization of a square in the complex plane:
# - center: x+i*y
# - 2*width + 1 pixels in the real dimension, 2*height + 1 pixels in the imaginary dimension
# - distance of two pixels is 'gridsize' on the complex plane
    real_parts = []
    for n in range(-width, width+1):
        real_parts.append(x + n*gridsize)
    imaginary_parts = []
    for m in range(height, -height-1, -1):
        imaginary_parts.append(y + m*gridsize)
    gridpoints = [[]]
    s = 0
    for imag in imaginary_parts:
        for real in real_parts:
            gridpoints[s].append(complex(real, imag))
        gridpoints.append([])
        s +=1
    return gridpoints[:-1]

def fractal_png(x, y, width, height, stepsize, iter = ''):
    grid = create_grid(x, y, width, height, stepsize)
    fr_png = []
    for m in range(len(grid)-1,-1,-1):
        fr_png_current_row = []
        for n in range(len(grid[m])):
            fr_png_current_row.append(escape_time_pixel(grid[m][n].real, grid[m][n].imag))
        fr_png.append(fr_png_current_row)
    arr = np.array(fr_png)
    path = './zoom_small' # define where to save the image
    cv2.imwrite(os.path.join(path , f'{FRACTAL}_{x}_{y}_{width}_{height}{iter}.png'), arr)


####################
## Example calls: ##
####################
#fractal_png(-0.5, -0.5, 1800, 1300, 1e-3) --for Burning ship--
#fractal_png(-0.8, 0, 1400, 1300, 1e-3) --for Mandelbrot--


###############################
### Create fractal zoom gif ###
###############################

centerX = -1.7618998999
centerY =  -0.02799
dimension = 500
timesteps = 500

iter = 0
for j in np.logspace(-4, -8, timesteps):
    fractal_png(centerX, centerY, dimension, dimension, j, '_' + str(iter))
    iter += 1

file_paths=[f'./zoom_small/{FRACTAL}_{centerX}_{centerY}_{dimension}_{dimension}_{i}.png' for i in range(timesteps)]
images = []
for path in file_paths:
    images.append(imageio.v2.imread(path))
imageio.mimsave(f'{FRACTAL}_{centerX}_{centerY}_{dimension}_{dimension}.gif', images, fps = 10)

