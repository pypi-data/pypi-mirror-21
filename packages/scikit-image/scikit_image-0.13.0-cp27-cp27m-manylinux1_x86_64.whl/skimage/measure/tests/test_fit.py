import numpy as np
from numpy.testing import assert_equal, assert_almost_equal, assert_array_less
from numpy.testing import assert_raises, assert_array_less
from skimage.measure import LineModelND, CircleModel, EllipseModel, ransac
from skimage.transform import AffineTransform
from skimage.measure.fit import _dynamic_max_trials
from skimage._shared._warnings import expected_warnings


def test_line_model_invalid_input():
    assert_raises(ValueError, LineModelND().estimate, np.empty((1, 3)))


def test_line_model_predict():
    model = LineModelND()
    model.params = ((0, 0), (1, 1))
    x = np.arange(-10, 10)
    y = model.predict_y(x)
    assert_almost_equal(x, model.predict_x(y))


def test_line_model_estimate():
    # generate original data without noise
    model0 = LineModelND()
    model0.params = ((0, 0), (1, 1))
    x0 = np.arange(-100, 100)
    y0 = model0.predict_y(x0)

    data = np.column_stack([x0, y0])

    # estimate parameters of noisy data
    model_est = LineModelND()
    model_est.estimate(data)

    # test whether estimated parameters almost equal original parameters
    random_state = np.random.RandomState(1234)
    x = random_state.rand(100, 2)
    assert_almost_equal(model0.predict(x), model_est.predict(x), 1)


def test_line_model_residuals():
    model = LineModelND()
    model.params = (np.array([0, 0]), np.array([0, 1]))
    assert_equal(model.residuals(np.array([[0, 0]])), 0)
    assert_equal(model.residuals(np.array([[0, 10]])), 0)
    assert_equal(model.residuals(np.array([[10, 0]])), 10)
    model.params = (np.array([-2, 0]), np.array([1, 1])  / np.sqrt(2))
    assert_equal(model.residuals(np.array([[0, 0]])), np.sqrt(2))
    assert_almost_equal(model.residuals(np.array([[-4, 0]])), np.sqrt(2))


def test_line_model_under_determined():
    data = np.empty((1, 2))
    assert_raises(ValueError, LineModelND().estimate, data)


def test_line_modelND_invalid_input():
    assert_raises(ValueError, LineModelND().estimate, np.empty((5, 1)))


def test_line_modelND_predict():
    model = LineModelND()
    model.params = (np.array([0, 0]), np.array([0.2, 0.98]))
    x = np.arange(-10, 10)
    y = model.predict_y(x)
    assert_almost_equal(x, model.predict_x(y))


def test_line_modelND_estimate():
    # generate original data without noise
    model0 = LineModelND()
    model0.params = (np.array([0,0,0], dtype='float'),
                         np.array([1,1,1], dtype='float')/np.sqrt(3))
    # we scale the unit vector with a factor 10 when generating points on the
    # line in order to compensate for the scale of the random noise
    data0 = (model0.params[0] +
             10 * np.arange(-100,100)[...,np.newaxis] * model0.params[1])

    # add gaussian noise to data
    random_state = np.random.RandomState(1234)
    data = data0 + random_state.normal(size=data0.shape)

    # estimate parameters of noisy data
    model_est = LineModelND()
    model_est.estimate(data)

    # test whether estimated parameters are correct
    # we use the following geometric property: two aligned vectors have
    # a cross-product equal to zero
    # test if direction vectors are aligned
    assert_almost_equal(np.linalg.norm(np.cross(model0.params[1],
                                                model_est.params[1])), 0, 1)
    # test if origins are aligned with the direction
    a = model_est.params[0] - model0.params[0]
    if np.linalg.norm(a) > 0:
        a /= np.linalg.norm(a)
    assert_almost_equal(np.linalg.norm(np.cross(model0.params[1], a)), 0, 1)


def test_line_modelND_residuals():
    model = LineModelND()
    model.params = (np.array([0, 0, 0]), np.array([0, 0, 1]))
    assert_equal(abs(model.residuals(np.array([[0, 0, 0]]))), 0)
    assert_equal(abs(model.residuals(np.array([[0, 0, 1]]))), 0)
    assert_equal(abs(model.residuals(np.array([[10, 0, 0]]))), 10)


def test_line_modelND_under_determined():
    data = np.empty((1, 3))
    assert_raises(ValueError, LineModelND().estimate, data)


def test_circle_model_invalid_input():
    assert_raises(ValueError, CircleModel().estimate, np.empty((5, 3)))


def test_circle_model_predict():
    model = CircleModel()
    r = 5
    model.params = (0, 0, r)
    t = np.arange(0, 2 * np.pi, np.pi / 2)

    xy = np.array(((5, 0), (0, 5), (-5, 0), (0, -5)))
    assert_almost_equal(xy, model.predict_xy(t))


