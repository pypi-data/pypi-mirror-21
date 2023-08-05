

.. _sphx_glr_auto_examples_filters_plot_frangi.py:


=============
Frangi filter
=============

The Frangi and hybrid Hessian filters can be used to detect continuous
edges, such as vessels, wrinkles, and rivers.




.. code-block:: pytb

    Traceback (most recent call last):
      File "/Users/jni/projects/scikit-image/doc/source/../ext/sphinx_gallery/gen_rst.py", line 498, in execute_script
        exec(code_block, example_globals)
      File "<string>", line 3, in <module>
    ImportError: cannot import name 'frangi'





.. code-block:: python


    from skimage.data import camera
    from skimage.filters import frangi, hessian

    import matplotlib.pyplot as plt

    image = camera()

    fig, ax = plt.subplots(ncols=3, subplot_kw={'adjustable': 'box-forced'})

    ax[0].imshow(image, cmap=plt.cm.gray)
    ax[0].set_title('Original image')

    ax[1].imshow(frangi(image), cmap=plt.cm.gray)
    ax[1].set_title('Frangi filter result')

    ax[2].imshow(hessian(image), cmap=plt.cm.gray)
    ax[2].set_title('Hybrid Hessian filter result')

    for a in ax:
        a.axis('off')

    plt.tight_layout()

**Total running time of the script:**
(0 minutes 0.000 seconds)



.. container:: sphx-glr-download

    **Download Python source code:** :download:`plot_frangi.py <plot_frangi.py>`


.. container:: sphx-glr-download

    **Download IPython notebook:** :download:`plot_frangi.ipynb <plot_frangi.ipynb>`
