# This file is part of PyCI.
#
# PyCI is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# PyCI is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyCI. If not, see <http://www.gnu.org/licenses/>.

from filecmp import cmp as compare
from tempfile import NamedTemporaryFile

from nose.tools import assert_raises

import numpy as np

from pyci import doci, comb
from pyci.test import datafile


class TestDOCIWfn:

    CASES = [(16, 8), (64, 1), (64, 4), (65, 1), (65, 4), (129, 3)]

    def test_raises(self):
        assert_raises(ValueError, doci.wfn, 10, 11)
        assert_raises(ValueError, doci.wfn, 10, 0)
        assert_raises(RuntimeError, doci.wfn, 100000, 10000)

    def test_to_from_file(self):
        for nbasis, nocc in self.CASES:
            yield self.run_to_from_file, nbasis, nocc

    def test_add_all_dets(self):
        for nbasis, nocc in self.CASES:
            yield self.run_add_all_dets, nbasis, nocc

    def test_add_excited_dets(self):
        for nbasis, nocc in self.CASES:
            yield self.run_add_excited_dets, nbasis, nocc

    def run_to_from_file(self, nbasis, nocc):
        file1 = NamedTemporaryFile()
        file2 = NamedTemporaryFile()
        wfn1 = doci.wfn(nbasis, nocc)
        wfn1.add_all_dets()
        wfn1.to_file(file1.name)
        wfn2 = doci.wfn.from_file(file1.name)
        wfn2.to_file(file2.name)
        assert compare(file1.name, file2.name, shallow=False)

    def run_add_all_dets(self, nbasis, nocc):
        wfn = doci.wfn(nbasis, nocc)
        wfn.add_all_dets()
        for det in wfn:
            assert wfn.popcnt_det(det) == wfn.nocc
        assert len(wfn) == comb(wfn.nbasis, wfn.nocc)

    def run_add_excited_dets(self, nbasis, nocc):
        wfn = doci.wfn(nbasis, nocc)
        wfn.reserve(comb(wfn.nbasis, wfn.nocc))
        assert_raises(ValueError, wfn.add_excited_dets, -1)
        assert_raises(ValueError, wfn.add_excited_dets, 100)
        length = 0
        for i in range(wfn.nocc + 1):
            length += comb(wfn.nocc, i) * comb(wfn.nvir, i)
            wfn.add_excited_dets(i)
            assert len(wfn) == length
        assert len(wfn) == comb(wfn.nbasis, wfn.nocc)