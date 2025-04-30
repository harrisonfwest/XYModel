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
        # Neighbors in order:               Right,  Bottom,               Left,      Up
        self.neighbors = {i : ((i//L)*L + (i+1)%L, (i+L)%N, (i//L)*L + (i-1)%L, (i-L)%N) for i in list(range(N))}
        self.spins = np.random.uniform(0, 2*np.pi, self.size)
        self.temperature = temperature
        self.energy = np.sum(self.get_energy())/N  # Energy per spin is total energy / number of spins
        self.fig = plt.figure()
        self.im = plt.imshow(self.spins.reshape(self.width, self.width), cmap = 'twilight_shifted',
                             vmin = 0, vmax = 2*np.pi)

    def poke(self): # tries a random new spin for each lattice site, in a random order of sites
        beta = 1 / self.temperature
        sites = list(range(len(self.spins)))
        np.random.shuffle(sites)
        for site in sites: # site is an index in the lattice; Check each one
            oldEnergy = -sum(np.cos(self.spins[site] - self.spins[n]) for n in self.neighbors[site]) \
                        - (self.h * np.cos(self.spins[site]))
            newSpin = self.spins[site] + np.random.uniform(0, 2*np.pi)
            if newSpin >= 2*np.pi:
                newSpin -= 2*np.pi
            newEnergy = -sum(np.cos(newSpin - self.spins[n]) for n in self.neighbors[site]) \
                        - self.h * np.cos(self.spins[site])
            if newEnergy <= oldEnergy or np.random.rand() < np.exp(-(newEnergy - oldEnergy) * beta):
                self.spins[site] = newSpin

    def get_energy(self):
        energy = np.zeros(np.shape(self.spins))
        for site in range(len(self.spins)):
            energy[site] = - sum(np.cos(self.spins[site] - self.spins[n]) for n in self.neighbors[site]) \
                           - self.h * np.cos(self.spins[site])
        # returns array of energy at each site, summed to get total energy, and then divided by number of spins
        # to get average energy per site of system
        return energy

    def animate(self):
        for _ in range(15):
            self.poke()
        grid = self.spins.reshape(self.width, self.width)
        self.im.set_data(grid)
        return self.im

    def make_animation(self, duration = 8, prepend = 'lattice'):
        anim = animation.FuncAnimation(self.fig, self.animate, frames = duration * 25, interval = 40)
        video = anim.to_html5_video()

        # embedding for the video
        html = display.HTML(video)

        # draw the animation
        display.display(html)
        plt.close()

        return

        name = prepend + '.gif'
        count = 0
        while os.path.exists(name):
            count += 1
            name = prepend + str(count) + '.gif'
        anim.save(name, writer = 'PillowWriter')

    def show(self):
        grid = self.spins.reshape(self.width, self.width)
        plot = plt.imshow(grid, cmap = 'twilight_shifted', vmin = 0, vmax = 2*np.pi)
        plt.colorbar(plot, label = 'Spin angle').ax.set_yticks([0, np.pi, 2* np.pi], ['0', '$\pi$', '2$\pi$'])
        plt.axis('off')
        plt.show()

sample = lattice(width = 128)
for _ in range(100):
    sample.show()
    sample.poke()
sample.show()