def test_circle_model_estimate():
    # generate original data without noise
    model0 = CircleModel()
    model0.params = (10, 12, 3)
    t = np.linspace(0, 2 * np.pi, 1000)
    data0 = model0.predict_xy(t)

    # add gaussian noise to data
    random_state = np.random.RandomState(1234)
    data = data0 + random_state.normal(size=data0.shape)

    # estimate parameters of noisy data
    model_est = CircleModel()
    model_est.estimate(data)

    # test whether estimated parameters almost equal original parameters
    assert_almost_equal(model0.params, model_est.params, 1)


def test_circle_model_residuals():
    model = CircleModel()
    model.params = (0, 0, 5)
    assert_almost_equal(abs(model.residuals(np.array([[5, 0]]))), 0)
    assert_almost_equal(abs(model.residuals(np.array([[6, 6]]))),
                        np.sqrt(2 * 6**2) - 5)
    assert_almost_equal(abs(model.residuals(np.array([[10, 0]]))), 5)


def test_ellipse_model_invalid_input():
    assert_raises(ValueError, EllipseModel().estimate, np.empty((5, 3)))


def test_ellipse_model_predict():
    model = EllipseModel()
    model.params = (0, 0, 5, 10, 0)
    t = np.arange(0, 2 * np.pi, np.pi / 2)

    xy = np.array(((5, 0), (0, 10), (-5, 0), (0, -10)))
    assert_almost_equal(xy, model.predict_xy(t))


def test_ellipse_model_estimate():
    for angle in range(0, 180, 15):
        rad = np.deg2rad(angle)
        # generate original data without noise
        model0 = EllipseModel()
        model0.params = (10, 20, 15, 25, rad)
        t = np.linspace(0, 2 * np.pi, 100)
        data0 = model0.predict_xy(t)

        # add gaussian noise to data
        random_state = np.random.RandomState(1234)
        data = data0 + random_state.normal(size=data0.shape)

        # estimate parameters of noisy data
        model_est = EllipseModel()
        model_est.estimate(data)

        # test whether estimated parameters almost equal original parameters
        assert_almost_equal(model0.params[:2], model_est.params[:2], 0)
        res = model_est.residuals(data0)
        assert_array_less(res, np.ones(res.shape))


def test_ellipse_model_estimate_from_data():
    data = np.array([
        [264, 854], [265, 875], [268, 863], [270, 857], [275, 905], [285, 915],
        [305, 925], [324, 934], [335, 764], [336, 915], [345, 925], [345, 945],
        [354, 933], [355, 745], [364, 936], [365, 754], [375, 745], [375, 735],
        [385, 736], [395, 735], [394, 935], [405, 727], [415, 736], [415, 727],
        [425, 727], [426, 929], [435, 735], [444, 933], [445, 735], [455, 724],
        [465, 934], [465, 735], [475, 908], [475, 726], [485, 753], [485, 728],
        [492, 762], [495, 745], [491, 910], [493, 909], [499, 904], [505, 905],
        [504, 747], [515, 743], [516, 752], [524, 855], [525, 844], [525, 885],
        [533, 845], [533, 873], [535, 883], [545, 874], [543, 864], [553, 865],
        [553, 845], [554, 825], [554, 835], [563, 845], [565, 826], [563, 855],
        [563, 795], [565, 735], [573, 778], [572, 815], [574, 804], [575, 665],
        [575, 685], [574, 705], [574, 745], [575, 875], [572, 732], [582, 795],
        [579, 709], [583, 805], [583, 854], [586, 755], [584, 824], [585, 655],
        [581, 718], [586, 844], [585, 915], [587, 905], [594, 824], [593, 855],
        [590, 891], [594, 776], [596, 767], [593, 763], [603, 785], [604, 775],
        [603, 885], [605, 753], [605, 655], [606, 935], [603, 761], [613, 802],
        [613, 945], [613, 965], [615, 693], [617, 665], [623, 962], [624, 972],
        [625, 995], [633, 673], [633, 965], [633, 683], [633, 692], [633, 954],
        [634, 1016], [635, 664], [641, 804], [637, 999], [641, 956], [643, 946],
        [643, 926], [644, 975], [643, 655], [646, 705], [651, 664], [651, 984],
        [647, 665], [651, 715], [651, 725], [651, 734], [647, 809], [651, 825],
        [651, 873], [647, 900], [652, 917], [651, 944], [652, 742], [648, 811],
        [651, 994], [652, 783], [650, 911], [654, 879]])

    # estimate parameters of real data
    model = EllipseModel()
    model.estimate(data)

    # test whether estimated parameters are smaller then 1000, so means stable
    assert_array_less(np.abs(model.params[:4]), np.array([2e3] * 4))


def test_ellipse_model_estimate_failers():
    # estimate parameters of real data
    model = EllipseModel()
    assert not model.estimate(np.ones((5, 2)))
    assert not model.estimate(np.array([[50, 80], [51, 81], [52, 80]]))


