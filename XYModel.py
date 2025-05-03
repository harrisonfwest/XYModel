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
    def __init__(self, temperature : float = .01, width : int = 128, external_field : float = 0.0) -> None:
        # Assumes coupling constant J = 1
        self.width = width
        self.size = self.width * self.width
        self.h = external_field
        L, N = self.width, self.size
        self.neighbors = {i : ((i//L)*L + (i+1)%L, (i+L)%N, (i//L)*L + (i-1)%L, (i-L)%N) for i in list(range(N))}
        self.spins = np.random.uniform(0, 2*pi, self.size)
        self.temperature = temperature

        self.fig, self.ax = plt.subplots()
        self.im = plt.imshow(self.spins.reshape(self.width, self.width), cmap = 'twilight',
                             vmin = 0, vmax = 2*pi,
                             interpolation = 'nearest')
        plt.title('XY Lattice: T = %.4f, h = %.4f' % (temperature, external_field))
        plt.colorbar(self.im, ticks=[0, pi, 2*pi], label = 'Spin angle').ax.set_yticklabels([0, '$\pi$', '2$\pi$'])
        plt.axis('off')

    def poke(self) -> None:
        beta = 1 / self.temperature
        sites = list(range(len(self.spins)))
        np.random.shuffle(sites)
        for site in sites:
            oldEnergy = -sum(np.cos(self.spins[site] - self.spins[n]) for n in self.neighbors[site]) - (self.h * np.cos(self.spins[site]))
            newSpin = (self.spins[site] + np.random.uniform(0, 2*pi)) % (2 * pi)
            newEnergy = -sum(np.cos(newSpin          - self.spins[n]) for n in self.neighbors[site]) - (self.h * np.cos(newSpin))
            if newEnergy <= oldEnergy or np.random.rand() < np.exp(-(newEnergy - oldEnergy) * beta):
                self.spins[site] = newSpin
        self.fig.canvas.draw()
        return

    def get_energy(self) -> np.array: # currently unused, but can be used later to see how energy changes as system equilibrates
        energy = np.zeros(np.shape(self.spins))
        for site in range(len(self.spins)):
            energy[site] = -sum(np.cos(self.spins[site] - self.spins[n]) for n in self.neighbors[site]) \
                           - (self.h * np.cos(self.spins[site]))
        return energy
    
    def get_magnetization(self):
        mag = np.sum(np.cos(self.spins))
        return mag/self.size
    
    def plot_magnetization(self): # Plot mean magnetization of an initial system over time
        mags = []
        for _ in range(200):
            mags.append(self.get_magnetization)
            self.poke()
        fig = plt.figure()
        fig.plot(range(200), mags)
        fig.title('Mean magnetization of system with width %i, h = %.4f, T = %.4f' % (self.width, self.h, self.temperature))
        fig.xlabel('Time step')
        fig.ylabel('Mean magnetization')
        fig.show()

    def animate(self, frame):
        self.poke()
        grid = self.spins.reshape(self.width, self.width)
        self.im = plt.imshow(grid, cmap = 'twilight', interpolation = 'nearest')
        return self.im

    def make_animation(self, prepend : str = 'lattice') -> None:
        anim = animation.FuncAnimation(self.fig, self.animate, frames = 200, interval = 100)
        name = prepend + '.gif'
        count = 0
        while os.path.exists('gifs/' + name):
            count += 1
            name = prepend + str(count) + '.gif'
        anim.save('gifs/' + name)
        # TODO: save image of final frame of the animation
        # plt.savefig('stills/' + prepend + str(count) + '.png')
        return
    
    def copy(self): # primary purpose is to copy the spin structure
        copy = lattice(temperature = self.temperature, width = self.width, external_field = self.h)
        copy.spins = np.copy(self.spins)
        return copy
    
    ### TODO: previously there was a show() function, but calling it would prevent make_animation() from
    ### working correctly. Could be worth re-creating but not a necessary feature as long as make_animation() works
    ### Note that make_animation takes much longer than simply showing would, but it produces and saves a full gif
    ### showing the system's evolution instead of a still image

sample = lattice(width = 128, temperature = 15)
sample.make_animation()