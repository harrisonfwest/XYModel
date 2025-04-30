"""
Created on Sun Apr 20, 2025 @ 4:09 pm
@author: Harrison West, Renn Summersgill
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import display

class lattice():
    def __init__(self, temperature = .01, width = 64, external_field = 0.0):
        self.width = width
        self.size = self.width * self.width
        self.h = external_field
        L, N = self.width, self.size
        self.neighbors = {i : ((i//L)*L + (i+1)%L, (i+L)%N, (i//L)*L + (i-1)%L, (i-L)%N) for i in list(range(N))}
        self.spins = np.random.uniform(0, 2*np.pi, self.size)
        self.temperature = temperature
        self.fig = plt.figure()
        self.im = plt.imshow(self.spins.reshape(self.width, self.width), cmap = 'twilight_shifted',
                             vmin = 0, vmax = 2*np.pi)
        plt.colorbar(ticks=[0, np.pi, 2*np.pi]).ax.set_yticklabels([0, '$\pi$', '2$\pi$'])
        plt.axis('off')

    def poke(self): # tries a random new spin for each lattice site, in a random order of sites
        beta = 1 / self.temperature
        sites = list(range(len(self.spins)))
        np.random.shuffle(sites)
        for site in sites:
            oldEnergy = -sum(np.cos(self.spins[site] - self.spins[n]) for n in self.neighbors[site]) - (self.h * np.cos(self.spins[site]))
            newSpin = self.spins[site] + np.random.uniform(-np.pi, np.pi)
            if newSpin >= 2*np.pi:
                newSpin -= 2*np.pi
            newEnergy = -sum(np.cos(newSpin - self.spins[n]) for n in self.neighbors[site]) - (self.h * np.cos(self.spins[site]))
            if newEnergy <= oldEnergy or np.random.rand() < np.exp(-(newEnergy - oldEnergy) * beta):
                self.spins[site] = newSpin

    def get_energy(self):
        energy = np.zeros(np.shape(self.spins))
        for site in range(len(self.spins)):
            energy[site] = -sum(np.cos(self.spins[site] - self.spins[n]) for n in self.neighbors[site]) \
                           - self.h * np.cos(self.spins[site])
        return energy

    '''
    def animate(self):
        grid = self.spins.reshape(self.width, self.width)
        self.im = plt.imshow(grid, cmap = 'twilight_shifted', vmin = -np.pi, vmax = +np.pi)
    '''

    def animate(self, frame):
        for _ in range(15):
            self.poke()
        grid = self.spins.reshape(self.width, self.width)
        self.im.set_data(grid)
        return self.im

    def make_animation(self, prepend = 'lattice'):
        anim = animation.FuncAnimation(self.fig, self.animate)

        # video = anim.to_html5_video()
        #
        # # embedding for the video
        # html = display.HTML(video)
        #
        # # draw the animation
        # display.display(html)

        name = prepend + '.gif'
        count = 0
        while os.path.exists(name):
            count += 1
            name = prepend + str(count) + '.gif'

        anim.save(name)

        return

    def show(self):
        grid = self.spins.reshape(self.width, self.width)
        plt.imshow(grid, cmap = 'twilight_shifted', vmin = 0, vmax = 2*np.pi)
        # plt.colorbar(ticks=[-np.pi + .1, 0, np.pi - .1]).ax.set_yticklabels(['-$\pi$', 0, '$\pi$'])
        plt.axis('off')
        plt.show()

sample = lattice(width = 512)
sample.make_animation()
# sample.make_animation(prepend = 'lattice')