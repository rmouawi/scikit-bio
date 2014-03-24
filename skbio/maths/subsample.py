#!/usr/bin/env python
r"""
Subsampling (:mod:`skbio.maths.subsample`)
==========================================

.. currentmodule:: skbio.maths.subsample

This module provides functionality for subsampling from vectors of counts.

Functions
---------

.. autosummary::
   :toctree: generated/

   subsample

"""
from __future__ import division

#-----------------------------------------------------------------------------
# Copyright (c) 2013--, scikit-bio development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

import numpy as np


def subsample(counts, n, replace=False):
    """Randomly subsample from a vector of counts.

    Returns a copy of `counts` if `n` is equal to or larger than the number of
    items in `counts`.

    Parameters
    ----------
    counts : 1-D array_like
        Vector of counts (integers) to randomly subsample from.
    n : int
        Number of items to subsample from `counts`.
    replace : bool, optional
        If ``True``, subsample with replacement. If ``False`` (the default),
        subsample without replacement.

    Returns
    -------
    subsampled : ndarray
        Subsampled vector of counts where the sum of the elements equals `n`
        (i.e., ``subsampled.sum() == n``).

    Raises
    ------
    TypeError
        If `counts` cannot be safely converted to an integer datatype.

    Examples
    --------
    Subsample 4 items (without replacement) from a vector of counts:

    >>> import numpy as np
    >>> from skbio.maths.subsample import subsample
    >>> a = np.array([4, 5, 0, 2, 1])
    >>> sub = subsample(a, 4)
    >>> sub.sum()
    4

    Trying to subsample an equal or greater number of items results in the same
    vector as our input:

    >>> subsample([0, 3, 0, 1], 8)
    array([0, 3, 0, 1])

    Subsample 5 items (with replacement):

    >>> sub = subsample([1, 0, 1, 2, 2, 3, 0, 1], 5, replace=True)
    >>> sub.sum()
    5

    """
    counts = np.asarray(counts)
    counts = counts.astype(int, casting='safe')

    if counts.ndim != 1:
        raise ValueError("Only 1-D vectors are supported.")

    counts_sum = counts.sum()
    if counts_sum <= n:
        return counts

    if replace:
        probs = counts / counts_sum
        result = np.random.multinomial(n, probs)
    else:
        nz = counts.nonzero()[0]
        unpacked = np.concatenate([np.repeat(np.array(i,), counts[i])
                                   for i in nz])
        permuted = np.random.permutation(unpacked)[:n]

        result = np.zeros(len(counts), dtype=int)
        for p in permuted:
            result[p] += 1

    return result
