"""
Test suite for the revolve_curve_along_path function in the curve2mesh module.

Author: Chaitanya Kesanapalli
"""

import numpy as np
import pytest
from curve2mesh import revolve_curve_along_path, circular_path, TWO_PI

def test_revolve_curve_along_path_shape():
    curve = np.array([[1, 2], [3, 4]])
    revolve_path = np.array([[0, 1], [np.pi/2, 2]])
    mesh = revolve_curve_along_path(curve, revolve_path)
    assert mesh.shape == (1, 4, 3)

def test_revolve_curve_along_path_type():
    curve = np.array([[1, 2], [3, 4]])
    revolve_path = np.array([[0, 1], [np.pi/2, 2]])
    mesh = revolve_curve_along_path(curve, revolve_path)
    assert isinstance(mesh, np.ndarray)

def test_circular_path_shape():
    path = circular_path(4, TWO_PI)
    assert path.shape == (4, 2)

def test_circular_path_type():
    path = circular_path(4, TWO_PI)
    assert isinstance(path, np.ndarray)

def test_circular_path_invalid_divisions():
    with pytest.raises(ValueError):
        circular_path(-1)

def test_circular_path_invalid_divisions_type():
    with pytest.raises(ValueError):
        circular_path(3.5)

def test_revolve_curve_along_path_invalid_curve_shape():
    curve = np.array([1, 2, 3])
    revolve_path = np.array([[0, 1], [np.pi/2, 2]])
    with pytest.raises(ValueError):
        revolve_curve_along_path(curve, revolve_path)

def test_revolve_curve_along_path_invalid_revolve_path_shape():
    curve = np.array([[1, 2], [3, 4]])
    revolve_path = np.array([1, 2, 3])
    with pytest.raises(ValueError):
        revolve_curve_along_path(curve, revolve_path)

# Tests for revolve_curve_along_path

def test_revolve_curve_along_path_valid_input():
    curve = np.array([[1, 2], [3, 4]])
    revolve_path = np.array([[0, 1], [np.pi / 2, 2]])
    expected_output = np.array([[[1.2246468e-16, 2.0000000e+00, 2.0000000e+00],
                                 [1.0000000e+00, 0.0000000e+00, 2.0000000e+00],
                                 [3.0000000e+00, 0.0000000e+00, 4.0000000e+00],
                                 [3.6739404e-16, 6.0000000e+00, 4.0000000e+00]]])
    output = revolve_curve_along_path(curve, revolve_path)
    np.testing.assert_allclose(output, expected_output)

# Tests for circular_path

def test_circular_path_valid_input():
    divisions = 4
    expected_output = np.array([[0.0, 1.0],
                                [2 * np.pi / 3, 1.0],
                                [4 * np.pi / 3, 1.0],
                                [TWO_PI, 1.0]])
    output = circular_path(divisions)
    np.testing.assert_allclose(output, expected_output)


def test_circular_path_invalid_input():
    with pytest.raises(ValueError):
        circular_path(-1)
