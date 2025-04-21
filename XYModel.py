"""
Created on Sun Apr 20, 2025 @ 4:09 pm
@author: Harrison West, Renn Summersgill
"""

import numpy as np
import matplotlib.pyplot as plt

class lattice():
    def __init__(self, temperature = .1, width = 15):
        self.width = width
        self.size = self.width * self.width
        L, N = self.width, self.size
        self.neighbors = {i : ((i//L)*L + (i+1)%L, (i+L)%N, (i-1)%L, (i//L)*L + (i-L)%N) for i in list(range(N))}
        self.spins = np.random.uniform(-np.pi, np.pi, self.size)
        self.temperature = temperature
        self.energy = np.sum(self.get_energy())/N

    def set_temperature(self, temperature):
        self.temperature = temperature

    def poke(self): # tries a random spin for each lattice site in a random order
        beta = 1 / self.temperature
        sites = list(range(len(self.spins)))
        np.random.shuffle(sites)
        for site in sites:
            oldEnergy = -np.sum(np.cos(self.spins[site] - self.spins[n]) for n in self.neighbors[site])
            newSpin = self.spins[site] + np.random.uniform(-np.pi, np.pi)
            if newSpin > 2*np.pi:
                newSpin -= 2*np.pi
            newEnergy = -np.sum(np.cos(newSpin - self.spins[n]) for n in self.neighbors[site])
            if np.random.rand() < np.exp(-(newEnergy - oldEnergy) * beta):
                self.spins[site] = newSpin

    def get_energy(self):
        energy = np.zeros(np.shape(self.spins))
        site = 0
        for spin in self.spins:
            energy[site] = -sum(np.cos(spin - self.spins[n]) for n in self.neighbors[site])
            site += 1
        return energy

    def plot_lattice(self):
        grid = self.spins.reshape(self.width, self.width)
        plt.imshow(grid, cmap = 'twilight_shifted', vmin = -np.pi, vmax = +np.pi)
        plt.colorbar()
        plt.colorbar(ticks=[-np.pi + .1, 0, np.pi - .1]).ax.set_yticklabels(['-$\pi$', 0, '$\pi$'])
        plt.show()

sample = lattice(width = 256)
while True:
    sample.plot_lattice()