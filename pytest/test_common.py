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


@pytest.mark.parametrize("invalid_input", [
    ([], Z_SAMPLE, ANGLE_COUNT_SAMPLE),
    (X_SAMPLE, [], ANGLE_COUNT_SAMPLE),
    (X_SAMPLE, Z_SAMPLE, -1)
])
def test_revolve_curve_invalid_input(invalid_input):
    """Test if revolve_curve handles invalid inputs correctly."""
    x, z, angle_count = invalid_input
    with pytest.raises(ValueError):
        revolve_curve(x, z, angle_count)
