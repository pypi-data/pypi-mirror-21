Data Partitioner
================

Simple project that can be used to consistently partition a data set
into two parts - a test set and a training set. There are also helpful
methods that provide a way to partition into more groups of elements.

Installation
============

The easiest way to install this module is to install it via ``pip``:

::

    $ pip install data_partitioner

Usage
=====

Using this module is dead simple. The main module (``DatasetSuplier``)
offers two methods that return the training set (``training_set()``) or
the test set (``test_set()``). Both of these methods are consitent, so
no matter how many times you call them on the same object, they will
return the same set of elements back.

You have two configuration options you can specify:

-  ``training_percent`` - the percent of the dataset used for the
   training set. It defaults to ``0.8``.
-  ``partitioning_function`` - the function that's used to partition the
   dataset.
-  It defaults to ``data_partitioner.pseudorandom_function``, which will
   randomly assign every element of the dataset to either the test set
   or the training set.
-  Another useful existing option you can set it to is
   ``data_partitioner.LinearFakeRandomFunction``, which will make sure
   that no elements in the training set come after any elements of the
   test set.
-  You can also manually write this callable, which will take one
   parameter as input - the index of the element currently considered.

Example
=======

::

    from data_partitioner import DatasetSuplier

    dataset = [
        ('Alice', 10, 23, 401),
        ('Bob', 20, 40, 812),
        ('Christine', 41, 92, 533),
        ('Dave', 843, 12, -5),
        ('Elizabeth', 682, 33, -7),
        ('Fred', 95, 642, 34),
    ]
    suplier = DatasetSuplier(dataset)

    for iteration in range(100):
        for element in suplier.training_set():
            do_train(element[1])
    for element in suplier.test_set():
        do_evaluate(element[1])
