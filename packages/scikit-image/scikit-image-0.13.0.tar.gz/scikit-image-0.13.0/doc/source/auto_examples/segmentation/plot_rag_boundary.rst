

.. _sphx_glr_auto_examples_segmentation_plot_rag_boundary.py:


==========================
Region Boundary based RAGs
==========================

Construct a region boundary RAG with the ``rag_boundary`` function. The
function  :py:func:`skimage.future.graph.rag_boundary` takes an
``edge_map`` argument, which gives the significance of a feature (such as
edges) being present at each pixel. In a region boundary RAG, the edge weight
between two regions is the average value of the corresponding pixels in
``edge_map`` along their shared boundary.





.. code-block:: pytb

    Traceback (most recent call last):
      File "/Users/jni/projects/scikit-image/doc/source/../ext/sphinx_gallery/gen_rst.py", line 498, in execute_script
        exec(code_block, example_globals)
      File "<string>", line 14, in <module>
    AttributeError: module 'skimage.future.graph' has no attribute 'show_rag'





.. code-block:: python

    from skimage.future import graph
    from skimage import data, segmentation, color, filters, io
    from matplotlib import pyplot as plt


    img = data.coffee()
    gimg = color.rgb2gray(img)

    labels = segmentation.slic(img, compactness=30, n_segments=400)
    edges = filters.sobel(gimg)
    edges_rgb = color.gray2rgb(edges)

    g = graph.rag_boundary(labels, edges)
    lc = graph.show_rag(labels, g, edges_rgb, img_cmap=None, edge_cmap='viridis',
                        edge_width=1.2)

    plt.colorbar(lc, fraction=0.03)
    io.show()

**Total running time of the script:**
(0 minutes 0.000 seconds)



.. container:: sphx-glr-download

    **Download Python source code:** :download:`plot_rag_boundary.py <plot_rag_boundary.py>`


.. container:: sphx-glr-download

    **Download IPython notebook:** :download:`plot_rag_boundary.ipynb <plot_rag_boundary.ipynb>`
