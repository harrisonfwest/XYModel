"""
Created on Sun Apr 20, 2025 @ 4:09 pm
@author: Harrison West, Renn Summersgill
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

class lattice():
    def __init__(self, temperature = .1, width = 15):
        self.width = width
        self.size = self.width * self.width
        L, N = self.width, self.size
        self.neighbors = {i : ((i//L)*L + (i+1)%L, (i+L)%N, (i//L)*L + (i-L)%L, (i-L)%N) for i in list(range(N))}
        self.spins = np.random.uniform(-np.pi, np.pi, self.size)
        self.temperature = temperature
        self.energy = np.sum(self.get_energy())/N
        self.fig = plt.figure()
        self.im = plt.imshow(self.spins.reshape(self.width, self.width), cmap = 'twilight_shifted',
                             vmin = -np.pi, vmax = +np.pi)
        plt.colorbar(ticks=[-np.pi + .1, 0, np.pi - .1]).ax.set_yticklabels(['-$\pi$', 0, '$\pi$'])
        plt.axis('off')

    def poke(self): # tries a random new spin for each lattice site, in a random order of sites
        beta = 1 / self.temperature
        sites = list(range(len(self.spins)))
        np.random.shuffle(sites)
        for site in sites:
            oldEnergy = -sum(np.cos(self.spins[site] - self.spins[n]) for n in self.neighbors[site])
            newSpin = self.spins[site] + np.random.uniform(-np.pi, np.pi)
            if newSpin > 2*np.pi:
                newSpin -= 2*np.pi
            newEnergy = -sum(np.cos(newSpin - self.spins[n]) for n in self.neighbors[site])
            if np.random.rand() < np.exp(-(newEnergy - oldEnergy) * beta):
                self.spins[site] = newSpin

    def get_energy(self):
        energy = np.zeros(np.shape(self.spins))
        for site in range(len(self.spins)):
            energy[site] = -sum(np.cos(self.spins[site] - self.spins[n]) for n in self.neighbors[site])
        return energy

    def animate(self):
        grid = self.spins.reshape(self.width, self.width)
        self.im = plt.imshow(grid, cmap = 'twilight_shifted', vmin = -np.pi, vmax = +np.pi)

    def animate(self, frame):
        self.poke()
        grid = self.spins.reshape(self.width, self.width)
        self.im.set_data(grid)
        return self.im

    def make_animation(self):
        anim = animation.FuncAnimation(self.fig, self.animate, frames = self.width, interval = 10)
        anim.save('lattice.gif', fps = 30)

sample = lattice(temperature = .1, width = 128)

sample.make_animation()

# while True:
#     sample.poke()
#     sample.plot_lattice()