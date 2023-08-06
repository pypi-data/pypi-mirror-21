# Copyright  2016  Kevin Murray <spam@kdmurray.id.au>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import absolute_import, division, print_function
from numpy import random
from pymer import hash_to_kmer


def numnt(x):
    if x < 0 or x > 3:
        raise ValueError("numnt must be given a number between 0 & 3")
    return "ACGT"[x]


class MarkovGenerator(object):

    def __init__(self, transcount, seed=None):
        self.P = transcount.transitions
        self.pi = transcount.steady_state
        self.k = transcount.k - 1
        self.bitmask = 2**(2 * self.k) - 1
        self.rand = random.RandomState()
        self.rand.seed(seed)

    def generate_sequence(self, length, seed=None):
        if seed is not None:
            self.rand.seed(seed)

        prev_mer = self.rand.choice(self.pi.size, p=self.pi)
        sequence = list(hash_to_kmer(prev_mer, self.k))

        for x in range(self.k, length):
            # Emission probs for the previous kmer
            p = self.P[prev_mer]
            nt = self.rand.choice(p.size, p=p)
            sequence.append(numnt(nt))
            # Add the nucleotide to the previous hash using bit ops
            # equiv. to x = x[1:] + nt
            prev_mer <<= 2
            prev_mer |= nt
            prev_mer &= self.bitmask

        return ''.join(sequence)
