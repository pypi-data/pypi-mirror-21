`lathe <http://lathe.readthedocs.io/>`__
=====

Basic machine learning tools for BYU CS478.

.. image:: docs/images/lathe.gif
   :align: center

.. inclusion-marker-do-not-remove

requirements
------------

-  `python2.7 <https://www.python.org/downloads/>`__ or `python3.3+ <https://www.python.org/downloads/>`__
-  `pip <https://pip.pypa.io/en/stable/installing/>`__ (*optional*)

installation
------------

::

    pip install lathe

usage
-----

.. code:: python

    import lathe

    args = lathe.parse_args()
    attributes, data, targets = lathe.load(args.file, label_size=1)


documentation
-------------

http://lathe.readthedocs.io
