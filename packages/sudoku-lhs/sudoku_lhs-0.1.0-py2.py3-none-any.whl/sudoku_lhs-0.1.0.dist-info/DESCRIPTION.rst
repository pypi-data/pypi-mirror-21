Latin hypercube sampler with a sudoku-like constraint.

The sudoku LHS algorithm is a bit like the first stage in the design
of an `N`-dimensional sudoku puzzle, hence the name: each "sudoku box"
must have exactly the same number of samples, and no two samples may
occur on the same axis-aligned hyperplane.

This gives coarse stratification in `N` dimensions with linear runtime.

Supports Python 2.7 and 3.4.


