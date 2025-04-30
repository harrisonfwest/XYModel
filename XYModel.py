"""
Created on Sun Apr 20, 2025 @ 4:09 pm
@author: Harrison West, Renn Summersgill
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

pi = np.pi
class lattice():
    def __init__(self, temperature : float = .01, width : int = 64, external_field : float = 0.0) -> None:
        self.width = width
        self.size = self.width * self.width
        self.h = external_field
        L, N = self.width, self.size
        self.neighbors = {i : ((i//L)*L + (i+1)%L, (i+L)%N, (i//L)*L + (i-1)%L, (i-L)%N) for i in list(range(N))}
        self.spins = np.random.uniform(0, 2*pi, self.size)
        self.temperature = temperature
        self.fig = plt.figure()
        self.im = plt.imshow(self.spins.reshape(self.width, self.width), cmap = 'twilight',
                             vmin = 0, vmax = 2*pi)
        plt.colorbar(self.im, ticks=[0, pi, 2*pi], extend = 'both').ax.set_yticklabels([0, '$\pi$', '2$\pi$'], label = 'Spin angle')
        plt.axis('off')

    def show(self) -> None:
        grid = self.spins.reshape(self.width, self.width)
        plt.imshow(grid, cmap = 'twilight_shifted', vmin = 0, vmax = 2*pi)
        plt.axis('off')
        plt.show()
        return

    def poke(self) -> None:
        beta = 1 / self.temperature
        sites = list(range(len(self.spins)))
        np.random.shuffle(sites)
        for site in sites:
            oldEnergy = -sum(np.cos(self.spins[site] - self.spins[n]) for n in self.neighbors[site]) - self.h * np.cos(self.spins[site])

            newSpin = (self.spins[site] + np.random.uniform(0, 2*pi)) % (2 * pi)

            newEnergy = -sum(np.cos(newSpin - self.spins[n]) for n in self.neighbors[site]) - self.h * np.cos(self.spins[site])
            if newEnergy <= oldEnergy or np.random.rand() < np.exp(-(newEnergy - oldEnergy) * beta):
                self.spins[site] = newSpin
        return

    def get_energy(self) -> np.array: # currently unused, but can be used later to see how energy changes as system equilibrates
        energy = np.zeros(np.shape(self.spins))
        for site in range(len(self.spins)):
            energy[site] = -sum(np.cos(self.spins[site] - self.spins[n]) for n in self.neighbors[site]) \
                           - self.h * np.cos(self.spins[site])
        return energy

    def animate(self, frame):
        self.poke()
        grid = self.spins.reshape(self.width, self.width)
        self.im.set_data(grid)
        return self.im

    def make_animation(self, prepend : str = 'lattice') -> None:
        anim = animation.FuncAnimation(self.fig, self.animate, frames = 1000, interval = 20)
        name = prepend + '.gif'
        count = 0
        while os.path.exists('gifs/' + name):
            count += 1
            name = prepend + str(count) + '.gif'
        anim.save('gifs/' + name)
        return

sample = lattice(width = 128)
sample.make_animation()