# -*- coding: utf-8 -*-
##
## This file is part of CDS Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007, 2008 CERN.
##
## CDS Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## CDS Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with CDS Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Regression tests for the search engine query parsers."""

import unittest

from invenio import search_engine_query_parser

from invenio.testutils import make_test_suite, run_test_suite
from invenio.search_engine import perform_request_search as SE_perform_request_search


class TestSpiresToInvenioSyntaxConverter(unittest.TestCase):
    """Test parsing SPIRES syntax 
       
    These tests are written against the INSPIRE "large" set and use 
    invenio.search_engine.perform_request_search which loads the parser
    """

    def _compare_searches(self, invenio_search_query, spires_search_query):
        """Perform two searches and confirm the results are equivalent

        To pass, the hitsets must be non-zero and ordered identically.
        """
        invenio_search_result = SE_perform_request_search(p=invenio_search_query)
        spires_search_result = SE_perform_request_search(p=spires_search_query)

        # first make sure the test is non trivial
        self.assert_(len(spires_search_result)>0)

        # make sure we have the same results
        self.assertEqual(invenio_search_result, spires_search_result)


    ###################################
    # SPIRES syntax parsing / result set tests
    ###################################
    def test_operators(self):
        """SPIRES search syntax: find a ellis and t shapes"""
        invenio_search = "author:ellis and title:shapes"
        spires_search = "find a ellis and t shapes"
        self._compare_searches(invenio_search, spires_search)

    def test_parens(self):
        """SPIRES search syntax: find a ellis and not t hadronic and not t collisions"""
        invenio_search = "author:ellis and not (title:hadronic or title:collisions)"
        spires_search = "find a ellis and not t hadronic and not t collisions "
        self._compare_searches(invenio_search, spires_search)

    def test_author_simple(self):
        """SPIRES search syntax: find a ellis, j"""
        invenio_search = 'author:"ellis, j*"'
        spires_search = 'find a ellis, j'
        self._compare_searches(invenio_search, spires_search)

    def test_author_reverse(self):
        """SPIRES search syntax: find a j ellis"""
        invenio_search = 'author:"ellis, j*"'
        spires_search = 'find a j ellis'
        self._compare_searches(invenio_search, spires_search)

    def test_author_initials(self):
        """SPIRES search syntax: find a a m blik"""
        inv_search = 'author:"blik, a* m*"'
        spi_search = 'find a a m blik'
        self._compare_searches(inv_search, spi_search)

    def test_author_full_initial(self):
        """SPIRES search syntax: find a klebanov, igor r."""
        inv_search = 'author:"klebanov, igor* r*" or author:"klebanov, i.r." or author:"klebanov, ig.r."'
        spi_search = "find a klebanov, igor r."
        self._compare_searches(inv_search, spi_search)


    def test_author_full_first(self):
        """SPIRES search syntax: find a ellis, john"""
        invenio_search = 'author:"ellis, john" or author:"ellis, j.*" or author:"ellis, j" or author:"ellis, jo.*" or author:"ellis, jo" or author:"ellis, john *"'
        spires_search = 'find a ellis, john'
        self._compare_searches(invenio_search, spires_search)

    def test_combine_multiple(self):
        """SPIRES search syntax: find a gattringer, c and k symmetry chiral and not title chiral"""
        inv_search = "author:'gattringer, c*' keyword:chiral  keyword:symmetry -title:chiral "
        spi_search = "find a c gattringer and k symmetry chiral and not title chiral"
        self._compare_searches(inv_search, spi_search)

    def test_combine_multiple_or(self):
        """SPIRES search syntax: find a j ellis and (t report or k cross section)"""
        inv_search = "author:'ellis, j*' and (title:report  or (keyword:cross section))"
        spi_search = "find a j ellis and (t report or k cross section)"
        self._compare_searches(inv_search, spi_search)

    def test_fin_to_find_trans(self):
        """SPIRES search syntax: fin a ellis, j == find a ellis, j"""
        inv_search = "find a ellis, j"
        spi_search = "fin a ellis, j"
        self._compare_searches(inv_search, spi_search)

    def test_quotes(self):
        """SPIRES search syntax: find t 'compton scattering' and a brooks"""
        inv_search = "title:'compton scattering' author:mele"
        spi_search = "find t 'compton scattering' and a mele"
        self._compare_searches(inv_search, spi_search)


TEST_SUITE = make_test_suite(TestSpiresToInvenioSyntaxConverter)


if __name__ == "__main__":
    run_test_suite(TEST_SUITE)

