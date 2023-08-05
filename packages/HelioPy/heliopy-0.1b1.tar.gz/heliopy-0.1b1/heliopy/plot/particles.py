"""Methods for plotting particle distribution functions."""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def scatter3d(x, y, z, pdf):
    """Perform 3D scatter plot of distribution function data."""
    fig = plt.gcf()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, c=np.log10(pdf), s=40)


def contour2d(x, y, pdf, showbins=True, nlevels=10):
    """Perform a countour plot of 2D distribution function data."""
    ax = plt.gca()
    ax.tricontourf(x, y, np.log10(pdf), nlevels, cmap='viridis')
    if showbins:
        ax.scatter(x, y, c=np.log10(pdf), cmap='viridis', edgecolors='k', s=30)


def surf2d(x, y, pdf):
    """3D surf plot of 2D distribution function."""
    fig = plt.gcf()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(x, y, np.log10(pdf), cmap='viridis', linewidths=0, alpha=0.5)
