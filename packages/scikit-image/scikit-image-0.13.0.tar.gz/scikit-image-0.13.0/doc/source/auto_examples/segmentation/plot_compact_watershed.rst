

.. _sphx_glr_auto_examples_segmentation_plot_compact_watershed.py:


=============================================
Find Regular Segments Using Compact Watershed
=============================================

The watershed transform is commonly used as a starting point for many
segmentation algorithms. However, without a judicious choice of seeds, it
can produce very uneven fragment sizes, which can be difficult to deal with
in downstream analyses.

The *compact* watershed transform remedies this by favoring seeds that are
close to the pixel being considered.

Both algorithms are implemented in the :py:func:`skimage.morphology.watershed`
function. To use the compact form, simply pass a ``compactness`` value greater
than 0.




.. code-block:: pytb

    Traceback (most recent call last):
      File "/Users/jni/projects/scikit-image/doc/source/../ext/sphinx_gallery/gen_rst.py", line 498, in execute_script
        exec(code_block, example_globals)
      File "<string>", line 16, in <module>
    TypeError: watershed() got an unexpected keyword argument 'compactness'





.. code-block:: python


    import numpy as np
    from skimage import data, util, filters, color
    from skimage.morphology import watershed
    import matplotlib.pyplot as plt

    coins = data.coins()
    edges = filters.sobel(coins)

    grid = util.regular_grid(coins.shape, n_points=468)

    seeds = np.zeros(coins.shape, dtype=int)
    seeds[grid] = np.arange(seeds[grid].size).reshape(seeds[grid].shape) + 1

    w0 = watershed(edges, seeds)
    w1 = watershed(edges, seeds, compactness=0.01)

    fig, (ax0, ax1) = plt.subplots(1, 2)

    ax0.imshow(color.label2rgb(w0, coins))
    ax0.set_title('Classical watershed')

    ax1.imshow(color.label2rgb(w1, coins))
    ax1.set_title('Compact watershed')

    plt.show()

**Total running time of the script:**
(0 minutes 0.000 seconds)



.. container:: sphx-glr-download

    **Download Python source code:** :download:`plot_compact_watershed.py <plot_compact_watershed.py>`


.. container:: sphx-glr-download

    **Download IPython notebook:** :download:`plot_compact_watershed.ipynb <plot_compact_watershed.ipynb>`
