JupyterHuck
===========

A data browser which has a tree structure.This browser also controls
matplotlib graphs embedded in PyQt5 windows.

Installation
------------

::

    pip install JupyterHuck

Usage
-----

.. code:: python

    %gui qt ### necessary when using in Jupyter
    from JupyterHuck.MyView import getRoot
    from JupyterHuck.MyGraph import MyGraphWindow

    r=getRoot()

    a='This is a string'
    r.cur.add(a)

    graph=MyGraphWindow()
    graph.plot([1,2,3],[1,2,1])
    r.cur.add(graph)

    r.save()

.. figure:: https://github.com/threemeninaboat3247/JupyterHuck/blob/master/JupyterHuck.png
   :alt: 

