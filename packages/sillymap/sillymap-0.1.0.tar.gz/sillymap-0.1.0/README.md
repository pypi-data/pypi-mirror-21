# Sillymap

A silly implementation of a short read mapper for the course DD3436.

## Installation

     pip install sillymap

## Example

    $ sillymap index
    This should index your input fasta

    $ sillymap map
    This should map your sequences against an index

## Course goals and content

* Distributed project handling, including using version control system for source code.
    - Git
    - Github
    - Pypi
    - bioconda
* Important libraries in Python.
    - Pandas
    - Biopython
    - scikit-bio
    - Jupyter notebook
    - Matplotlib
* Efficient programming in Python.
    - Numpy
    - Scipy
    - profiling
    - Pypy
* Parallel programming in Python.
    - threads
    - multiprocessing
    - MPI
* Efficient debugging.
    - ipdb


## Assignments

Assignment 1:
A repository on Github with a Readme, license and setup.py. The program itself only prints a friendly message. Bonus: Travis CI.

Assignment 2:
A release on github where the program can map a few exactly matching short reads against a longer sequence, using the burrows wheeler transform and the FM-index (http://alexbowe.com/fm-index/) where rank can be stored as the table Occ in (https://en.wikipedia.org/wiki/FM-index). This assignment should include a test suite.

Assignment 3:
Using the test suite for assignment 2, modify the code to make it run faster/more efficiently. Create two versions:
 1. Make it run with pypy.
 2. Using numpy, scipy or other libraries to speed up the code.

Both scripts should pass integration tests in Travis.

Make a report explaining the optimizations and the improvements.

Assignment 4:
Parallelize the code using both:
 1. Multiple cores on one computer.
 2. Using multiple computers (MPI).

Make a report explaining the optimizations and the improvements.
