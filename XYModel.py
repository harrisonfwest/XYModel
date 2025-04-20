"""
Created on Sun Apr 20, 2025 @ 4:09 pm
@author: Harrison West, Renn Summersgill
"""

import numpy as np
import matplotlib.pyplot as plt

def newLattice1D(width: int) -> np.ndarray:
    lattice = np.random.uniform(-np.pi, np.pi, size=width)
    return lattice

def showLattice(lattice: np.ndarray) -> None:
    plt.imshow(lattice, cmap = 'hsv', vmin = -np.pi, vmax = +np.pi)
    plt.ylim(0, len(lattice[0]))
    plt.xlim(0, len(lattice[0]))
    plt.colorbar(ticks = [-np.pi+.1, 0, np.pi-.1]).ax.set_yticklabels(['-$\pi$', 0, '$\pi$'])
    plt.show()

# showLattice(newLattice1D(10))

def energyof1D(lattice: np.ndarray) -> float:
    energy = 0
    for i in range(len(lattice)):
        energy += np.cos(lattice[i] - lattice[(i+1)%len(lattice)])
    return energy

def squareLattice2D(width: int) -> np.ndarray:
    lattice = np.random.uniform(-np.pi, np.pi, size=[width, width])
    return lattice

def energyof2D(lattice: np.ndarray) -> float:
    energy = 0
    for i in range(len(lattice)):
        for j in range(len(lattice)):
            energy += np.cos(lattice[i, j] - lattice[(i+1)%len(lattice[0]), (j+1)%len(lattice[0])])
    return energy

def equilibrate2D(lattice: np.ndarray, temp: float) -> np.ndarray:
    width = len(lattice[0])
    for _ in range(20000):
        i = np.random.choice(width)
        j = np.random.choice(width)
        oldE = energyof2D(lattice)
        newLattice = lattice
        for k in np.linspace(2*np.pi, 0):
            newL
        if newLattice[i, j] + 0.5 > np.pi:
            newLattice[i, j] = newLattice[i, j] - (np.pi - 0.5)
        else:
            newLattice[i, j] + 0.5
        newE = energyof2D(newLattice)
        if newE < oldE or np.random.random() < np.exp(-newE/temp):
            lattice = newLattice
    return lattice

sample = squareLattice2D(50)
showLattice(sample)
sample = equilibrate2D(sample, 1.5)
showLattice(sample)
