import numpy as np
from numpy.testing import (assert_equal, assert_almost_equal,
                           assert_raises)
from skimage.transform._geometric import GeometricTransform
from skimage.transform import (estimate_transform, matrix_transform,
                               EuclideanTransform, SimilarityTransform,
                               AffineTransform, FundamentalMatrixTransform,
                               EssentialMatrixTransform, ProjectiveTransform,
                               PolynomialTransform, PiecewiseAffineTransform)
from skimage._shared._warnings import expected_warnings


SRC = np.array([
    [-12.3705, -10.5075],
    [-10.7865, 15.4305],
    [8.6985, 10.8675],
    [11.4975, -9.5715],
    [7.8435, 7.4835],
    [-5.3325, 6.5025],
    [6.7905, -6.3765],
    [-6.1695, -0.8235],
])
DST = np.array([
    [0, 0],
    [0, 5800],
    [4900, 5800],
    [4900, 0],
    [4479, 4580],
    [1176, 3660],
    [3754, 790],
    [1024, 1931],
])


def test_estimate_transform():
    for tform in ('euclidean', 'similarity', 'affine', 'projective',
                  'polynomial'):
        estimate_transform(tform, SRC[:2, :], DST[:2, :])
    assert_raises(ValueError, estimate_transform, 'foobar',
                  SRC[:2, :], DST[:2, :])


def test_matrix_transform():
    tform = AffineTransform(scale=(0.1, 0.5), rotation=2)
    assert_equal(tform(SRC), matrix_transform(SRC, tform.params))


def test_euclidean_estimation():
    # exact solution
    tform = estimate_transform('euclidean', SRC[:2, :], SRC[:2, :] + 10)
    assert_almost_equal(tform(SRC[:2, :]), SRC[:2, :] + 10)
    assert_almost_equal(tform.params[0, 0], tform.params[1, 1])
    assert_almost_equal(tform.params[0, 1], - tform.params[1, 0])

    # over-determined
    tform2 = estimate_transform('euclidean', SRC, DST)
    assert_almost_equal(tform2.inverse(tform2(SRC)), SRC)
    assert_almost_equal(tform2.params[0, 0], tform2.params[1, 1])
    assert_almost_equal(tform2.params[0, 1], - tform2.params[1, 0])

    # via estimate method
    tform3 = EuclideanTransform()
    tform3.estimate(SRC, DST)
    assert_almost_equal(tform3.params, tform2.params)


def test_euclidean_init():
    # init with implicit parameters
    rotation = 1
    translation = (1, 1)
    tform = EuclideanTransform(rotation=rotation, translation=translation)
    assert_almost_equal(tform.rotation, rotation)
    assert_almost_equal(tform.translation, translation)

    # init with transformation matrix
    tform2 = EuclideanTransform(tform.params)
    assert_almost_equal(tform2.rotation, rotation)
    assert_almost_equal(tform2.translation, translation)

    # test special case for scale if rotation=0
    rotation = 0
    translation = (1, 1)
    tform = EuclideanTransform(rotation=rotation, translation=translation)
    assert_almost_equal(tform.rotation, rotation)
    assert_almost_equal(tform.translation, translation)

    # test special case for scale if rotation=90deg
    rotation = np.pi / 2
    translation = (1, 1)
    tform = EuclideanTransform(rotation=rotation, translation=translation)
    assert_almost_equal(tform.rotation, rotation)
    assert_almost_equal(tform.translation, translation)


def test_similarity_estimation():
    # exact solution
    tform = estimate_transform('similarity', SRC[:2, :], DST[:2, :])
    assert_almost_equal(tform(SRC[:2, :]), DST[:2, :])
    assert_almost_equal(tform.params[0, 0], tform.params[1, 1])
    assert_almost_equal(tform.params[0, 1], - tform.params[1, 0])

    # over-determined
    tform2 = estimate_transform('similarity', SRC, DST)
    assert_almost_equal(tform2.inverse(tform2(SRC)), SRC)
    assert_almost_equal(tform2.params[0, 0], tform2.params[1, 1])
    assert_almost_equal(tform2.params[0, 1], - tform2.params[1, 0])

    # via estimate method
    tform3 = SimilarityTransform()
    tform3.estimate(SRC, DST)
    assert_almost_equal(tform3.params, tform2.params)