def test_ellipse_model_residuals():
    model = EllipseModel()
    # vertical line through origin
    model.params = (0, 0, 10, 5, 0)
    assert_almost_equal(abs(model.residuals(np.array([[10, 0]]))), 0)
    assert_almost_equal(abs(model.residuals(np.array([[0, 5]]))), 0)
    assert_almost_equal(abs(model.residuals(np.array([[0, 10]]))), 5)


def test_ransac_shape():
    # generate original data without noise
    model0 = CircleModel()
    model0.params = (10, 12, 3)
    t = np.linspace(0, 2 * np.pi, 1000)
    data0 = model0.predict_xy(t)

    # add some faulty data
    outliers = (10, 30, 200)
    data0[outliers[0], :] = (1000, 1000)
    data0[outliers[1], :] = (-50, 50)
    data0[outliers[2], :] = (-100, -10)

    # estimate parameters of corrupted data
    model_est, inliers = ransac(data0, CircleModel, 3, 5,
                                random_state=1)

    # test whether estimated parameters equal original parameters
    assert_equal(model0.params, model_est.params)
    for outlier in outliers:
        assert outlier not in inliers


def test_ransac_geometric():
    random_state = np.random.RandomState(1)

    # generate original data without noise
    src = 100 * random_state.random_sample((50, 2))
    model0 = AffineTransform(scale=(0.5, 0.3), rotation=1,
                             translation=(10, 20))
    dst = model0(src)

    # add some faulty data
    outliers = (0, 5, 20)
    dst[outliers[0]] = (10000, 10000)
    dst[outliers[1]] = (-100, 100)
    dst[outliers[2]] = (50, 50)

    # estimate parameters of corrupted data
    model_est, inliers = ransac((src, dst), AffineTransform, 2, 20,
                                random_state=random_state)

    # test whether estimated parameters equal original parameters
    assert_almost_equal(model0.params, model_est.params)
    assert np.all(np.nonzero(inliers == False)[0] == outliers)


def test_ransac_is_data_valid():

    is_data_valid = lambda data: data.shape[0] > 2
    model, inliers = ransac(np.empty((10, 2)), LineModelND, 2, np.inf,
                            is_data_valid=is_data_valid, random_state=1)
    assert_equal(model, None)
    assert_equal(inliers, None)


def test_ransac_is_model_valid():

    def is_model_valid(model, data):
        return False
    model, inliers = ransac(np.empty((10, 2)), LineModelND, 2, np.inf,
                            is_model_valid=is_model_valid, random_state=1)
    assert_equal(model, None)
    assert_equal(inliers, None)


def test_ransac_dynamic_max_trials():
    # Numbers hand-calculated and confirmed on page 119 (Table 4.3) in
    #   Hartley, R.~I. and Zisserman, A., 2004,
    #   Multiple View Geometry in Computer Vision, Second Edition,
    #   Cambridge University Press, ISBN: 0521540518

    # e = 0%, min_samples = X
    assert_equal(_dynamic_max_trials(100, 100, 2, 0.99), 1)

    # e = 5%, min_samples = 2
    assert_equal(_dynamic_max_trials(95, 100, 2, 0.99), 2)
    # e = 10%, min_samples = 2
    assert_equal(_dynamic_max_trials(90, 100, 2, 0.99), 3)
    # e = 30%, min_samples = 2
    assert_equal(_dynamic_max_trials(70, 100, 2, 0.99), 7)
    # e = 50%, min_samples = 2
    assert_equal(_dynamic_max_trials(50, 100, 2, 0.99), 17)

    # e = 5%, min_samples = 8
    assert_equal(_dynamic_max_trials(95, 100, 8, 0.99), 5)
    # e = 10%, min_samples = 8
    assert_equal(_dynamic_max_trials(90, 100, 8, 0.99), 9)
    # e = 30%, min_samples = 8
    assert_equal(_dynamic_max_trials(70, 100, 8, 0.99), 78)
    # e = 50%, min_samples = 8
    assert_equal(_dynamic_max_trials(50, 100, 8, 0.99), 1177)

    # e = 0%, min_samples = 5
    assert_equal(_dynamic_max_trials(1, 100, 5, 0), 0)
    assert_equal(_dynamic_max_trials(1, 100, 5, 1), np.inf)


def test_ransac_invalid_input():
    assert_raises(ValueError, ransac, np.zeros((10, 2)), None, min_samples=2,
                  residual_threshold=0, max_trials=-1)
    assert_raises(ValueError, ransac, np.zeros((10, 2)), None, min_samples=2,
                  residual_threshold=0, stop_probability=-1)
    assert_raises(ValueError, ransac, np.zeros((10, 2)), None, min_samples=2,
                  residual_threshold=0, stop_probability=1.01)


if __name__ == "__main__":
    np.testing.run_module_suite()
