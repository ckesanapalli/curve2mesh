"""
Module for generating 3D meshes from 2D curves.

This module provides functionality to revolve a 2D curve around the Y-axis
to create a 3D mesh. It supports operations with NumPy if available, falling
back to standard Python math operations otherwise.

Author: Chaitanya Kesanapalli
License: MIT License
"""
from typing import Sequence
import math

# Try to import NumPy. If not available, use standard Python math operations.
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


def revolve_curve(
        x: Sequence[float],
        z: Sequence[float],
        angle_count: int
        ) -> list[tuple[float, float, float]]:
    """
    Revolve a 2D curve around the Y-axis to create a 3D mesh.

    Parameters
    ----------
    x : Sequence[float]
        X-coordinates of the 2D curve.
    z : Sequence[float]
        Z-coordinates of the 2D curve.
    angle_count : int
        Number of angles for the revolution.

    Returns
    -------
    list[tuple[float, float, float]]
        A list of tuples representing the faces of the 3D mesh.

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    >>> # Example 2D curve
    >>> x = np.linspace(0, 1, 100) if NUMPY_AVAILABLE else [i/100 for i in range(100)]
    >>> z = x

    >>> angle_count = 50
    >>> faces = revolve_curve(x, z, angle_count)

    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111, projection='3d')
    >>> ax.add_collection3d(Poly3DCollection(faces, facecolors='g', linewidths=1, alpha=0.5))
    >>> ax.set_xlim(-1, 1)
    >>> ax.set_ylim(-1, 1)
    >>> ax.set_zlim(-1, 1)
    >>> plt.show()
    """
    if NUMPY_AVAILABLE:
        return _revolve_curve_numpy(x, z, angle_count)
    else:
        return _revolve_curve_standard(x, z, angle_count)


def _revolve_curve_numpy(x, z, angle_count):
    """revolve_curve using NumPy."""
    angle_step = 2 * np.pi / angle_count
    angles = np.linspace(0, 2 * np.pi - angle_step, angle_count)
    cos1, sin1 = np.cos(angles), np.sin(angles)
    cos2, sin2 = np.cos(angles + angle_step), np.sin(angles + angle_step)
    ones = np.ones_like(angles)

    x1, z1, x2, z2 = x[:-1], z[:-1], x[1:], z[1:]
    mul = np.multiply.outer
    return np.array([
        [mul(x1, cos1), mul(x1, sin1), mul(z1, ones)],
        [mul(x1, cos2), mul(x1, sin2), mul(z1, ones)],
        [mul(x2, cos2), mul(x2, sin2), mul(z2, ones)],
        [mul(x2, cos1), mul(x2, sin1), mul(z2, ones)],
    ]).reshape(4, 3, -1).transpose(2, 0, 1)


def _revolve_curve_standard(x, z, angle_count):
    """revolve_curve using standard Python math."""
    angle_step = 2 * math.pi / angle_count
    faces = []

    for angle_idx in range(angle_count):
        angle = angle_step * angle_idx
        cos1, sin1 = math.cos(angle), math.sin(angle)
        cos2, sin2 = math.cos(angle + angle_step), math.sin(angle + angle_step)

        for idx in range(len(x) - 1):
            x1, z1, x2, z2 = x[idx], z[idx], x[idx + 1], z[idx + 1]
            face = [
                (x1 * cos1, x1 * sin1, z1),
                (x1 * cos2, x1 * sin2, z1),
                (x2 * cos2, x2 * sin2, z2),
                (x2 * cos1, x2 * sin1, z2),
            ]
            faces.append(face)

    return faces
