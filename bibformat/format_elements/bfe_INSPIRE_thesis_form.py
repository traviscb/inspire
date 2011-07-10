# -*- coding: utf-8 -*-
##
## $Id$
##
## This file is part of Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007, 2011 CERN.
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
"""BibFormat element - titles
"""
__revision__ = "$Id$"

from invenio.config import CFG_SITE_SUPPORT_EMAIL, CFG_SITE_URL

def format_element(bfo, action="", onsubmit=""):
    """
    Creates a Thesis Submission form for the record, after checking some variables
    @param onsubmit: a js action to be taken onSubmit
    """



    recid = bfo.control_field("001")

    action = CFG_SITE_URL + "/inspire/thesis_upload"

    form = '''
<form name="fulltext_upload" method="post" onSubmit="%s"
action="%s" enctype="multipart/form-data">
<input type="hidden" name="recid" id="recid" value="%s" />
<table>
<tr id="file_upload" class="form_label_required" ><td class="left">Share
your thesis</td>
<td class="right"><input type="file" name="filedata" size="35" /></td></tr>
<tr></tr>

<tr class="form_label_required"><td class=left>* Your Email</td>
<td class=right>
<input size=35 name="username" id="username"></td></tr>
<tr class="form_label"><td class=left>Your Name</td>
<td class=right><INPUT size=35 name=realname id=realname></td></tr>
<tr class="form_label"><td class=left>Your Advisor</td>
<td class=right><INPUT size=35 name=Advisor id=Advisor></td></tr>
<tr class="form_label"><td class=left>Comments</td>
<td class=right><textarea name="usercomment" id=usercomment rows="2"
cols="35" wrap="virtual"></textarea></td></tr>
<tr><td></td><td><input type="submit"
name="submit" value="Upload My Thesis" class="formbutton" /></td>
</table>
''' % (onsubmit,action,recid)



    for coll in bfo.fields("980__a"):
        if coll == "Thesis":
            return form


    # not a thesis:
    return '''
    <div class="note">This paper does not appear to be a thesis, so submission is not available for this paper.   If you believe this is
    an error, please contact us at <a href="mailto:%s">%s</a>''' % (CFG_SITE_SUPPORT_EMAIL, CFG_SITE_SUPPORT_EMAIL)




# we know the argument is unused, thanks
# pylint: disable-msg=W0613
def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0
# pylint: enable-msg=W0613