def test_similarity_init():
    # init with implicit parameters
    scale = 0.1
    rotation = 1
    translation = (1, 1)
    tform = SimilarityTransform(scale=scale, rotation=rotation,
                                translation=translation)
    assert_almost_equal(tform.scale, scale)
    assert_almost_equal(tform.rotation, rotation)
    assert_almost_equal(tform.translation, translation)

    # init with transformation matrix
    tform2 = SimilarityTransform(tform.params)
    assert_almost_equal(tform2.scale, scale)
    assert_almost_equal(tform2.rotation, rotation)
    assert_almost_equal(tform2.translation, translation)

    # test special case for scale if rotation=0
    scale = 0.1
    rotation = 0
    translation = (1, 1)
    tform = SimilarityTransform(scale=scale, rotation=rotation,
                                translation=translation)
    assert_almost_equal(tform.scale, scale)
    assert_almost_equal(tform.rotation, rotation)
    assert_almost_equal(tform.translation, translation)


    # test special case for scale if rotation=90deg
    scale = 0.1
    rotation = np.pi / 2
    translation = (1, 1)
    tform = SimilarityTransform(scale=scale, rotation=rotation,
                                translation=translation)
    assert_almost_equal(tform.scale, scale)
    assert_almost_equal(tform.rotation, rotation)
    assert_almost_equal(tform.translation, translation)


def test_affine_estimation():
    # exact solution
    tform = estimate_transform('affine', SRC[:3, :], DST[:3, :])
    assert_almost_equal(tform(SRC[:3, :]), DST[:3, :])

    # over-determined
    tform2 = estimate_transform('affine', SRC, DST)
    assert_almost_equal(tform2.inverse(tform2(SRC)), SRC)

    # via estimate method
    tform3 = AffineTransform()
    tform3.estimate(SRC, DST)
    assert_almost_equal(tform3.params, tform2.params)


def test_affine_init():
    # init with implicit parameters
    scale = (0.1, 0.13)
    rotation = 1
    shear = 0.1
    translation = (1, 1)
    tform = AffineTransform(scale=scale, rotation=rotation, shear=shear,
                            translation=translation)
    assert_almost_equal(tform.scale, scale)
    assert_almost_equal(tform.rotation, rotation)
    assert_almost_equal(tform.shear, shear)
    assert_almost_equal(tform.translation, translation)

    # init with transformation matrix
    tform2 = AffineTransform(tform.params)
    assert_almost_equal(tform2.scale, scale)
    assert_almost_equal(tform2.rotation, rotation)
    assert_almost_equal(tform2.shear, shear)
    assert_almost_equal(tform2.translation, translation)


def test_piecewise_affine():
    tform = PiecewiseAffineTransform()
    tform.estimate(SRC, DST)
    # make sure each single affine transform is exactly estimated
    assert_almost_equal(tform(SRC), DST)
    assert_almost_equal(tform.inverse(DST), SRC)


def test_fundamental_matrix_estimation():
    src = np.array([1.839035, 1.924743, 0.543582,  0.375221,
                    0.473240, 0.142522, 0.964910,  0.598376,
                    0.102388, 0.140092, 15.994343, 9.622164,
                    0.285901, 0.430055, 0.091150,  0.254594]).reshape(-1, 2)
    dst = np.array([1.002114, 1.129644, 1.521742, 1.846002,
                    1.084332, 0.275134, 0.293328, 0.588992,
                    0.839509, 0.087290, 1.779735, 1.116857,
                    0.878616, 0.602447, 0.642616, 1.028681]).reshape(-1, 2)

    tform = estimate_transform('fundamental', src, dst)

    # Reference values obtained using COLMAP SfM library.
    tform_ref = np.array([[-0.217859, 0.419282, -0.0343075],
                          [-0.0717941, 0.0451643, 0.0216073],
                          [0.248062, -0.429478, 0.0221019]])
    assert_almost_equal(tform.params, tform_ref, 6)


def test_fundamental_matrix_residuals():
    essential_matrix_tform = EssentialMatrixTransform(
        rotation=np.eye(3), translation=np.array([1, 0, 0]))
    tform = FundamentalMatrixTransform()
    tform.params = essential_matrix_tform.params
    src = np.array([[0, 0], [0, 0], [0, 0]])
    dst = np.array([[2, 0], [2, 1], [2, 2]])
    assert_almost_equal(tform.residuals(src, dst)**2, [0, 0.5, 2])


