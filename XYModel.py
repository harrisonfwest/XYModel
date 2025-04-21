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
    plt.imshow(lattice, cmap = 'twilight_shifted', vmin = -np.pi, vmax = +np.pi)
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
            energy -= (np.cos(lattice[i, j] - lattice[(i+1)%len(lattice[0]), j])
            + np.cos(lattice[i, j] - lattice[i, (j+1)%len(lattice[0])]))
    return energy/(2 * len(lattice)**2)

def equilibrate2D(lattice: np.ndarray, temp: float) -> np.ndarray:
    currLattice = lattice
    width = len(lattice[0])
    for k in range(len(lattice)):
        i = np.random.choice(range(width))
        j = np.random.choice(range(width))
        oldE = energyof2D(currLattice)
        newLattice = np.copy(currLattice)
        newLattice[i][j] = np.random.uniform(-np.pi, np.pi)
        newE = energyof2D(newLattice)
        if np.random.uniform(0, 1) < np.exp(-(newE - oldE)/temp):
            currLattice[i][j] = newLattice[i][j]
    return currLattice

sample = squareLattice2D(512)
showLattice(sample)
while True:
    sample = equilibrate2D(sample, 0.005 )
    showLattice(sample)