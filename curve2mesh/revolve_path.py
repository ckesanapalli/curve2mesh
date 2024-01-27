"""
Module for generating 3D meshes from 2D curves.

Author: Chaitanya Kesanapalli
License: MIT License
"""

import numpy as np

TWO_PI = 2 * np.pi


def revolve_curve_along_path(curve: np.ndarray, revolve_path: np.ndarray) -> np.ndarray:
    """
    Revolve a 2D curve along a given path to create a 3D surface mesh.

    This function takes a 2D curve and a path for revolution, and creates a 3D mesh by revolving
    the curve along the path.

    Parameters
    ----------
    curve : np.ndarray
        An (n x 2) array representing X, Z coordinates of the 2D curve.
    revolve_path : np.ndarray
        An (m x 2) array representing polar coordinates (angle in radians, radius) of the revolve path.

    Returns
    -------
    np.ndarray
        An ((m-1)(n-1) x 4 x 3) array representing the faces of the 3D surface mesh.


    Raises
    ------
    ValueError
        If `curve` or `revolve_path` do not have the correct shape or dimensions.

    Examples
    --------
    >>> from curve2mesh import revolve_curve_along_path
    >>> import numpy as np
    >>>
    >>> # Simple Example
    >>> curve = np.array([[1, 2], [3, 4]])
    >>> revolve_path = np.array([[0, 1], [np.pi/2, 2]])
    >>> mesh = revolve_curve_along_path(curve, revolve_path)
    >>> mesh
    array([[[1.2246468e-16, 2.0000000e+00, 2.0000000e+00],
            [1.0000000e+00, 0.0000000e+00, 2.0000000e+00],
            [3.0000000e+00, 0.0000000e+00, 4.0000000e+00],
            [3.6739404e-16, 6.0000000e+00, 4.0000000e+00]]])
    >>>
    >>> # 3D Plot
    >>> import matplotlib.pyplot as plt
    >>> from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    >>> x = np.linspace(1, 10, 100)
    >>> z = np.log(x)
    >>> curve = np.array([x, z]).T
    >>>
    >>> angle_rad = np.linspace(0, 4*np.pi, 100)
    >>> radius = angle_rad/10
    >>> revolve_path = np.array([angle_rad, radius]).T
    >>>
    >>> revolved_mesh = revolve_curve_along_path(curve, revolve_path)
    >>>
    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111, projection='3d')
    >>> ax.add_collection3d(Poly3DCollection(revolved_mesh, alpha=0.5))
    >>> ax.set_xlim(-x.max(), x.max())
    >>> ax.set_ylim(-x.max(), x.max())
    >>> ax.set_zlim(z.min(), z.max())
    >>> plt.show()

    """
    if curve.ndim != 2 or curve.shape[1] != 2:
        raise ValueError("Curve array must be of shape (n, 2)")

    if revolve_path.ndim != 2 or revolve_path.shape[1] != 2:
        raise ValueError("Revolve path array must be of shape (m, 2)")

    main_x1, main_x2 = curve[:-1, 0], curve[1:, 0]
    main_z1, main_z2 = curve[:-1, 1], curve[1:, 1]

    curve_matrix = np.array([
        [main_x1, main_x1, main_z1],
        [main_x1, main_x1, main_z1],
        [main_x2, main_x2, main_z2],
        [main_x2, main_x2, main_z2],
        ])

    angles_rad, path_radius = revolve_path.T
    path_x, path_y = path_radius * [np.cos(angles_rad), np.sin(angles_rad)]
    path_x1, path_x2 = path_x[1:], path_x[:-1]
    path_y1, path_y2 = path_y[1:], path_y[:-1]
    ones = np.ones_like(path_x1)

    path_matrix = np.array([
        [path_x1, path_y1, ones],
        [path_x2, path_y2, ones],
        [path_x2, path_y2, ones],
        [path_x1, path_y1, ones],
        ])

    mesh = np.einsum("van, vag -> gnva", curve_matrix, path_matrix)
    return mesh.reshape(-1, 4, 3)


def circular_path(divisions: int, end_angle: float = TWO_PI) -> np.ndarray:
    """
    Generate a circular path described in polar coordinates.

    This function creates a circular path with a specified number of divisions
    and an end angle. The path is represented in polar coordinates (angle, radius=1).

    Parameters
    ----------
    divisions : int
        The number of divisions in the circular path. Must be a positive integer.
    end_angle : float, optional
        The ending angle of the circular path in radians. Defaults to 2π for a full circle.

    Returns
    -------
    np.ndarray
        An array of shape (divisions, 2) representing the polar coordinates of the path.

    Raises
    ------
    ValueError
        If divisions is not a positive integer.

    Examples
    --------
    >>> circular_path(4)
    array([[0.        , 1.        ],
           [2.0943951 , 1.        ],
           [4.1887902 , 1.        ],
           [6.28318531, 1.        ]])
    """
    if not isinstance(divisions, int) or divisions <= 0:
        raise ValueError("divisions must be a positive integer")

    angles = np.linspace(0, end_angle, divisions)
    revolve_path = np.column_stack((angles, np.ones(divisions)))
    return revolve_path