def test_fundamental_matrix_forward():
    essential_matrix_tform = EssentialMatrixTransform(
        rotation=np.eye(3), translation=np.array([1, 0, 0]))
    tform = FundamentalMatrixTransform()
    tform.params = essential_matrix_tform.params
    src = np.array([[0, 0], [0, 1], [1, 1]])
    assert_almost_equal(tform(src), [[0, -1, 0], [0, -1, 1], [0, -1, 1]])


def test_fundamental_matrix_inverse():
    essential_matrix_tform = EssentialMatrixTransform(
        rotation=np.eye(3), translation=np.array([1, 0, 0]))
    tform = FundamentalMatrixTransform()
    tform.params = essential_matrix_tform.params
    src = np.array([[0, 0], [0, 1], [1, 1]])
    assert_almost_equal(tform.inverse(src), [[0, 1, 0], [0, 1, -1], [0, 1, -1]])


def test_essential_matrix_init():
    tform = EssentialMatrixTransform(rotation=np.eye(3),
                                     translation=np.array([0, 0, 1]))
    assert_equal(tform.params,
                 np.array([0, -1, 0, 1, 0, 0, 0, 0, 0]).reshape(3, 3))


def test_essential_matrix_estimation():
    src = np.array([1.839035, 1.924743, 0.543582,  0.375221,
                    0.473240, 0.142522, 0.964910,  0.598376,
                    0.102388, 0.140092, 15.994343, 9.622164,
                    0.285901, 0.430055, 0.091150,  0.254594]).reshape(-1, 2)
    dst = np.array([1.002114, 1.129644, 1.521742, 1.846002,
                    1.084332, 0.275134, 0.293328, 0.588992,
                    0.839509, 0.087290, 1.779735, 1.116857,
                    0.878616, 0.602447, 0.642616, 1.028681]).reshape(-1, 2)

    tform = estimate_transform('essential', src, dst)

    # Reference values obtained using COLMAP SfM library.
    tform_ref = np.array([[-0.0811666, 0.255449, -0.0478999],
                          [-0.192392, -0.0531675, 0.119547],
                          [0.177784, -0.22008, -0.015203]])
    assert_almost_equal(tform.params, tform_ref, 6)


def test_essential_matrix_forward():
    tform = EssentialMatrixTransform(rotation=np.eye(3),
                                     translation=np.array([1, 0, 0]))
    src = np.array([[0, 0], [0, 1], [1, 1]])
    assert_almost_equal(tform(src), [[0, -1, 0], [0, -1, 1], [0, -1, 1]])


def test_essential_matrix_inverse():
    tform = EssentialMatrixTransform(rotation=np.eye(3),
                                     translation=np.array([1, 0, 0]))
    src = np.array([[0, 0], [0, 1], [1, 1]])
    assert_almost_equal(tform.inverse(src), [[0, 1, 0], [0, 1, -1], [0, 1, -1]])


def test_essential_matrix_residuals():
    tform = EssentialMatrixTransform(rotation=np.eye(3),
                                     translation=np.array([1, 0, 0]))
    src = np.array([[0, 0], [0, 0], [0, 0]])
    dst = np.array([[2, 0], [2, 1], [2, 2]])
    assert_almost_equal(tform.residuals(src, dst)**2, [0, 0.5, 2])


def test_projective_estimation():
    # exact solution
    tform = estimate_transform('projective', SRC[:4, :], DST[:4, :])
    assert_almost_equal(tform(SRC[:4, :]), DST[:4, :])

    # over-determined
    tform2 = estimate_transform('projective', SRC, DST)
    assert_almost_equal(tform2.inverse(tform2(SRC)), SRC)

    # via estimate method
    tform3 = ProjectiveTransform()
    tform3.estimate(SRC, DST)
    assert_almost_equal(tform3.params, tform2.params)


def test_projective_init():
    tform = estimate_transform('projective', SRC, DST)
    # init with transformation matrix
    tform2 = ProjectiveTransform(tform.params)
    assert_almost_equal(tform2.params, tform.params)


def test_polynomial_estimation():
    # over-determined
    tform = estimate_transform('polynomial', SRC, DST, order=10)
    assert_almost_equal(tform(SRC), DST, 6)

    # via estimate method
    tform2 = PolynomialTransform()
    tform2.estimate(SRC, DST, order=10)
    assert_almost_equal(tform2.params, tform.params)


