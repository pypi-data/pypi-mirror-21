from heliopy.vector.transformations import *
import numpy as np


def test_cart2pitchangles():
    v = np.array([0, 1, 0])
    x = np.array([0, 0, 0])
    y = np.array([1, -1, 0])
    z = np.array([0, 0, 1])

    out = cart2pitchangles(x, y, z, v)
    expected = np.array([0, np.pi, np.pi / 2])
    np.testing.assert_almost_equal(out, expected)


def test_cart2pol():
    x = 1
    y = 0
    r, phi = cart2pol(x, y)
    np.testing.assert_almost_equal(r, 1)
    np.testing.assert_almost_equal(phi, 0)

    y = 1
    r, phi = cart2pol(x, y)
    np.testing.assert_almost_equal(r, np.sqrt(2))
    np.testing.assert_almost_equal(phi, np.pi / 4)


def test_pol2cart():
    r = np.random.rand()
    phi = 0
    x, y = pol2cart(r, phi)
    np.testing.assert_almost_equal(x, r)
    np.testing.assert_almost_equal(y, 0)

    r = np.random.rand()
    phi = np.pi / 2
    x, y = pol2cart(r, phi)
    np.testing.assert_almost_equal(x, 0)
    np.testing.assert_almost_equal(y, r)


def test_cartsph():
    x = np.random.rand()
    y = np.random.rand()
    z = np.random.rand()
    r, theta, phi = cart2sph(x, y, z)
    xnew, ynew, znew = sph2cart(r, theta, phi)
    np.testing.assert_almost_equal(xnew, x)
    np.testing.assert_almost_equal(ynew, y)
    np.testing.assert_almost_equal(znew, z)


def test_cart2sph():
    x = 1
    y = 0
    z = 0
    r, theta, phi = cart2sph(x, y, z)
    assert r == 1
    assert theta == 0
    assert phi == 0


def test_rotationmatrix():
    v = np.array([0, 0, 1])
    Rout = rotationmatrix(v)
    expected = np.array([[1, 0, 0],
                         [0, 1, 0],
                         [0, 0, 1]])

    np.testing.assert_almost_equal(Rout, expected)

    # Vector with random components in range [-0.5, 0.5]
    v = np.random.rand(3) - 0.5
    Rout = rotationmatrix(v)
    vz = np.dot(Rout, v) / np.linalg.norm(v)
    expected = np.array([0, 0, 1])
    np.testing.assert_almost_equal(vz, expected)
