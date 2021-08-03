#!/usr/bin/python

import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import numpy as np


def explode(data):
    size = np.array(data.shape)*2
    data_e = np.zeros(size - 1, dtype=data.dtype)
    data_e[::2, ::2, ::2] = data
                   
    return data_e

colors = [
    '#00FF00',
    '#0000FF',
    '#FF7F00',
    '#7F4000',
    '#00FF7F',
    '#FFFF00',
    '#7F7F7F',
    '#FF00FF',
    '#FF0000',
    '#7F00FF',
    '#007FFF',
    '#00FFFF',
    '#FFFFFF',
]

solutions = []

with open('solutions_cube', 'r') as f:
    x = 0
    solution = np.zeros((4, 4, 4), dtype='U10')
    for line in f: 
        if x == 4:
            x = 0
            solutions.append(solution)
            solution = np.zeros((4, 4, 4), dtype='U10')
        else:
            data = line.split()
            for z in range(4): 
                for y in range(4): 
                    solution[x,y,z] = colors[int(data[z * 4 + y]) - 1]
            x += 1
    
class UserInterface:
    def __init__(self):
        self.ind = 0
        self.ax = plt.figure().add_subplot(projection='3d')
        
        self.slider = Slider(plt.axes([0.05, 0.05, 0.9, 0.075]), None, 0, len(solutions) - 1, valstep=1)
        self.slider.on_changed(self.change)

        self.bnext = Button(plt.axes([0.85, 0.15, 0.1, 0.075]), 'Next')
        self.bnext.on_clicked(self.next)
        self.bprev = Button(plt.axes([0.05, 0.15, 0.1, 0.075]), 'Previous')
        self.bprev.on_clicked(self.prev)
        
        self.showSolution()
        
    def next(self, event):
        if self.ind < len(solutions) - 1:
            self.ind += 1
            self.slider.set_val(self.ind)
            self.showSolution()
        
    def prev(self, event):
        if self.ind > 0:
            self.ind -= 1
            self.slider.set_val(self.ind)
            self.showSolution()
        
    def change(self, value):
        self.ind = value
            
        self.showSolution()
        
    def showSolution(self):
        solution = solutions[self.ind]
        filled = np.ones(solution.shape)

        # upscale the above voxel image, leaving gaps
        filled_2 = explode(filled)
        fcolors_2 = explode(solution)
        ecolors_2 = explode(solution)


        for x in range(4): 
            for y in range(4): 
                for z in range(4): 
                    if x < 3 and fcolors_2[2*x,2*y,2*z] == fcolors_2[2*x + 2,2*y,2*z]:
                        filled_2[2*x + 1,2*y,2*z] = filled_2[2*x,2*y,2*z]
                        fcolors_2[2*x + 1,2*y,2*z] = fcolors_2[2*x,2*y,2*z] + '55'
                        ecolors_2[2*x + 1,2*y,2*z] = ecolors_2[2*x,2*y,2*z]
                    if y < 3 and fcolors_2[2*x,2*y,2*z] == fcolors_2[2*x,2*y + 2,2*z]:
                        filled_2[2*x,2*y + 1,2*z] = filled_2[2*x,2*y,2*z]
                        fcolors_2[2*x,2*y + 1,2*z] = fcolors_2[2*x,2*y,2*z] + '55'
                        ecolors_2[2*x,2*y + 1,2*z] = ecolors_2[2*x,2*y,2*z]
                    if z < 3 and fcolors_2[2*x,2*y,2*z] == fcolors_2[2*x,2*y,2*z + 2]:
                        filled_2[2*x,2*y,2*z + 1] = filled_2[2*x,2*y,2*z]
                        fcolors_2[2*x,2*y,2*z + 1] = fcolors_2[2*x,2*y,2*z] + '55'
                        ecolors_2[2*x,2*y,2*z + 1] = ecolors_2[2*x,2*y,2*z]

        # Shrink the gaps
        x, y, z = np.indices(np.array(filled_2.shape) + 1).astype(float) // 2
        space = 0.3
        x[0::2, :, :] += space
        y[:, 0::2, :] += space
        z[:, :, 0::2] += space
        x[1::2, :, :] += 1 - space
        y[:, 1::2, :] += 1 - space
        z[:, :, 1::2] += 1 - space

        self.ax.clear()
        self.ax.voxels(x, y, z, filled_2, facecolors=fcolors_2, edgecolors=ecolors_2)
        plt.draw()

ui = UserInterface()

plt.show()
