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
            newSpin = np.random.uniform(0, 2*pi)
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
    
    def plot_energy(self) -> None:
        energies = []
        x_vals = np.arange(1, 750)
        for _ in x_vals:
            energies.append(np.sum(self.get_energy())/self.size)
            self.poke()
        plt.clf()
        plt.plot(x_vals, energies)
        plt.title('Mean energy of system with width %i, h = %.4f, T = %.4f' % (self.width, self.h, self.temperature))
        plt.xlabel('Time step')
        plt.ylabel('Mean energy')
        name = 'stills/mean_energy.png'
        count = 0
        while os.path.exists(name):
            count += 1
            name = 'stills/mean_energy' + str(count) + '.png'
        plt.savefig(name)
        return None
    
    def get_magnetization(self):
        mag = np.sum(np.cos(self.spins))
        return mag/self.size
    
    def plot_magnetization(self) -> None: # Plot mean magnetization of an initial system over time
        mags = []
        x_vals = np.arange(1, 750)
        for _ in x_vals:
            mags.append(self.get_magnetization())
            self.poke()
        plt.clf()
        plt.plot(x_vals, mags)
        plt.title('Mean magnetization of system with width %i, h = %.4f, T = %.4f' % (self.width, self.h, self.temperature))
        plt.xlabel('Time step')
        plt.ylabel('Mean magnetization')
        
        name = 'stills/mean_mag.png'
        count = 0
        while os.path.exists(name):
            count += 1
            name = 'stills/mean_mag' + str(count) + '.png'
        plt.savefig(name)
        return None

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

plt.close()
temperature_range = [0.01, 0.1, 1, 3, 10]
x_vals = np.arange(1, 500)
mean_mags = np.empty(shape = (len(temperature_range), len(x_vals), 20))
for i in range(len(temperature_range)):
    for k in range(20):
        mag_lattice = lattice(temperature = temperature_range[i])
        plt.close()
        for j in range(len(x_vals)):
            mean_mags[i, j, k] = mag_lattice.get_magnetization()
            mag_lattice.poke()

# mean_mags: for each temp, an array of xvals, each has 20 vals to average
final_means = np.empty(shape = (len(temperature_range), len(x_vals)))
for i in range(len(temperature_range)):
    for j in range(len(x_vals)):
        final_means[i, j] = np.average(mean_mags[i, j])


plt.clf()
for i in range(len(temperature_range)):
    plt.plot(x_vals, abs(final_means[i]), label = 'T = %.2f' % temperature_range[i], alpha = 0.5)
plt.legend()
plt.title('Absolute Values of Mean Magnetizations per spin (averaged over 20 systems for convergence) (Width = 128)')
plt.savefig('stills/mean_mag_collection.png')