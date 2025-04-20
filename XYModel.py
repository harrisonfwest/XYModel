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
    plt.imshow(lattice, cmap = 'cool')
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

showLattice(squareLattice2D(100))