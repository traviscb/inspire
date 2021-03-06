# -*- coding: utf-8 -*-
##
## $Id$
##
## This file is part of Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2010 CERN, SLAC
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
"""BibFormat element - Prints references
"""
__revision__ = "$Id$"

def format_element(bfo, reference_prefix, reference_suffix):
    """
    Prints the references of this record

    @param reference_prefix a prefix displayed before each reference
    @param reference_suffix a suffix displayed after each reference
    """

    from invenio.search_engine import search_unit
    from invenio.bibformat import format_record
    references = bfo.fields("999C5", escape=1)
    out = ""

    for reference in references:
        ref_out = ''

#        if reference.has_key('o'):
#            if out != "":
#                ref_out = '</li>'
#            ref_out += '<li><small>'+\
#                       reference['o']+ "</small> "

        display_journal = ''
        display_report = ''
        clean_report = ''
        clean_journal = ''
        hits = []
        if reference.has_key('s'):
            display_journal = reference['s']
            clean_journal = reference['s']
        if reference.has_key('r'):
            display_report = reference['r']
            clean_report = reference['r']
        if clean_report:
            hits = search_unit(f='reportnumber', p=clean_report)
        if clean_journal and len(hits)!=1:
            hits = search_unit(f='journal', p=clean_journal)
        if reference.has_key('a') and len(hits)!=1:
            hits = search_unit(f='doi', p=reference['a'])
        if len(hits) == 1:
            ref_out += '<small>' +\
                       format_record(list(hits)[0],'hs') + '</small>'


        else:

            if reference.has_key('h'):
                ref_out += "<small> " + reference['h']+ ".</small> "

            if reference.has_key('m'):
                ref_out += "<small>"+ reference['m'] + ".</small> "

            if reference.has_key('a'):
                ref_out += " <small><a href=\"http://dx.doi.org/" + \
                reference['a'] + "\">" + reference['a']+ "</a></small> "

            ref_out += ' <small>'
            if display_journal:
                ref_out += display_journal
            if display_report:
                ref_out += ' ' + display_report
            ref_out += '<br /> <em>(not extracted or not in INSPIRE)</em></small>'



        ref_out += "<br />"

        if reference_prefix is not None and ref_out != '':
            ref_out = reference_prefix + ref_out
        if reference_suffix is not None and ref_out != '':
            ref_out += reference_suffix

        out += ref_out

    if out != '':
        out += '</li>'

    return out

def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0
