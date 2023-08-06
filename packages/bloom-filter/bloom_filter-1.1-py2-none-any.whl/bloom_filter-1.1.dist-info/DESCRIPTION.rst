A pure python bloom filter (low storage requirement, probabilistic
set datastructure) is provided.  It is known to work on CPython 2.x,
CPython 3.x, Pypy and Jython.

Includes mmap, in-memory and disk-seek backends.

The user specifies the desired maximum number of elements and the
desired maximum false positive probability, and the module
calculates the rest.


