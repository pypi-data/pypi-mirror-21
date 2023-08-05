# This mock-up is called by ../tests/test_plugin.py
# to verify the behaviour of the plugin infrastructure

from skimage.io import ImageCollection


def imread(fname, dtype=None):
    assert fname == 'test.png'
    assert dtype == 'i4'


def imsave(fname, arr):
    assert fname == 'test.png'
    assert arr == [1, 2, 3]


def imshow(arr, plugin_arg=None):
    assert arr == [1, 2, 3]
    assert plugin_arg == (1, 2)


def imread_collection(x, conserve_memory=True):
    assert conserve_memory == False
    assert x == '*.png'
    return ImageCollection([0, 1], load_func=lambda x: x)


def imshow_collection(x):
    assert len(x) == 2
