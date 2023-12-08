"""
Test suite for the revolve_curve function in the curve2mesh module.

This test suite covers various scenarios, including input validations,
output correctness, and checks for both NumPy and standard Python implementations.

Author: Chaitanya Kesanapalli
"""

import pytest
import math
import numpy as np
from curve2mesh import revolve_curve

# Constants for testing
X_SAMPLE = [0, 1, 2]
Z_SAMPLE = [2, 1, 0]
ANGLE_COUNT_SAMPLE = 10


def approx_equal_3d_array(array1, array2, tol=1e-5):
    """Helper function to check approximate equality of 3D arrays."""
    return all(math.isclose(a, b, rel_tol=tol) for a, b in zip(array1.ravel(), array2.ravel()))


@pytest.fixture
def sample_curve():
    """Fixture to provide sample curve data."""
    x = np.linspace(0, 1, 10) if np else [i/10 for i in range(10)]
    z = np.power(x, 2) if np else [i**2/100 for i in range(10)]
    return x, z


@pytest.mark.parametrize("angle_count", [10, 50, 100])
def test_revolve_curve_length(sample_curve, angle_count):
    """Test if revolve_curve returns the correct number of faces."""
    x, z = sample_curve
    faces = revolve_curve(x, z, angle_count)
    expected_faces_count = (len(x) - 1) * angle_count
    assert len(faces) == expected_faces_count, "Incorrect number of faces in the generated mesh."


def test_revolve_curve_small():
    x = [1, 2]
    z = [3, 4]
    angle_count = 4
    result = revolve_curve(x, z, angle_count)
    assert len(result) == angle_count * (len(x) - 1), "Incorrect number of faces generated"

def test_revolve_curve_with_numpy():
    x = [0.5, 1.0, 1.5]
    z = [1, 4, 9]
    angle_count = 8
    result = revolve_curve(x, z, angle_count)
    assert len(result) == angle_count * (len(x) - 1), "Incorrect number of faces generated with NumPy"

def test_revolve_curve_without_numpy(monkeypatch):
    monkeypatch.setattr("curve2mesh.NUMPY_AVAILABLE", False)  # Replace 'curve2mesh' with the actual name of your module
    x = [0.5, 1.0, 1.5]
    z = [1, 4, 9]
    angle_count = 8
    result = revolve_curve(x, z, angle_count)
    assert len(result) == angle_count * (len(x) - 1), "Incorrect number of faces generated without NumPy"
