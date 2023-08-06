.. kv.python documentation master file, created by
   sphinx-quickstart on Sun Feb 22 21:47:03 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the nosqldb package
==============================

.. toctree::
   :maxdepth: 2

.. automodule:: nosqldb

Store Operations
----------------

This section contains classes used to configure and manage connections to
the proxy server and to the Oracle NoSQL Database Store.

Factory
^^^^^^^
.. autoclass:: Factory
    :members:

ProxyConfig
^^^^^^^^^^^
.. autoclass:: ProxyConfig
    :members:

Store
^^^^^
.. autoclass:: Store
    :members:

StoreConfig
^^^^^^^^^^^
.. autoclass:: StoreConfig
    :members:

Reads
-----

This section contains classes used to manage read operations performed
against the store.

Direction
^^^^^^^^^
.. autoclass:: Direction
    :members:

FieldRange
^^^^^^^^^^
.. autoclass:: FieldRange
    :members:

MultiRowOptions
^^^^^^^^^^^^^^^
.. autoclass:: MultiRowOptions
    :members:

ReadOptions
^^^^^^^^^^^
.. autoclass:: ReadOptions
    :members:

Row
^^^
.. autoclass:: Row
    :members:

ResultIterator
^^^^^^^^^^^^^^
.. autoclass:: ResultIterator
    :members:

TableIteratorOptions
^^^^^^^^^^^^^^^^^^^^
.. autoclass:: TableIteratorOptions
    :members:

Consistency Guarantees
----------------------

This section contains classes used to define consistency guarantees that
are applied to read operations.

Consistency
^^^^^^^^^^^
.. autoclass:: Consistency
    :members:

SimpleConsistency
^^^^^^^^^^^^^^^^^
.. autoclass:: SimpleConsistency
    :members:

TimeConsistency
^^^^^^^^^^^^^^^
.. autoclass:: TimeConsistency
    :members:

VersionConsistency
^^^^^^^^^^^^^^^^^^
.. autoclass:: VersionConsistency
    :members:


Writes
------

This section contains classes used to manage write operations performed
against the store.

ExecutionFuture
^^^^^^^^^^^^^^^
.. autoclass:: ExecutionFuture
    :members:

Durability
^^^^^^^^^^
.. autoclass:: Durability
    :members:

Result
^^^^^^^^^^^^^^^
.. autoclass:: Result
    :members:

StatementResult
^^^^^^^^^^^^^^^
.. autoclass:: StatementResult
    :members:

WriteOptions
^^^^^^^^^^^^
.. autoclass:: WriteOptions
    :members:

Grouped Table Operations
------------------------

This sections contains classes used to create and execute a sequence of
write operations. A sequence of write operations is an atomic unit: either
all the operations succeed or none of them do.

Operation
^^^^^^^^^
.. autoclass:: Operation
    :members:

OperationResult
^^^^^^^^^^^^^^^
.. autoclass:: OperationResult
    :members:

OperationType
^^^^^^^^^^^^^
.. autoclass:: OperationType
    :members:

Exceptions
----------
This section contains the exceptions that can be raised by the methods
contained in the nosqldb module.

CancellationException
^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: CancellationException
    :members:

ConsistencyException
^^^^^^^^^^^^^^^^^^^^
.. autoclass:: ConsistencyException
    :members:

ConnectionException
^^^^^^^^^^^^^^^^^^^
.. autoclass:: ConnectionException
    :members:

DurabilityException
^^^^^^^^^^^^^^^^^^^
.. autoclass:: DurabilityException
    :members:

ExecutionException
^^^^^^^^^^^^^^^^^^^
.. autoclass:: ExecutionException
    :members:

FaultException
^^^^^^^^^^^^^^
.. autoclass:: FaultException
    :members:

IllegalArgumentException
^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: IllegalArgumentException
    :members:

InterruptionException
^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: InterruptionException
    :members:

OperationExecutionException
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: OperationExecutionException
    :members:

ProxyException
^^^^^^^^^^^^^^
.. autoclass:: ProxyException
    :members:

RequestTimeoutException
^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: RequestTimeoutException
    :members:

TimeoutException
^^^^^^^^^^^^^^^^
.. autoclass:: TimeoutException
    :members:

UnsupportedOperationException
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: UnsupportedOperationException
    :members:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
