
import os
from skimage import data, img_as_float, io, img_as_uint

from skimage.viewer import ImageViewer
from skimage.viewer.qt import QtGui, QtCore, has_qt
from skimage.viewer.widgets import (
    Slider, OKCancelButtons, SaveButtons, ComboBox, CheckBox, Text)
from skimage.viewer.plugins.base import Plugin

from numpy.testing import assert_almost_equal, assert_equal
from numpy.testing.decorators import skipif
from skimage._shared._warnings import expected_warnings


def get_image_viewer():
    image = data.coins()
    viewer = ImageViewer(img_as_float(image))
    viewer += Plugin()
    return viewer


@skipif(not has_qt)
def test_check_box():
    viewer = get_image_viewer()
    cb = CheckBox('hello', value=True, alignment='left')
    viewer.plugins[0] += cb

    assert_equal(cb.val, True)
    cb.val = False
    assert_equal(cb.val, False)
    cb.val = 1
    assert_equal(cb.val, True)
    cb.val = 0
    assert_equal(cb.val, False)


@skipif(not has_qt)
def test_combo_box():
    viewer = get_image_viewer()
    cb = ComboBox('hello', ('a', 'b', 'c'))
    viewer.plugins[0] += cb

    assert_equal(str(cb.val), 'a')
    assert_equal(cb.index, 0)
    cb.index = 2
    assert_equal(str(cb.val), 'c'),
    assert_equal(cb.index, 2)


@skipif(not has_qt)
def test_text_widget():
    viewer = get_image_viewer()
    txt = Text('hello', 'hello, world!')
    viewer.plugins[0] += txt

    assert_equal(str(txt.text), 'hello, world!')
    txt.text = 'goodbye, world!'
    assert_equal(str(txt.text), 'goodbye, world!')


@skipif(not has_qt)
def test_slider_int():
    viewer = get_image_viewer()
    sld = Slider('radius', 2, 10, value_type='int')
    viewer.plugins[0] += sld

    assert_equal(sld.val, 4)
    sld.val = 6
    assert_equal(sld.val, 6)
    sld.editbox.setText('5')
    sld._on_editbox_changed()
    assert_equal(sld.val, 5)


@skipif(not has_qt)
def test_slider_float():
    viewer = get_image_viewer()
    sld = Slider('alpha', 2.1, 3.1, value=2.1, value_type='float',
                 orientation='vertical', update_on='move')
    viewer.plugins[0] += sld

    assert_equal(sld.val, 2.1)
    sld.val = 2.5
    assert_almost_equal(sld.val, 2.5, 2)
    sld.editbox.setText('0.1')
    sld._on_editbox_changed()
    assert_almost_equal(sld.val, 2.5, 2)


@skipif(not has_qt)
def test_save_buttons():
    viewer = get_image_viewer()
    sv = SaveButtons()
    viewer.plugins[0] += sv

    import tempfile
    fid, filename = tempfile.mkstemp(suffix='.png')
    os.close(fid)

    timer = QtCore.QTimer()
    timer.singleShot(100, QtGui.QApplication.quit)

    # exercise the button clicks
    sv.save_stack.click()
    sv.save_file.click()

    # call the save functions directly
    sv.save_to_stack()
    with expected_warnings(['precision loss']):
        sv.save_to_file(filename)

    img = data.imread(filename)

    with expected_warnings(['precision loss']):
        assert_almost_equal(img, img_as_uint(viewer.image))

    img = io.pop()
    assert_almost_equal(img, viewer.image)

    os.remove(filename)


@skipif(not has_qt)
def test_ok_buttons():
    viewer = get_image_viewer()
    ok = OKCancelButtons()
    viewer.plugins[0] += ok

    ok.update_original_image(),
    ok.close_plugin()