def test_polynomial_init():
    tform = estimate_transform('polynomial', SRC, DST, order=10)
    # init with transformation parameters
    tform2 = PolynomialTransform(tform.params)
    assert_almost_equal(tform2.params, tform.params)


def test_polynomial_default_order():
    tform = estimate_transform('polynomial', SRC, DST)
    tform2 = estimate_transform('polynomial', SRC, DST, order=2)
    assert_almost_equal(tform2.params, tform.params)


def test_polynomial_inverse():
    assert_raises(Exception, PolynomialTransform().inverse, 0)


def test_union():
    tform1 = SimilarityTransform(scale=0.1, rotation=0.3)
    tform2 = SimilarityTransform(scale=0.1, rotation=0.9)
    tform3 = SimilarityTransform(scale=0.1 ** 2, rotation=0.3 + 0.9)
    tform = tform1 + tform2
    assert_almost_equal(tform.params, tform3.params)

    tform1 = AffineTransform(scale=(0.1, 0.1), rotation=0.3)
    tform2 = SimilarityTransform(scale=0.1, rotation=0.9)
    tform3 = SimilarityTransform(scale=0.1 ** 2, rotation=0.3 + 0.9)
    tform = tform1 + tform2
    assert_almost_equal(tform.params, tform3.params)
    assert tform.__class__ == ProjectiveTransform

    tform = AffineTransform(scale=(0.1, 0.1), rotation=0.3)
    assert_almost_equal((tform + tform.inverse).params, np.eye(3))


def test_union_differing_types():
    tform1 = SimilarityTransform()
    tform2 = PolynomialTransform()
    assert_raises(TypeError, tform1.__add__, tform2)


def test_geometric_tform():
    tform = GeometricTransform()
    assert_raises(NotImplementedError, tform, 0)
    assert_raises(NotImplementedError, tform.inverse, 0)
    assert_raises(NotImplementedError, tform.__add__, 0)


def test_invalid_input():
    assert_raises(ValueError, ProjectiveTransform, np.zeros((2, 3)))
    assert_raises(ValueError, AffineTransform, np.zeros((2, 3)))
    assert_raises(ValueError, SimilarityTransform, np.zeros((2, 3)))
    assert_raises(ValueError, EuclideanTransform, np.zeros((2, 3)))

    assert_raises(ValueError, AffineTransform,
                  matrix=np.zeros((2, 3)), scale=1)
    assert_raises(ValueError, SimilarityTransform,
                  matrix=np.zeros((2, 3)), scale=1)
    assert_raises(ValueError, EuclideanTransform,
                  matrix=np.zeros((2, 3)), translation=(0, 0))

    assert_raises(ValueError, PolynomialTransform, np.zeros((3, 3)))

    assert_raises(ValueError, FundamentalMatrixTransform,
                  matrix=np.zeros((3, 2)))
    assert_raises(ValueError, EssentialMatrixTransform,
                  matrix=np.zeros((3, 2)))
    assert_raises(ValueError, EssentialMatrixTransform,
                  rotation=np.zeros((3, 2)))
    assert_raises(ValueError, EssentialMatrixTransform,
                  rotation=np.zeros((3, 3)))
    assert_raises(ValueError, EssentialMatrixTransform,
                  rotation=np.eye(3))
    assert_raises(ValueError, EssentialMatrixTransform,
                  rotation=np.eye(3), translation=np.zeros((2,)))
    assert_raises(ValueError, EssentialMatrixTransform,
                  rotation=np.eye(3), translation=np.zeros((2,)))
    assert_raises(ValueError, EssentialMatrixTransform,
                  rotation=np.eye(3), translation=np.zeros((3,)))


def test_degenerate():
    src = dst = np.zeros((10, 2))

    tform = SimilarityTransform()
    tform.estimate(src, dst)
    assert np.all(np.isnan(tform.params))

    tform = AffineTransform()
    tform.estimate(src, dst)
    assert np.all(np.isnan(tform.params))

    tform = ProjectiveTransform()
    tform.estimate(src, dst)
    assert np.all(np.isnan(tform.params))


if __name__ == "__main__":
    from numpy.testing import run_module_suite
    run_module_suite()
